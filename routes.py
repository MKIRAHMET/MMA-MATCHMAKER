from flask import render_template, request, redirect, flash, url_for
from extension import db  # Use db from extension
from models import User, Fighter, Matchup, Fight  # Correct model imports
from forms import FighterForm, RegistrationForm, LoginForm, FightForm
from flask_login import current_user, login_user, login_required, logout_user,login_manager
from functools import wraps

# Define your routes here
from app import app 

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs): 
        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('greeting')) 
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = current_user if current_user.is_authenticated else None
    if user:
        base_template = "baseadmin.html" if user.is_admin else "baseuser.html"
    else:
        base_template = "base.html"
    if form.validate_on_submit():
     
        username = form.username.data
        password = form.password.data
        
 
        user = User.query.filter_by(username=username).first()
        

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form, base_template=base_template) 

@app.route('/profiles')
@login_required
@admin_required
def profiles():
    base_template = "baseadmin.html"
    user = current_user if current_user.is_authenticated else None
    current_users = User.query.all()
    return render_template('users.html',base_template=base_template, user=user, current_users=current_users)



@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = current_user if current_user.is_authenticated else None
    if user and user.id == user_id:
        # Fetch only the fights added by the current user
        my_fights = Fight.query.filter_by(user_id=current_user.id).all()  # Adjusted to get user's fights
        my_matchmaking = current_user.matchups.all()  # Fetch matchups for current user
    else:
        flash("Unauthorized access to another user's profile.", "error")
        return redirect(url_for('profiles'))  # Redirect to a safe page

    if user:
        base_template = "baseadmin.html" if user.is_admin else "baseuser.html"
    else:
        base_template = "base.html" 
    return render_template('profile.html', base_template=base_template, user=user, my_fights=my_fights, my_matchmaking=my_matchmaking)


@app.route('/add_item', methods=["GET", "POST"])
@login_required
def add_item():
    form = FightForm()
    user = current_user if current_user.is_authenticated else None

    # Determine which base template to use based on user role
    base_template = "baseadmin.html" if user and user.is_admin else "baseuser.html" if user else "base.html"

    if request.method == 'POST':
        if form.validate_on_submit():
            # Create a new Fight instance from the form data
            new_fight = Fight(
                weight_class=form.weight_class.data,
                red_corner=form.red_corner.data,
                blue_corner=form.blue_corner.data,
                styles=form.styles.data,
                round=form.round.data,
                time=form.time.data,
                user_id=user.id  # Set the user_id to the current user's ID
            )
            # Add the new fight to the session and commit it
            db.session.add(new_fight)
            db.session.commit()
            flash("New fight successfully added.", "success")
            return redirect(url_for('add_item'))  # Redirect to avoid form resubmission
        else:
            # Display specific errors in the form
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in '{field}': {error}", "error")

    # Fetch all fights to display
    fights = Fight.query.all()

    return render_template(
        'add_item.html',
        base_template=base_template,
        user=user,
        fights=fights,
        form=form
    )


@app.route('/remove_item/<int:user_id>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def remove_item(user_id, item_id):
    user = current_user if current_user.is_authenticated else None
    base_template = "baseadmin.html" if user and user.is_admin else "baseuser.html" if user else "base.html"
    
    # Ensure the user is authorized to remove this item
    if current_user.id != user_id:
        flash("Unauthorized access.", "error")
        return redirect(url_for('profile', user_id=current_user.id))

    # Fetch the fight to remove
    fight_to_remove = Fight.query.get(item_id)
    
    if fight_to_remove and fight_to_remove.user_id == user_id:
        db.session.delete(fight_to_remove)
        db.session.commit()
        flash("Fight removed successfully.", "success")
    else:
        flash("Fight not found or unauthorized.", "error")

    return redirect(url_for('profile', user_id=user_id))

@app.route('/edit_item/<int:user_id>/<int:fight_id>', methods=['GET', 'POST'])
@login_required
def edit_item(user_id, fight_id):
    user = current_user if current_user.is_authenticated else None
    # Determine which base template to use
    base_template = "baseadmin.html" if user and user.is_admin else "baseuser.html" if user else "base.html"

    # Ensure the user is authorized to edit this item
    if current_user.id != user_id:
        flash("Unauthorized access.", "error")
        return redirect(url_for('profile', user_id=current_user.id))

    # Fetch the fight to edit
    fight_to_edit = Fight.query.get(fight_id)

    # Check if the fight exists and is associated with the user
    if not fight_to_edit or fight_to_edit.user_id != user_id:
        flash("Fight not found or unauthorized.", "error")
        return redirect(url_for('profile', user_id=current_user.id))

    if request.method == 'POST':
        # Ensure all required form fields are present
        try:
            fight_to_edit.blue_corner = request.form['blue_corner']
            fight_to_edit.red_corner = request.form['red_corner']
            fight_to_edit.styles = request.form['styles']  # Ensure styles is included in the form

            # Commit the changes to the database
            db.session.commit()
            flash("Fight updated successfully.", "success")
        except KeyError as e:
            flash(f"Missing field: {str(e)}", "error")
        except Exception as e:
            flash(f"An error occurred while updating the fight: {str(e)}", "error")
        
        return redirect(url_for('profile', user_id=user_id))

    # Render the edit template, passing base_template and user as context
    return render_template('edit_fight.html', fight=fight_to_edit, base_template=base_template, user=user)

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
@admin_required
def dashboard():
    user = current_user if current_user.is_authenticated else None
    form = FighterForm()
    if request.method == 'POST' and form.validate():
        new_fighter = Fighter(
            name=form.name.data, 
            surname=form.surname.data, 
            weight_class=form.weight_class.data, 
            team=form.team.data, 
            coach=form.coach.data,
            gender=form.gender.data
        )
        db.session.add(new_fighter)
        db.session.commit()
        flash("New fighter successfully added.", "success")
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        flash("There were errors in the form. Please correct them.", "error")
    if user:
        base_template = "baseadmin.html" if user.is_admin else "baseuser.html"
    else:
        base_template = "base.html"  # Fallback template if no user found
    fighters = Fighter.query.all()
    return render_template('dashboard.html',base_template=base_template, fighters=fighters, form=form, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()  # Adjusted indentation
    if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    base_template = 'base.html'
    return render_template('register.html',base_template=base_template, title='Register', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))