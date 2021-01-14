from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app=Flask(__name__)
app.config['SECRET_KEY'] = 'HellY0uAintGett1n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'





@app.route('/',methods=['GET','POST'])
def home():
    return render_template("index.html")



@app.route('/profile')
def profile():
    return 'Profile'


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return 'Signup'

@app.route('/logout')
def logout():
    return 'Logout'


#Position all of this after the db and app have been initialised
"""bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(user_id):
    #TODO change here
    return User.query.get(user_id)
"""












if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=8080,debug=True)