from flask import Flask, render_template, g, request, redirect, url_for
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from boto.s3.connection import S3Connection

app = Flask(__name__)

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
# db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/blog"
# db_uri = "postgresql://ucisgcrsvynlud:17ddf90852366f1446ea2d1b3e9b95032cdc9f0bdd444a7446b2c7304604e18d@ec2-54-159-22-90.compute-1.amazonaws.com:5432/dd9rlcfn5lcueh"
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = s3
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

@app.route('/')
def hello_world():
    entries = Entry.query.order_by(desc(Entry.id)).all()
    return render_template('index.html', entries=entries)

@app.route('/post', methods=['POST'])
def add_entry():
    if request.form['password'] == '1234' and request.form['title'] != "" and request.form['body'] != "":
        entry = Entry()
        entry.title = request.form['title']
        entry.body = request.form['body']
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('hello_world'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    if request.form['password'] == '1234':
        post_id = request.form['post_id']
        entry = Entry.query.filter(Entry.id == post_id).first()
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('hello_world'))

@app.route('/update', methods=['POST'])
def update_entry():
    post_id = request.form['post_id']
    entry = Entry.query.filter(Entry.id == post_id).first()
    return render_template("update.html", entry=entry)

@app.route('/update_post', methods=['POST'])
def update_post():
    if request.form['password'] == '1234' and request.form['title'] != "" and request.form['body'] != "":
        post_id = request.form['post_id']
        entry = Entry.query.filter(Entry.id == post_id).first()
        entry.title = request.form['title']
        entry.body = request.form['body']
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('hello_world'))
