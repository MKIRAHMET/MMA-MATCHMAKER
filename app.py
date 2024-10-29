from flask import Flask, render_template
from extension import db
from flask_login import LoginManager, UserMixin, current_user
from models import User
from flask_wtf.csrf import CSRFProtect


 
# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fight_library.db'
csrf = CSRFProtect(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
# Initialize the database with app context
db.init_app(app)
import routes 
# Home route and custom error handlers
@app.route('/')
@app.route('/index')
def greeting():
    user = current_user if current_user.is_authenticated else None
    
    # Determine the appropriate base template
    if user:
        base_template = "baseadmin.html" if user.is_admin else "baseuser.html"
    else:
        base_template = "base.html"  # Fallback template if no user found
    
    # Render the template with dynamic user information and base template
    return render_template('greeting.html', user=user, base_template=base_template)


@app.errorhandler(404)
def not_found(e):
    user = current_user if current_user.is_authenticated else None
    if user:
        if user.is_admin == 1:
            base_template = "baseadmin.html"
        else:
            base_template = "baseuser.html"
    else:
        base_template = "base.html"
    return render_template("404.html",base_template=base_template), 404

# Start the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created before running the server
    app.run(debug=True)
    
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

