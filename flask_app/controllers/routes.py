from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)


@app.route('/')
def log_reg ():
    if 'user_id' in session:
        return redirect('/success')
    return render_template('index.html')



@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }

    return render_template('dashboard.html', user=User.get_one(data), recipes = Recipe.get_all())


# @app.route('/dojo/<int:id>')
# def dojo_show(id):
#     context = {
#         "dojo": dojo.Dojo.get_one_ninjas({'id': id})
#     }
#     return render_template("dojo-show.html", **context)


if __name__=="__main__":
    app.run(debug=True)