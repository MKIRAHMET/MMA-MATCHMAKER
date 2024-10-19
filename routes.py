from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app import app, db
from models import User, Fighters, FightItem, Fights
from forms import FighterForm

# The home page of matchmaker
@app.route('/profiles')
def profiles():
    current_users = User.query.all()
    return render_template('users.html', current_users=current_users)

# Displays profile pages for a user with the user_id primary key
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404(description="No such user found.")
    my_matchmaking = Fights.query.get(user.fights_id)
    return render_template('profile.html', user=user, my_matchmaking=my_matchmaking)

# Adds new fight items (matches)
@app.route('/add_item/<int:user_id>/<int:red_corner_id>/<int:blue_corner_id>/<int:fight_id>')
def add_item(user_id, red_corner_id, blue_corner_id, fight_id):
    user = User.query.filter_by(id=user_id).first_or_404(description="No such user found.")

    existing_fight = FightItem.query.filter(
        ((FightItem.red_corner_id == red_corner_id) & (FightItem.blue_corner_id == blue_corner_id)) |
        ((FightItem.red_corner_id == blue_corner_id) & (FightItem.blue_corner_id == red_corner_id))
    ).first()

    if existing_fight:
        flash("This fight pairing already exists.", "warning")
        return redirect(url_for('profile', user_id=user_id))

    new_item = FightItem(
        red_corner_id=red_corner_id, 
        blue_corner_id=blue_corner_id, 
        fight_id=fight_id
    )

    db.session.add(new_item)
    db.session.commit()

    flash("New fight item successfully added.", "success")
    return redirect(url_for('profile', user_id=user_id))

# Removes an existing fight item
@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
    # Fetch the item to be deleted
    fight = FightItem.query.get(item_id)
    if not fight:
        flash("Fight item not found.", "error")
    else:
        # Delete the item
        db.session.delete(fight)
        db.session.commit()
        flash("Fight item successfully removed.", "success")

    return redirect(url_for('profile', user_id=user_id))

# Display the Dashboard page with a form for adding fighters
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    form = FighterForm()
    if request.method == 'POST' and form.validate():
        # Create a new fighter
        new_fighter = Fighters(
            name=form.name.data, 
            surname=form.surname.data, 
            weight_class=form.weight_class.data, 
            team=form.team.data, 
            coach=form.coach.data
        )
        # Add to the database
        db.session.add(new_fighter)
        db.session.commit()
        flash("New fighter successfully added.", "success")
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        flash("There were errors in the form. Please correct them.", "error")

    fighters = Fighters.query.all()
    return render_template('dashboard.html', fighters=fighters, form=form)
