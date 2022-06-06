from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module

# install bcrypt   pipenv install werkzeug==2.0.3 flask==2.0.3 flask-bcrypt



# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Naming convenction to use for mutiple projects. just change the string name to the proper scema
DATABASE = 'Recipes_mydb'

# model the class after the friend table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.choice = data['choice']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create(cls, data:dict):
        #query the string
        query = "INSERT INTO recipes (name, description, choice, instructions, date_made, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(choice)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(user_id)s);"
        #contact the database
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    #want to be able to update whichever recipe we select by id thro the DB since each id is unique to the recipe
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # class method to get all the emails fromt the database
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes


    # @classmethod
    # def get_users_and_recipes(cls,data):
    #     query = "SELECT * FROM recipes WHERE id = %(id)s;"
    #     result = connectToMySQL(DATABASE).query_db(query,data)

    #     return 


    #edit the recipe and update the information
    @classmethod
    def update(cls, data):
        # make sure theres no spaces inbetwwen each comma
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,choice=%(choice)s,instructions=%(instructions)s,date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        # if(data['choice'] == 'False'):
        #     #no
        #     data['choice'] = 0
        # else:
        #     data['choice'] = 1

        # CHECKBOX 1 FOR YES 0 FOR NO

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    # PASS IN VALIDATION FOR NEW RECIPE FORM
    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 2 characters!")
        if len(recipe['description']) < 2:
            is_valid = False
            flash("I told you at least 2 characters!")
        if recipe['instructions'] == '':
            is_valid = False
            flash("Name must be at least 2 characters!")
        if not recipe['date_made']:
            is_valid = False
            flash("Add Date!")
        return is_valid