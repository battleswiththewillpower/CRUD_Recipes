from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    data ={
        "id":id
    }
    return render_template('editrecipe.html', recipe=Recipe.get_one(data)) 


@app.route('/recipe/select/<int:id>')
def select_recipe(id):
    data ={
        "id":id
    }

    user_data={
        'id':session['user_id']

    }
    return render_template('display-recipe.html', recipe=Recipe.get_one(data),user=User.get_one(user_data)) 


@app.route('/recipe/update/<int:id>', methods=['POST'])
def update(id):
    update_data={
            'id': id,
            'name':request.form['name'],
            'description':request.form['description'],
            'instructions':request.form['instructions'],
            'date_made':request.form['date_made'],
            'user_id':session['user_id']
    }

    if 'choice' not in request.form:
        update_data['choice'] = 0
    else:
        update_data['choice'] = request.form['choice']

    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        
        return redirect('/recipe/new')
    
    # recipe = Recipe.get_one(update_data['id'])
    Recipe.update(update_data)
    return redirect('/success')


@app.route('/recipe/new')
def new():
    return render_template("addrecipe.html")

@app.route('/recipe/create', methods=['POST'])
def create():

    data={
            'name':request.form['name'],
            'description':request.form['description'],
            'instructions':request.form['instructions'],
            'date_made':request.form['date_made'],
            'user_id':session['user_id']
    }

    if 'choice' not in request.form:
        data['choice'] = 0
    else:
        data['choice'] = request.form['choice']

    # if there are errors:
    # We call the staticmethod on Burger model to validate
    if 'user_id' not in session:
        return redirect('/recipe/new')
    if not Recipe.validate_recipe(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/recipe/new')
    # else no errors:
    # Burger.save(request.form)
    # print(request.form)
    Recipe.create(data)
    return redirect('/success')


@app.route('/recipe/destroy/<int:id>')
def destroy(id):
    data ={
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/success')


if __name__=="__main__":
    app.run(debug=True)


    # combine the form with the usdr ID from session