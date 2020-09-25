from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import os

dbdir="sqlite:///"+os.path.abspath(os.getcwd())+"/database.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db= SQLAlchemy(app)

class proyecto(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    name1=db.Column(db.String(50), nullable=False)
    name2=db.Column(db.String(50), nullable=True)
    name3=db.Column(db.String(50), nullable=True)
    name4=db.Column(db.String(50), nullable=True)
    content1=db.Column(db.String(800), nullable=False)
    logo=db.Column(db.String(500), nullable=False)
    url=db.Column(db.String(500), nullable=False)
class message(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    namef=db.Column(db.String(100), nullable=False)
    emailf=db.Column(db.String(500), nullable=False)
    contentf=db.Column(db.String(500), nullable=True)

enlace=True

@app.route("/")
def home():
    global enlace
    proyectos=proyecto.query.all()
    if enlace==True:
        enlace==False
    else:
        enlace==True
    return render_template("index.html", proyectos=proyectos, enlace=enlace)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method=="POST":
        bd_proyect= proyecto(title=request.form["title"], name1=request.form["name1"], name2=request.form["name2"], name3=request.form["name3"], name4=request.form["name4"], content1=request.form["content1"], logo=request.form["imagen"], url=request.form["url"])
        if bd_proyect.title=="" or bd_proyect.name1==""  or bd_proyect.content1=="" or bd_proyect.logo=="" or bd_proyect.url=="":
            return redirect(url_for('error1'))
        elif len(bd_proyect.title)>=100 or len(bd_proyect.name1)>=50 or len(bd_proyect.name2)>=50 or len(bd_proyect.name3)>=50 or len(bd_proyect.name4)>=50 or len(bd_proyect.content1)>=800:
            return redirect(url_for('error2'))
        elif len(bd_proyect.content1)<=50:
            return redirect(url_for('error3'))

        db.session.add(bd_proyect)
        db.session.commit()

        return redirect(url_for('done'))
    return render_template("add.html")


@app.route('/contacto', methods=["GET","POST"])
def contacto():
    if request.method=="POST":
        bd_message= message(namef=request.form["namef"], emailf=request.form["emailf"], contentf=request.form["contentf"])
        db.session.add(bd_message)
        db.session.commit()
        return redirect(url_for('done2'))
    return render_template("contacto.html")

@app.route("/informacion")
def informacion():
    return render_template("informacion.html")

@app.route("/done")
def done():
    return render_template("done.html")

@app.route("/done2")
def done2():
    return render_template("done2.html")

@app.route("/error1")
def error1():
    return render_template("error1.html")

@app.route("/error2")
def error2():
    return render_template("error2.html")

@app.route("/error3")
def error3():
    return render_template("error3.html")

@app.errorhandler(404)
def error4(err):
 return render_template('error4.html'), 404
if __name__=="__main__":
    db.create_all()
    app.run( port=5000,debug=True)
