from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re


class Tree:
    db = "login"
    def __init__(self, data):
        self.tree_id =data['tree_id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create_recipe(cls, form_data):
        query = "INSERT INTO trees(name, description, instructions, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s,%(user_id)s)"
        return connectToMySQL("login").query_db(query, form_data)

    @classmethod
    def get_all_recipes(cls):
        query= "SELECT * FROM trees"
        results = connectToMySQL("login").query_db(query)
        trees = []
        for row in results:
            trees.append(cls(row))
        return trees

    @classmethod
    def get_recipe(cls, data):
        query= "SELECT * FROM trees WHERE tree_id = %(id)s"
        results = connectToMySQL("login").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


#under you have WHERE tree_id = %(id)s" becuase you are updating youre recipe table with the
#  id of tree_id with the actual id the recipe created which is id
    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s WHERE tree_id = %(id)s"
        return connectToMySQL("login").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trees WHERE tree_id = %(id)s"
        return connectToMySQL("login").query_db(query, data)


    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("name must be at least 3 characters", "error")
            is_valid = False
        if len(data['description']) < 2:
            flash("must have description", "error")
            is_valid = False
        if len(data['instructions']) < 4:
            flash("Must have instructions", "error")
            is_valid = False
        if len(data['under_30']) < 2:
            flash("Must Select Yes or No", "error")
            is_valid = False

        return is_valid



#    @classmethod
#    def get_all_recipes_with_users(cls):
#        query = "SELECT * FROM trees LEFT JOIN users ON trees.user_id = user.id;"
#        trees = connectToMySQL("login").query_db(query)
#        results=[]
#       for recipe in trees:
#           data = {
#            'id' :data['id'],
#            'first_name': data['first_name'],
#           'last_name': data['last_name'],
#           'email': data['email'],
#           'password': data['password'],
#           'created_at': data['created_at'],
#           'updated_at': data['updated_at'],
#           }
#           one_recipe = cls(recipe)
#           one_recipe.creator = user.User(data)
#           results.append(one_recipe)
#       return results