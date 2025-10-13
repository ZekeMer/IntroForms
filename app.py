from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

#secure connection between frontend and backend of application
app.secret_key = 'top-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    quan = db.Column(db.Integer, nullable = False)
    comments = db.Column(db.Text)
    rel = db.Column(db.String(50), nullable=False)
    accommodations = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

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
        
        #new profile database
        try:
            new_profile = Profile(name=name, email=email, quan=int(quan), comments = comments, rel=rel, accommodations=accommodations)
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your profile. Please try again."
            return render_template('profileForm.html', error=error)
        
        return render_template('profileSuccess.html', name = name, email = email, quan = quan, comments = comments, rel = rel, accommodations = accommodations)

    return render_template('profileForm.html')

#new route

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating', '').strip()
        feedback = request.form.get('feedback', '').strip()
    
        if not rating:
            error = "Please provide a rating"
            return render_template('feedbackForm.html', error = error)
        
        #new feedback in database
        try:
            #Is there something wrong with this comment_text variable?
            new_feedback = Feedback(rating=int(rating), comment = feedback)
            
            db.session.add(new_feedback)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your feedback. Please try again."
            return render_template('feedbackForm.html', error=error)

        return render_template('feedbackSuccess.html', rating = rating, feedback = feedback)

    return render_template('feedbackForm.html')

@app.route('/admin/profiles')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('admin_profiles.html', profiles = profiles)

@app.route('/admin/feedback')
def admin_feedback():
    feedbacks = Feedback.query.all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

#Intro SQL via Flask and adding a filter. Rating for all feedback = 1.

@app.route('/admin/feedback/rating_1')
def admin_feedback_rating_1():
    feedbacks = Feedback.query.filter_by(rating=1).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)


#Less than or = to 3, feedback isn't blank or a string of space.

@app.route('/admin/feedback/bad_review')
def admin_feedback_bad_review():
    feedbacks = Feedback.query.filter(Feedback.rating <= 3, Feedback.comment.isnot(None), Feedback.comment != "").all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

#Filtering by sibling amount. The relationship variable "rel" needs to be set to sibling & the amount of siblings should be greater than 5.

@app.route('/admin/profiles/siblings')
def admin_profiles_siblings():
    profiles = Profile.query.filter(Profile.rel == "sibling", Profile.quan > 5).all()
    return render_template('admin_profiles.html', profiles = profiles)

