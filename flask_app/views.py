from flask import render_template, request, redirect, url_for, send_file
from flask_app import app, db, bcrypt
from flask_app.models import User, List, Card
from flask_login import login_user, login_required, logout_user, current_user
from flask_app.helper_funcs import generate_csv
from werkzeug.utils import secure_filename
from datetime import datetime
import csv

# the main landing page of the site
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html') #display the registration form in case of a GET request
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # check if the username already exists, if it does, render a page to the user "username already exists"
        usr = User.query.filter_by(username=username).first()
        if usr:
            return render_template('error_page.html', error_msg="It looks like this username already exists.")
            # return "Username already exists. Please choose a different username."
        else:
            # a unique user is being created, so lets add him to the db and hash his password
            hashed_password = bcrypt.generate_password_hash(password) #this generates a hash of the password entered in the form

            usr_obj = User(username=username, email=email, password=hashed_password)
            db.session.add(usr_obj)
            db.session.commit()

            # user has been successfully created, so flash a message telling "Account Created Successfully" and take him to the login page.
            return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html') #display the login form in case of a GET request
    else:
        username = request.form['username']
        password = request.form['password']

        #check if a user with this username exists or not, if it does take him to the dashboard, if it doesn't display a message "Account doesn't exist"
        user = User.query.filter_by(username=username).first()
        if user: #if user exists, check if the entered password matches the hashed password
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(f'/{username}/dashboard')
            else:
                # if the passwords dont match, flash a message "Incorrect Password"
                return render_template('error_page.html', error_msg="It looks like you entered an incorrect password!")
        else:
            #display a message, "account doesn't exist"
            return render_template('error_page.html', error_msg="An account with this username doesn't exist.")

# the main user dashboard
@app.route('/<username>/dashboard')
@login_required
def dashboard(username):
    return render_template('dashboard.html', user=current_user)

@app.route('/<username>/create-list', methods=['GET', 'POST'])
@login_required
def create_list(username):
    if request.method == 'GET': #display the list creation form in case of a GET request
        return render_template('create_list.html')
    else:
        list_title = request.form['list_title']
        #create a new list object with this title
        new_list = List(list_title=list_title, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        #after creating the list, take the user back to dashboard
        return redirect(f'/{username}/dashboard')

@app.route('/<username>/create-card/inside-list/<list_id>', methods=['GET', 'POST'])
@login_required
def create_card(username, list_id):
    if request.method == 'GET': #display the card creation form in case of a GET request
        return render_template('create_card.html')
    else:
        card_title = request.form['card_title']
        card_content = request.form['card_content']
        status = request.form['status']
        deadline = request.form['deadline']
        list_obj = List.query.get(list_id)
        
        #this deadline date is a string, need to convert it to datetype, can use the strptime method for this:
        proper_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        # create a new card with these values
        card_obj = Card(card_title=card_title, card_content=card_content, status=status, deadline=proper_date, list_id=list_obj.list_id)
            
        db.session.add(card_obj)
        db.session.commit()
        #after creating the card, take the user back to dashboard
        return redirect(f'/{username}/dashboard')

@app.route('/<username>/edit-list/<list_id>', methods=['GET', 'POST'])
@login_required
def edit_list(username, list_id):
    if request.method == 'GET': #display the list edit form in case of a GET request
        return render_template('edit_list.html')
    else:
        list_title = request.form['list_title']
        list_obj = List.query.get(list_id)
        #change the title of the list with this new title
        list_obj.list_title = list_title
        db.session.commit()
        return redirect(f'/{username}/dashboard')


@app.route('/<username>/edit-card/<card_id>', methods=['GET', 'POST'])
@login_required
def edit_card(username, card_id):
    if request.method == 'GET': #display the edit card form in case of a GET request
        card_obj = Card.query.get(card_id)
        return render_template('edit_card.html', user=current_user, card=card_obj)
    else:
        card_title = request.form['card_title']
        card_content = request.form['card_content']
        status = request.form['status']
        deadline = request.form['deadline']
        list_id = int(request.form['list-id']) #get the list id of the list from the form
        card_obj = Card.query.get(card_id)
        
        #change the values of the card using these new ones
        card_obj.card_title = card_title
        card_obj.card_content = card_content
        card_obj.status = status
        card_obj.list_id = list_id

        #this deadline date is a string, need to convert to datetype, can use the strptime method for this:
        proper_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        card_obj.deadline = proper_date
        
        db.session.commit()
        #after creating the card, take the user back to dashboard
        return redirect(f'/{username}/dashboard')

@app.route('/<username>/delete-list/<list_id>')
@login_required
def delete_list(username, list_id):
    #fetch the list with this id and delete it
    list_obj = List.query.get(list_id)
    db.session.delete(list_obj)
    db.session.commit()
    return redirect(f'/{username}/dashboard')

@app.route('/<username>/delete-card/<card_id>')
@login_required
def delete_card(username, card_id):
    #fetch the card with this id and delete it
    card_obj = Card.query.get(card_id)
    db.session.delete(card_obj)
    db.session.commit()
    return redirect(f'/{username}/dashboard')

@app.route('/<username>/stats')
@login_required
def stats(username):
    #stats and summary page for the user
    current_date = datetime.today().date() #fetches today's date
    return render_template('stats.html', user=current_user, current_date=current_date)

@app.route('/<username>/export')
@login_required
def export(username):
    #export all user data, give user the option to choose a file destination
    generate_csv(username)
    path = 'exported_content.csv'
    return send_file(path, as_attachment=True)

@app.route('/<username>/import', methods=['GET', 'POST'])
@login_required
def import_csv(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        return render_template('import.html')
    else:
        f = request.files['file']
        f.filename = 'user_import.csv' #set a name for this file
        f.save(app.config['UPLOAD_FOLDER']+f.filename) #save the file in the upload_folder

        g = open('./flask_app/user_data/user_import.csv', 'r')
        g.readline() #skip the header line
        reader = csv.reader(g)
        
        prev_list_id = 0
        for line in reader:
            current_list_id = int(line[0])
            list_title = line[1].strip()
            card_title = line[3].strip()
            card_content = line[4].strip()
            card_status = line[5].strip()
            card_deadline = line[6].strip()

            #this deadline date is a string, need to convert to datetype, can use the strptime method for this:
            proper_date = datetime.strptime(card_deadline, '%Y-%m-%d').date()

            if prev_list_id != current_list_id:
                list_obj = List(list_title=list_title, user_id=user.id)
                db.session.add(list_obj)
                db.session.commit()
                card_obj = Card(card_title=card_title, card_content=card_content, status=card_status, deadline=proper_date, list_id=list_obj.list_id)
                db.session.add(card_obj)
                db.session.commit()
                prev_list_id = current_list_id #update the previous list id
            else:
                card_obj = Card(card_title=card_title, card_content=card_content, status=card_status, deadline=proper_date, list_id=list_obj.list_id)
                db.session.add(card_obj)
                db.session.commit()        

        return redirect(f'/{username}/dashboard')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # display a message to the user: "You've been successfully logged out"
    return render_template('logged_out.html')

@app.route('/about')
def about():
    return render_template('about.html')