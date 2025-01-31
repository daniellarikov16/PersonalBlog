from flask import *
from flask_login import *

app = Flask (__name__)
app.secret_key = 'dany_buster16'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'user' : {'password':'123456789'}}
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password in users[username]['password']:
            user = User(username)
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Вы ввели неверные данные!', 'error')
    return render_template('login.html')
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('admin.html')
if __name__ == '__main__':
    app.run(debug=True)