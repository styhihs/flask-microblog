from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Taiwan!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'BlahBlahBlah~'
        }
    ]
    return render_template('index.html', title = 'Homepage', user = user, posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    # avoid doing second login
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        #print 'loginininini'
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    # resp: information returned by the OpenID provider
    print 'resp.email: ' + resp.email
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    print 'herererere'
    print User.query.all()
    
    user = User.query.filter_by(email = resp.email).first()
    print 'ohohohohohohohohoh'
    # New user
    if user is None:
        print 'add new user!!!'
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    print 'NOT NEW USER'
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    print 'gooooooooooooooooooooood'
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user   # current_user is set by Flask-Login
