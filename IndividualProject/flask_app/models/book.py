from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
# create a regular expression object that we'll use later   
class Book:
    db_name = 'indproject'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.releaseDate = data['releaseDate']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database


    @classmethod
    def get_book_by_id(cls, data):
        query = "Select * from books left join users on books.user_id = users.id WHERE books.id = %(book_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def getUserWhoLikedBooks(cls, data):
        query = "SELECT likes.user_id as id from likes WHERE book_id = %(book_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likes = []
        if results:
            for like in results:
                likes.append( like['id'] )
            return likes
        return likes

    @classmethod
    def get_all(cls):
        query = "SELECT * from books left join users on books.user_id=users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of friends
        books = []
        # Iterate over the db results and create instances of friends with cls.
        if results:
            for book in results:
                books.append( book )
            return books
        return books
    
    # NOT NEEDED
    # @classmethod
    # def get_all_user_post(cls, data):
    #     query = "SELECT * FROM posts LEFT JOIN users on posts.user_id = users.id WHERE posts.user_id = %(user_id)s;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     # Create an empty list to append ou instances of friends
    #     posts = []
    #     # Iterate over the db results and create instances of fiends with cls.
    #     if results:
    #         for post in results:
    #             posts.append( post )
    #         return posts
    #     return posts
    
    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (title, author, releaseDate, description,  user_id) VALUES ( %(title)s,%(author)s, %(releaseDate)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, book_id) VALUES ( %(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND book_id = %(book_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_book(cls, data):
        query = "UPDATE books SET title = %(title)s, author = %(author)s, releaseDate = %(releaseDate)s, description = %(description)s WHERE id = %(book_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_book(cls, data):
        query = "DELETE FROM books WHERE id = %(book_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # @classmethod
    # def delete_all_user_posts(cls, data):
    #     query = "DELETE FROM posts WHERE user_id = %(user_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_book(r):
        is_valid = True
        # test whether a field matches the pattern
        
        if len(r['title'])< 3:
            flash('Title must be more than 3 characters', 'title')
            is_valid = False
        if len(r['author'])< 3:
            flash('Author must be more than 3 characters', 'author')
            is_valid = False
        if not r['releaseDate']:
            flash('Created date is required', 'releaseDate')
            is_valid= False
        if len(r['description'])< 3:
            flash('Description must be more than 3 characters', 'description')
            is_valid = False
        return is_valid