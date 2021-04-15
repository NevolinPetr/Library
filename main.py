from data import db_session
from data.books import Book
from data.genres import Genre
from data.users import User
from flask import Flask, render_template, redirect
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from forms.book import BookForm
from forms.login import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/library.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    books = db_sess.query(Book)
    return render_template("index.html", books=books)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
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
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/book',  methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = Book()
        book.title = form.title.data
        book.author = form.author.data
        genre = db_sess.query(Genre).filter(Genre.title == form.genre.data).first()
        if not genre:
            new_genre = Genre(title=form.genre.data)
            db_sess.add(new_genre)
            db_sess.commit()
            genre = db_sess.query(Genre).filter(Genre.title == form.genre.data).first()
        book.genre = genre
        book.created_date = form.created_date.data
        book.annotation = form.annotation.data
        book.img_file = form.img_file.data.filename
        form.img_file.data.save(f'static/img/{form.img_file.data.filename}')
        book.text_file = form.text_file.data.filename
        form.text_file.data.save(f'static/text/{form.text_file.data.filename}')
        genre.book.append(book)
        db_sess.merge(genre)
        db_sess.commit()
        return redirect('/')
    return render_template('book.html', title='Добавление книги', form=form)


def main():
    db_session.global_init("db/library.db")
    app.run()


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
