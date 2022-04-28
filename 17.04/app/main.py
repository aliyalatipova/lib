from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.price = form.price.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# добавляет в столбец бд, на самом деле нет(
@app.route('/news_like/<int:id_news>/<int:id_user>', methods=['GET', 'POST'])
@login_required
def news_like(id_news, id_user):
    # print(id_news, id_user)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id_user).first()
    if user:
        print(type(user.liked_news))
        # return str(user.liked_news)
        if user.liked_news.split()[-1] != str(id_news):
            user.liked_news = user.liked_news + ' ' + str(id_news)
        print('l', user.liked_news)
        db_sess.commit()
        user_id = user.id
        return redirect("/")
    else:
        abort(404)
        return redirect("/")


# как дизлайкать
@app.route('/dislike/<int:id_news>/<int:id_user>', methods=['GET', 'POST'])
@login_required
def dislike(id_news, id_user):
    # print(id_news, id_user)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id_user).first()
    if user:
        print(type(user.liked_news))
        # return str(user.liked_news)
        if str(id_news) in user.liked_news.split():
            another = list()
            for new in user.liked_news.split():
                if new != str(id_news):
                    another.append(new)
            user.liked_news = ' '.join(another)
        print('l', user.liked_news)
        db_sess.commit()
        return redirect("/")
    else:
        abort(404)
        return redirect("/")


# дизлайкать если человек находился в понравившихся
@app.route('/dislike_from/<int:id_news>/<int:id_user>', methods=['GET', 'POST'])
@login_required
def dislike_from(id_news, id_user):
    # print(id_news, id_user)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id_user).first()
    if user:
        print(type(user.liked_news))
        # return str(user.liked_news)
        if str(id_news) in user.liked_news.split():
            another = list()
            for new in user.liked_news.split():
                if new != str(id_news):
                    another.append(new)
            user.liked_news = ' '.join(another)
        print('l', user.liked_news)
        db_sess.commit()
        return redirect(f"/news_liked_by/{id_user}")
    else:
        abort(404)
        return redirect("/")


@app.route('/my_news1', methods=['GET', 'POST'])
def my_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("my_news.html", news=news)


@app.route('/news_liked_by/<int:id_user>', methods=['GET', 'POST'])
def news_liked_by(id_user):
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    user = db_sess.query(User).filter(User.id == id_user).first()
    liked = user.liked_news
    print(liked)
    liked_list = liked.split()
    liked_list = [int(x) for x in liked_list]
    print(liked_list)
    return render_template("liked_news.html", liked_list=liked_list, news=news)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.price.data = news.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    # news = db_sess.query(News).filter((News.user == current_user))
    # else:
    news = db_sess.query(News)

    if request.method == 'POST':
         # Передайте значение имени соответствующего поля ввода формы
        # year = request.form.get('year')
        find = request.form.get('find1')
        print(find)
        news_need = list()
        for n in news:
            if find in n.title:
                print(n.title)
                news_need.append(n.id)
        print(news_need)
    else:
        news_need = [n.id for n in news]


    return render_template("index.html", news=news, news_need=news_need)


# чтож будет попытка
# @app.route("/authorized/<int:id_user>", methods=['GET', 'POST'])
# def authorized(id_user):
    #db_sess = db_session.create_session()
    #news = db_sess.query(News)
    #user = db_sess.query(User).filter(User.id == id_user).first()
    #liked = user.liked_news
    #print(liked)
    #liked_list = liked.split()
    #liked_list = [int(x) for x in liked_list]
    # print(liked_list)
    #return render_template("authorized.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user_id = user.id
            print(user_id)
            # return redirect(f"/authorized/{str(user_id)}")
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
