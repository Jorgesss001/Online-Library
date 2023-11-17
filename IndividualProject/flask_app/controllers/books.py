from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.book import Book


@app.route('/add/book')
def addBook():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('addBook.html',loggedUser = User.get_user_by_id(loggedUserData))


@app.route('/create/book', methods = ['POST'])
def createBook():
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'releaseDate': request.form['releaseDate'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }   
    Book.create_book(data)
    return redirect('/')


@app.route('/books/<int:id>')
def viewBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    loggedUser = User.get_user_by_id(data)
    book = Book.get_book_by_id(data)
    return render_template('book.html', book = book, loggedUser = loggedUser)

@app.route('/books/edit/<int:id>')
def editBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    loggedUser = User.get_user_by_id(data)
    book = Book.get_book_by_id(data)
    if loggedUser['id'] == book['user_id']:
        return render_template('editBook.html', book = book, loggedUser = loggedUser)
    return redirect(request.referrer)
   

@app.route('/books/delete/<int:id>')
def deleteBook(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    loggedUser = User.get_user_by_id(data)
    book = Book.get_book_by_id(data)
    if loggedUser['id'] == book['user_id']:
        Book.delete_book(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/edit/book/<int:id>', methods = ['POST'])
def updateBook(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'releaseDate': request.form['releaseDate'],
        'description': request.form['description'],
        'user_id': session['user_id'],
        'book_id': id
    }  
    loggedUser = User.get_user_by_id(data)
    book = Book.get_book_by_id(data) 
    if loggedUser['id'] == book['user_id']:
        Book.update_book(data)
        flash('Update succesfull!', 'updateDone')
        return redirect(request.referrer)
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    usersWhoLikesThisBook = Book.getUserWhoLikedBooks(data)
    if session['user_id'] not in usersWhoLikesThisBook:
        Book.like(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def unlike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    usersWhoLikesThisBook = Book.getUserWhoLikedBooks(data)
    if session['user_id'] in usersWhoLikesThisBook:
        Book.unlike(data)
    return redirect(request.referrer)
