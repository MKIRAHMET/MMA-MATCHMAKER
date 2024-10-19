from flask import Flask, render_template
from extension import db


# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fight_library.db'

# Initialize the database with app context
db.init_app(app)
import routes 
# Home route and custom error handlers
@app.route('/')
@app.route('/index')
def greeting():
    return render_template('greeting.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Start the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created before running the server
    app.run(debug=True)
