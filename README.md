## Digital Rewards Program

Webapp component of the Digital Rewards Program project for 611 in Fall 2019. Comes installed with all dependencies and a bunch of static files.

## One Time Setup
Make sure to have Python3.7+ and Django 2.x installed. This is the bare minimum. A complete list of requirements can be found in *requirements.txt*. It is recommended that you use a virtual environment like venv or conda to ensure the correct dependency versions are installed.

To install using conda, 

    conda install --file requirements.txt

To install using pip,

    pip3 install -r requirements.txt

## Usage

Ensure the installation has been complete. Open the root project directory in a shell and run *python manage.py runserver*. The project should run and bar any errors,the web app should run successfully on port [8000](http://localhost:8000) on your local machine

## Project Walkthrough

The webapp uses the concept of Django apps to keep functionality logically separate. All logic related to business management and dashboard views are inside the dashboard app, the account login stuff is inside accounts and so on. Largely form based with API interaction, the forms are defined in forms.py inside individual apps and the views.py files hold the logic, for each form in each app. 

The json files in the root project directory keep track of session info for the current user. Although not ideal, it's an easy fix to move to browser session storage and something that shouldn't take long to implement. 

## Deploy to Heroku
THe process of deploying the app to Heroku is simple and a guide for the same can be found [here](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment)

All the files necessary for deployment are a part of the project package and so, deployment should be simple and involve setting up a Heroku account and registering it on the local machine. 

Thanks to Alan, Ethan, Katie and CSE@UB for giving us the chance to create something worthhwile and notable in a semester!

Happy Coding!

| || ||___ \ 
| || |_ __) |
|__   _/ __/ 
   |_||_____|