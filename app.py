from flask import Flask, render_template, g, request, redirect, url_for
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)

# db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/blog"
db_uri = "postgresql://jfwcbbxfvjylzw:62a5c2ccfa32861ed2803b9588adea30a18df6051aa15bb68edad08d1396efd6@ec2-18-214-35-70.compute-1.amazonaws.com:5432/d2uo3bne364pp2"
# DATABASE_URL=$(heroku config:get DATABASE_URL -a your-app) your_process
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
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
