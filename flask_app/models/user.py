from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module

# install bcrypt   pipenv install werkzeug==2.0.3 flask==2.0.3 flask-bcrypt



# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Naming convenction to use for mutiple projects. just change the string name to the proper scema
DATABASE = 'Recipes_mydb'

# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    
    @classmethod
    def create_user(cls, data:dict):
        #query the string
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        #contact the database
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    #want to be able to update whichever user we select by id thro the DB since each id is unique to the user
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # class method to get all the emails fromt the database
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data) 


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])  

    @staticmethod
    def validate_user_login( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,user)
            if len(results) >= 1:
                flash("Email already taken.")
                is_valid=False 
        # test whether a field matches the pattern
        
        if len(user['first_name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters!")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("I told you at least 2 characters!")
        if len(user['password']) < 4:
            is_valid = False
            flash("4 characters or more!")
        if user['password'] != user['confirm']:
            flash("password don't match")
        return is_valid

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        user = cls(result[0])
        for row in result:
            recipe_data = {
                'id': row['recipes.id'],
                'name': row['name'],
                'description': row['description'],
                'choice': row['choice'],
                'instructions': row['instructions'],
                'date_made': row['date_made'],
                'user_id': row['user_id'],
                'created_at': row['recipes.created_at'],
                'updated_at': row['recipes.updated_at']
            }
            user.recipes.append(recipe.Recipe(recipe_data))
        return user


#         SELECT * FROM orders 
# JOIN items_orders ON orders.id = items_orders.order_id 
# JOIN items ON items.id = items_orders.item_id;