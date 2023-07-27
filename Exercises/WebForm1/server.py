from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('form1copy.html')

@app.route('/submit', methods=['POST'])
def calculate():
    return f'Hello {request.form["Name"]}. Your email is {request.form["Email"]},\
        Your Password is {request.form["Password"]}'

app.run(debug=True)