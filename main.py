from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import os 
from datetime import datetime

DB_NAME = 'todo.db'

app = Flask(__name__)

app.config['SECRET_KEY']= "lkjhgfrtyuuop"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
#class içinde tablo oluştururum sonra

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(100), nullable = False)
    completed=db.Column(db.Integer, default=0) #??
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    

@app.route("/", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        new_content=request.form['content']
        if new_content == "":
            return 'Please enter some task'
        else:
            new_task=Todo(content=new_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task!'
        
    else:
        tasks= Todo.query.order_by(Todo.date.desc()).all()
        return render_template('main.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
 

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue uptading that task'
        
    else:
        return render_template("update.html", task=task)
    

@app.errorhandler(404)
def error(e):
    return render_template('404.html')
    

if __name__ == "__main__":

    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
