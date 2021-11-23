from .models import User, get_todays_recent_posts, get_nodes_edges, get_posts, get_devices, get_labels, get_algo, run_algo, pagerank_table
from flask import Flask, request, session, redirect, url_for, render_template, flash
from .forms import RegistrationForm, LoginForm, PostForm, DropForm, RunForm

app = Flask(__name__)

@app.route('/')
def index(methods=['GET']):
    form = PostForm()
    devices = get_devices()
    return render_template('index.html',form=form,devices=devices)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        if len(username) < 2:
            flash('Your username must be at least two characters.','error')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.','error')
        elif not User(username).register(password):
            flash('A user with that username already exists.','error')
        else:
            session['username'] = username
            flash('Success! Account Created! Go to the login page to sign in!','flash')
            return redirect(url_for('register'))

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        if not User(username).verify_password(password):
            flash('Invalid login.','error')
        else:
            session['username'] = username
            # flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    # flash('Logged out.')
    return redirect(url_for('index'))

# @app.route('/index')
# def index():
#     form = PostForm()
#     title = form.title.data
#     tags = form.tags.data
#     text = form.text.data
#     reltn = form.reltn.data
#     return render_template('index.html',form=form)

@app.route('/add_post', methods=['POST'])
def add_post():
    form = PostForm()
    title = form.title.data
    tags = form.tags.data
    text = form.text.data
    device = request.form['device_list']
    print(device)

    # reltn = form.reltn.data
    
    if not title:
        flash('You must give your post a title.','error')
    elif not tags:
        flash('You must give your post at least one tag.','error')
    elif not text:
        flash('You must give your post a text body.','error')
    else:
        User(session['username']).add_post(title, tags, text, device)
        flash('Your insight has been published!','flash')

    return redirect(url_for('index'))


@app.route('/plots')
def plots():
    labels,orient = get_labels()
    form = DropForm()
    return render_template("viz.html",labels=labels,orient=orient,form=form)#,device=device)


@app.route('/vis', methods=['GET', 'POST'])
def vis():
    labels,orient = get_labels()
    device = request.form['label_list1']
    dirt = request.form['label_list2']
    form = DropForm()
    return render_template("viz.html",labels=labels,orient=orient,device=device,form=form,dirt=dirt)


@app.route('/algo')
def algo():
    labels = get_algo()
    form = RunForm()
    headers,rows = pagerank_table()
    return render_template("algo.html",headers=headers,rows=rows,labels=labels,form=form)
    
@app.route('/algo_run', methods=['GET', 'POST'])
def algo_run():
    # labels = get_algo()
    algo = request.form['algo_list']
    # form = DropForm()
    # headers,rows = pagerank_table()
    run_algo(algo)
    flash("You've successfully run your algorithm!",'flash')

    return redirect(url_for('algo'))#render_template("algo.html",headers=headers,rows=rows,labels=labels,form=form)

@app.route('/table')
def table():
    headers,rows = get_posts()
    posts = get_todays_recent_posts()
    return render_template("table.html",headers=headers,rows=rows,posts=posts)


@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )
