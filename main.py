from flask import Flask, render_template, redirect, request, url_for
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from bs4 import BeautifulSoup
import lxml
from smtplib import SMTP
import envutils



email = "nikoskorompoos@gmail.com"
password = os.environ['password']
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    message = CKEditorField("Your message here", validators=[DataRequired()])
    submit = SubmitField("Submit")
# url_for(r'static\images\artwork')
listaphotos = os.listdir(r'C:\Users\User\PycharmProject\tara_tattoo\static\images\artwork')
photo_urls = ["static/images/artwork/" + photo_name for photo_name in listaphotos]
print(photo_urls)
app = Flask(__name__)
app.secret_key = "kleidi"
ckeditor = CKEditor(app)
Bootstrap(app)

@app.route('/index')
@app.route('/')
def homepage():
    return render_template('index.html', photos=photo_urls)


@app.route('/<int:num>')
def art_piece(num):
    photo_url = photo_urls[num-1]
    return render_template('art_piece.html', photo_url=photo_url)

@app.route('/contact', methods=['GET', 'POST'])
def contact_me():
    forma = ContactForm()
    if forma.validate_on_submit():
        name = request.form.get('name'),
        usermail = request.form.get('email')
        message = BeautifulSoup(request.form.get('message'), "lxml").text
        complete_message = f"Subject:Contact From Site\n\n A contact was made by{name} with {usermail}, the message is {message}"
        connection =  SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs="giannisloleus@gmail.com", msg=complete_message)
        return redirect(url_for('homepage'))
    return render_template('coontact.html', form=forma)


if __name__ == "__main__":
    app.run()
