from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import algorithm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mail.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mail(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(10), nullable = False)
    matter = db.Column(db.String(1000), nullable = False)
    category = db.Column(db.String(10), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.email}"



@app.route('/', methods = ['GET','POST'])
def mail():
    if request.method == 'POST':
        email = (request.form['email'])
        matter = (request.form['matter'])

        input_mail = [matter]
        # convert text to feature vectors
        input_data_features = algorithm.feature_extraction.transform(input_mail)
        # making prediction
        prediction = algorithm.model.predict(input_data_features)
        # print(prediction)
        if prediction[0] == 1:
            category = 'Spam mail'
            print(category)
        else:
            category = 'Ham mail'
            print(category)

        mail = Mail(email=email, matter=matter, category=category)
        db.session.add(mail)
        db.session.commit()
    allemail = Mail.query.all()
    return render_template('index.html', allemail=allemail)



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/delete/<int:sno>')
def delete(sno):
    mail = Mail.query.filter_by(sno = sno).first()
    db.session.delete(mail)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        email = (request.form['email'])
        matter = (request.form['matter'])
        mail = Mail.query.filter_by(sno = sno).first()
        mail.email = email
        mail.matter = matter
        db.session.add(mail)
        db.session.commit()
        return redirect("/")
    mail = Mail.query.filter_by(sno = sno).first()
    return render_template('update.html', mail=mail)

@app.route('/show/<int:sno>',methods = ['GET','POST'])
def show(sno):
    if request.method == 'POST':
       return redirect("/")
    mail = Mail.query.filter_by(sno = sno).first()
    return render_template('show.html', mail=mail)

if __name__ == '__main__':
    app.run(debug = True,port = 8000)

