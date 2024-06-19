from flask import Flask, abort, redirect, render_template, request, session, url_for, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjjhjhjkhskjjlkajiohrfjkjhrn'


menu = [{"name": "Установка", "url": "install-flask"},
        {"name":"Первое приложение", "url": "first-app"}, 
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/")
def index():
    print(url_for('index'))
    return render_template("index.html", menu=menu, title="Про Flask")


# Эндпоинт профиля зарегистрированного пользователя
@app.route("/profile/<username>")
def profile(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    return f"Пользователь: {username}"


# Эндпоинт о сайте
@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте")


# Обработка формы
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено!', category='success')
        else:
            flash('Ошибка отправки!', category='error')
        print(request.form)
    return render_template('contact.html', title="Обратная связь", menu=menu)


# Обработчик ошибки сервера 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


# Обработчик для авторизации и редиректа
@app.route("/login", methods=["POST", "GET"])
def login():
    if "userLogged" in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'zufs' and request.form['psw'] == '123':
        session["userLogged"] = request.form["username"]
        return redirect(url_for('profile', username=session['userLogged']))
    
    return render_template('login.html', title="Авторизация", menu=menu)


#with app.test_request_context():
#    print(url_for('about'))

if __name__ == "__main__":
    app.run(debug=True)
