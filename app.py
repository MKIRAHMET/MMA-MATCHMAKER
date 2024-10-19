from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#set the SQLALCHEMY_DATABASE_URI key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
#create an SQLAlchemy object named `db` and bind it to your app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fight_library.db'
db = SQLAlchemy(app)

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Initialized the database.")

@app.route('/')
@app.route('/index')
def greeting():
    return render_template('greeting.html')

# app name 
@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

if __name__ == "__main__":
    app.run(debug=True)

#uncomment the code below here when you are done creating database instance db and models
import routes
