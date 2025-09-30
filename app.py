from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#secure connection between frontend and backend of application
app.secret_key = 'top-secret'

@app.route('/')
def index():
    return redirect(url_for('profile'))

@app.route('/profile', methods = ['GET', 'POST'])
def profile(): 
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        quan = request.form.get('quan', '').strip()
        comments = request.form.get('comments', '').strip()
        rel = request.form.get('rel', '').strip()
        #boolean value
        accommodations = request.form.get('accommodations') == 'yes'

        #Validation
        if not name or not email or not quan or not rel:
            errorMsg = "Please fill in all requred fields."
            return render_template('profileForm.html', error = errorMsg)
        
        return render_template('profileSuccess.html', name = name, email = email, quan = quan, comments = comments, rel = rel, accommodations = accommodations)

    return render_template('profileForm.html')
