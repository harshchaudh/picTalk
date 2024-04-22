from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Dummy database (replace with a real database in production)
users = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signUp', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    
    if username in users:
        return "Username already exists! Please choose another."
    
    users[username] = password
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
