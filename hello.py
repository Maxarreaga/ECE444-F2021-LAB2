from flask import Flask, render_template, flash, session
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, ValidationError, Email


class NameForm(Form):

    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your UofT Email address?',
                        validators=[Required(), Email()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    utoronto = True
    name_form = NameForm()
    if name_form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        name = name_form.name.data
        name_form.name.data = ''
        email = name_form.email.data
        name_form.email.data = ''
        if old_name != name:
            print("changed name")
            flash('Looks like you have changed your name!')
        session['name'] = name
        if old_email != email:
            print("changed email")
            flash('Looks like you have changed your email!')
        session['email'] = email

        if "utoronto" not in email:
            utoronto = False

    return render_template('index.html', name_form=name_form, name=name, email=email, utoronto=utoronto)


@app.route('/user/<name>')
def user(name):
    # the response document we give the user
    return render_template('user.html', name=name, current_time=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)
