# Minikan
Minikan is a simple and minimal Kanban board for managing and organizing your tasks. It helps to increase productivity by letting you visualizing your workflow.

## Features
* Create, update and delete different cards and lists
* Move cards between lists
* Set deadlines for cards/mark them pending or complete
* Login/Signup management system (allows you to create accounts and login)
* Summary page for stats about the cards
* Import/Export data as CSV
* Custom error pages that show helpful error messages
* Simple and visually pleasing layout/design

## Technologies Used
Minikan is created using:
+ Flask
+ Flask-SQLAlchemy
+ Flask-login
+ Flask-Bcrypt
+ Matplotlib

## Project structure
This app consists of the following files:

```
requirements.txt        # required packages for running the application
README.md               # Contains info and setup instructions for the app
run.py                  # runs the app
flask_app/              # application package
    __init__.py         # initializes the app, creates instances for Flask, SQLAlchemy, Bcrypt
    views.py            # contains all the views for the app
    models.py           # contains the database models for the app
    helper_funcs.py     # helper functions for generating plots, exporting data as csv
    kanban.sqlite3      # sqlite database for the app
    static/             # static files like css, images
    templates/          # contains the html templates
```



## Installation Instructions
Follow the instractions bellow to run the app on your local machine:

1. Create a virtual environment
```
$ python3 -m venv venv  
```
2. Activate the Virtual Environment
```
$ source venv/bin/activate (Linux)
\venv\Scripts\activate     (Windows)
```
3. Install all the requirements
```
(venv) $ pip3 install -r requirements.txt
```
4. Start the app:
```
(venv) $ python3 run.py
```
The app will now be running at http://127.0.0.1:5000

## Minikan in action:
+ Main page
<img src="/flask_app/static/images/landing.png" alt="landing"/>

+ Creating an account
<img src="/flask_app/static/images/register.png" alt="register"/>

+ Dashboard
<img src="/flask_app/static/images/dashboard.png" alt="dashboard"/>

+ Quick Stats
<img src="/flask_app/static/images/stats.png" alt="stats"/>

## Resources that helped me create this project:
+ [Creating a kanban layout using CSS grid](https://ilikekillnerds.com/2020/09/create-a-trello-kanban-layout-using-css-grid/)
+ [Flask-login](https://flask-login.readthedocs.io)
+ [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com)
+ [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### Image Credits
The credits for all the images used in this project goes to their creators. Without them, the board would look too bland and empty. Thanks!
