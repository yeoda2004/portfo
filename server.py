'''
set FLASK_APP=server
set FLASK_ENV=development
flask run
'''
from flask import Flask, render_template, send_from_directory, url_for, request,redirect
import os
import csv

app = Flask(__name__)

@app.route("/")
def index_html():
    return render_template('index.html')


@app.route("/<string:page_name>")
def htmp_pg(page_name):
    return render_template(page_name)


@app.route("/submit_form", methods=['POST', 'GET'])
def submit_form():
    error = None
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            return render_template('/thank_you.html', message=data.get('email'))
        except:
            return f"Something went wrong with the database"
    else:
        return render_template("submit_error.html", message=f"something went wrong")
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    # return render_template('login.html', error=error)

####
def write_to_file(data):
    email = data.get('email','None')
    subject =data.get('subject','None')
    message =data.get('message','None')
    with open('database.txt',mode='a') as database:
        file = database.writelines(f"{email},{subject},{message}")

def write_to_csv(data):

    email = data.get('email','None')
    subject =data.get('subject','None')
    message =data.get('message','None')
    with open('database.csv',newline='', mode='a') as database:
        if database.tell() == 0:
            fieldnames = ['email', 'subject','message']
            writer = csv.DictWriter(database, fieldnames=fieldnames)
            writer.writeheader()
        csv_writer = csv.writer(database,delimiter=',', quotechar="'",quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

if __name__ == '__main__':
   app.run(debug = True)
