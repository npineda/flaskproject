#################
#### imports ####
#################

import requests
import logging
from pprint import pprint
from flask import render_template, Blueprint, \
    request, flash, redirect, url_for   # pragma: no cover
from flask.ext.login import login_required, current_user   # pragma: no cover

from .forms import MessageForm   # pragma: no cover
from project import db   # pragma: no cover
from project.models import BlogPost   # pragma: no cover
from project.models import User
from sqlalchemy.sql import select


CLIENT_ID = 'XTEKY0EK25W5S0VAWGBETHQNYY20FXPB5P1V2ZMY1GQSJXFW'
CLIENT_SECRET = 'PJFLTVUA5YNSXR2G5ISL5F4N2KOCZEZ2YUHXFWOV01UIGJO4'

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)   # pragma: no cover


################
#### routes ####
################
@home_blueprint.route('/fs_oauth',methods = ['POST'])
def fs_oauth():
    token = current_user.token
    if token == "":
        flash("Connected Already")
        return redirect(url_for('home.home'))
    else:
        return redirect('https://foursquare.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s' % (CLIENT_ID,'https://ec2-54-208-27-46.compute-1.amazonaws.com:8080/fs_get_token'))


@home_blueprint.route('/fs_get_token')
def fs_get_token():
    code = request.args.get('code')
    req = requests.get('https://foursquare.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s' % (CLIENT_ID, CLIENT_SECRET, 'https://ec2-54-208-27-46.compute-1.amazonaws.com:8080/fs_get_token', code))
    token = req.json()['access_token']
    user_request = requests.get('https://api.foursquare.com/v2/users/self?oauth_token=%s&v=20150207' % (token))
    response_dict = user_request.json()['response']
    user_dict = response_dict['user']
    user_id = user_dict['id']
    user = db.session.query(User).filter_by(id=current_user.id).first()
    user.token = token
    user.foursquare_id = user_id
    db.session.commit()
    users = db.session.query(User).all()
    users_printable = dir(users)
    logFile = open('mylog.txt', 'w')
    pprint(users, logFile)
    #print_users()
    #g.db.execute('update users set token=?, foursquare_id=? where name=?', [token, user_id, session.get('current_user')])
    #g.db.commit()
    #flash('successfully connected with foursquare')
    flash('you attempted to login to foursquare')
    return redirect('/')
    
'''@home_blueprint.route('/fs_checkin', methods=['POST'])
def fs_checkin():
    checkin_str = json.loads(request.form['checkin'])
    checkin = json.loads(request.form['checkin'])
    user = checkin['user']
    id = user['id']
    cur = g.db.execute('select name from users where foursquare_id=?', [id])
    users_data = [dict(name=row[0]) for row in cur.fetchall()]
    for current in users_data:
        associated_user = current['name']
        print associated_user
        g.db.execute('insert into entries (title, text, user) values ("Checkin", ?, ?)', [json.dumps(checkin_str), associated_user])
    g.db.commit()
    return ('Thanks', 200, '')'''




# use decorators to link the function to a url
@home_blueprint.route('/', methods=['GET', 'POST'])   # pragma: no cover
@login_required   # pragma: no cover
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()

        flash('New entry was successfully posted. Thanks.')
        flash(url_for('home.home'))

        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template(
            'index.html', posts=posts, form=form, error=error)


@home_blueprint.route('/welcome')   # pragma: no cover
def welcome():
    return render_template('welcome.html')  # render a template

def print_users():
    users = db.session.query(User).all()
    for user in users:
        flash(user.foursquare_id)