#################
#### imports ####
#################

from flask import render_template, Blueprint, \
    request, flash, redirect, url_for   # pragma: no cover
from flask.ext.login import login_required, current_user   # pragma: no cover

from .forms import MessageForm   # pragma: no cover
from project import db   # pragma: no cover
from project.models import BlogPost   # pragma: no cover
from project.models import User
from sqlalchemy.sql import select

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
@home_blueprint.route('/foursquare_oauth',methods = ['POST'])
def foursquare_oauth():
    #user = db.session.query(User).filter_by(id = current_user.id)
    #s = select(users).where(users.id == current_user.id)
    #result = db.session.execute(s)
    #current_user = db.session.query('select token from users where name=?',current_user.id)
    token = current_user.token
    if token == "":
        flash("User is not connected yet")
        #flash("Connected Already")
        #return redirecturl('/')  # may need to fix this line
   # else:
        #return redirect('https://foursquare.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s' % (CLIENT_ID),'my aws site accept endpoint')


'''@app.route('/foursquare_accept')
def foursquare_accept():
    code = request.args.get('code')
    r = requests.get('https://foursquare.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s' % (CLIENT_ID, CLIENT_SECRET, 'my accept endpoint', code))
    token = r.json()['access_token']
    user_request = requests.get('https://api.foursquare.com/v2/users/self?oauth_token=%s&v=20150207' % (token))
    response_dict = user_request.json()['response']
    user_dict = response_dict['user']
    user_id = user_dict['id']
    g.db.execute('update users set token=?, foursquare_id=? where name=?', [token, user_id, session.get('current_user')])
    g.db.commit()
    flash('successfully connected with foursquare')
    return redirect('/')'''
    
'''@app.route('/foursquare_checkin', methods=['POST'])
def foursquare_checkin():
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
        flash(current_user.id)
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template(
            'index.html', posts=posts, form=form, error=error)


@home_blueprint.route('/welcome')   # pragma: no cover
def welcome():
    return render_template('welcome.html')  # render a template
