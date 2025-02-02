from flask import *
from flask_login import *
import os

app = Flask (__name__)
app.secret_key = 'dany_buster16'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'user' : {'password':'123456789'}}
def load_data(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open (file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
                except json.JSONDecodeError:
                    print(f'JSONDecodeError in file: {filename}')
    return all_data


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
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))
@app.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
    data_folder = 'data'
    all_data = load_data(data_folder)
    return render_template('admin.html', data = all_data)
@app.route('/')
def main_page():
    data_folder = 'data'
    all_data = load_data(data_folder)
    return render_template('index.html', data = all_data)
@app.route('/add', methods=['GET', 'POST'])
def create_new():
    data_folder = 'data'
    all_data = load_data(data_folder)
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)