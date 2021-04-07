from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jajfghehqmvhty:d53d646f3ad54fbc4dbe08f1ee4e74390ba45b85f89a38718ae2fc4f4bafff88@ec2-23-22-191-232.compute-1.amazonaws.com:5432/d9k5j118537rok?sslmode=require'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = 'contact_database'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    subject = db.Column(db.String(200))
    message = db.Column(db.String)
    
    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message


@app.route('/')
def index(): 
    return render_template('index.html')


@app.route('/success', methods= ['POST'])
def success():
    if request.method == 'POST':
        req_name = request.form['name']
        req_email = request.form['email']
        req_subject = request.form['subject']
        req_message = request.form['message']
        
        data = Data(req_name, req_email, req_subject, req_message)
        db.session.add(data)
        db.session.commit()            
        return render_template('success.html')

if (__name__) == ('__main__'):
    app.run(debug=True)