from flask import Flask,redirect,url_for,render_template,request
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user
from models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HellY0uAintGett1n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = '.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    #the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

#hello


@app.route('/',methods=['GET','POST'])
def home():
    return render_template("index.html")



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)





#Login
@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('.profile'))





#Signup is parted in two, signup rute you see, and the one that authenticates
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))  
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('.login'))






@app.route('/logout')
def logout():
    return 'Logout'







if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=8080,debug=True)