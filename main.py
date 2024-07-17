import wtforms.validators
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired
# import sqlite3
from flask_sqlalchemy import SQLAlchemy
from miscel import copyright_year
 
# db = sqlite3.connect('books_collection.db')
# cursor = db.cursor()
 
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
 
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
 
    def __repr__(self):
        return f'<Books {self.title}>'
 
 
class AddBookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired('Please enter a correct input for Book Name.'),
                                                     wtforms.validators.Length(min=3)])
    book_author = StringField('Book Author', validators=[DataRequired('Please enter a correct input for Book Name.'),
                                                         wtforms.validators.Length(min=3)])
    book_rating = FloatField('Rating', validators=[DataRequired('Please enter a correct input for Rating.'),
                                                   wtforms.validators.NumberRange(max=10)])
    # Optional - Best using with Flask-Bootstrap to make the button looks nice.  Otherwise, just use regular form's
    # button and manually adding bootstrap button style.
    add_book = SubmitField('Add Book')
 
 
class DeleteBookForm(FlaskForm):
    book_id_1 = IntegerField('Book ID', validators=[DataRequired('Please enter a correct input for Book ID.')])
    book_id_2 = IntegerField('Book ID', validators=[wtforms.validators.Optional()])
    book_id_3 = IntegerField('Book ID', validators=[wtforms.validators.Optional()])
 
 
class EditBookRating(FlaskForm):
    book_rating = FloatField('Rating', validators=[DataRequired('Please enter a correct input for Rating.'),
                                                   wtforms.validators.NumberRange(max=10)])
 
 
@app.route('/')
def home():
    books = Books.query.all()
    year = copyright_year()
    if books:
        return render_template('index.html', books=books, year=year)
    else:
        important_msg = 'There isn\'t a book in the library yet.'
        return render_template('index.html', important_msg=important_msg)
 
 
@app.route("/add", methods=['POST', 'GET'])
def add():
    form = AddBookForm()
    year = copyright_year()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_input_title = form.book_name.data
            found_book = Books.query.filter_by(title=current_input_title).first()
            if found_book:
                return redirect(url_for('found_title'))
            else:
                add_book = Books(title=form.book_name.data,
                                 author=form.book_author.data,
                                 rating=form.book_rating.data)
                db.session.add(add_book)
                db.session.commit()
                return redirect(url_for('home'))
    return render_template('add.html', form=form, year=year)
 
 
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    delete_form = DeleteBookForm()
    year = copyright_year()
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            book_id_1 = delete_form.book_id_1.data
            book_id_2 = delete_form.book_id_2.data
            book_id_3 = delete_form.book_id_3.data
            book_id_list = [book_id_1, book_id_2, book_id_3]
            for i in book_id_list:
                if i:
                    found_book = Books.query.filter_by(id=i).first()
                    if found_book:
                        delete_book = Books.query.get(i)
                        db.session.delete(delete_book)
                        db.session.commit()
                    else:
                        return redirect(url_for('book_id_not_found'))
            return redirect(url_for('home'))
    return render_template('delete.html', delete_form=delete_form, year=year)
 
 
@app.route('/delete/<int:book_id>')
def delete_a_single_book(book_id):
    book = Books.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
 
 
@app.route('/edit_rating/<int:book_id>', methods=['POST', 'GET'])
def edit_book_rating(book_id):
    edit_rating_form = EditBookRating()
    year = copyright_year()
    if request.method == 'POST':
        if edit_rating_form.validate_on_submit():
            book_rating_to_edit = Books.query.filter_by(id=book_id).first()
            book_rating_to_edit.rating = edit_rating_form.book_rating.data
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit_rating.html', edit_rating_form=edit_rating_form, year=year, book_id=book_id)
 
 
@app.route('/success')
def success():
    return '<h1>Adding book successfully!</h1>'
 
 
@app.route('/found_title')
def found_title():
    return '<h1>This book had been added to the library!<h1>'
 
 
@app.route('/book_id_not_found')
def book_id_not_found():
    return '<h1>The id of a book you\'re trying to look up isn\'t available!</h1>'
 
 
@app.route('/base.html')
def base():
    year = copyright_year()
    return render_template('base.html', year=year)
 
 
if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(host='0.0.0.0', debug=True, port=5000)