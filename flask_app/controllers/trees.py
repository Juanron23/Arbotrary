from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    recipes = Recipe.get_all_recipes()
    user = User.get_user(data)
    return render_template("dashboard.html", user=user, recipes = recipes)


@app.route("/users/create", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect('/dashboard')
    valid = Recipe.validate_recipe(request.form)
    if valid:
        data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30' : request.form['under_30'],
        'user_id' : session['user_id']
        }
        recipe = Recipe.create_recipe(data)
#        return redirect(f'/show/{recipe}')
    return  redirect("/show_recipes")

@app.route("/show_recipes")
def new_recipe():
    return render_template("new_recipe.html")

@app.route('/show/<int:user_id>')
def show_new_recipe():
    return render_template("show.html")


@app.route("/recipe/<int:recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id):
    data = {
    'name': request.form['name'],
    'description': request.form['description'],
    'instructions': request.form['instructions'],
    'under_30' : request.form['under_30'],
    'id' : recipe_id
    }
    Recipe.update(data)
    return redirect(f'/recipes/{recipe_id}/edit')


@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    return render_template('edit.html', recipe = Recipe.get_recipe(data))


@app.route('/recipes/<int:recipe_id>/view')
def view_instruction(recipe_id):
    data = {
        'id': recipe_id
    }
    return render_template('view_instructions.html', recipe = Recipe.get_recipe(data))


@app.route("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    data={
        "id": recipe_id
    }

    Recipe.delete(data)
    return redirect('/dashboard')
