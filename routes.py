from app import app, db
from flask import render_template, url_for, flash, redirect, request, render_template, request, send_file, Flask, render_template, jsonify, Response
from forms import RegistrationForm, LoginForm, SubmissionForm
from models import User, Submission
from flask_login import login_user, current_user, logout_user, login_required
import os, shutil, time
from werkzeug.utils import secure_filename
from utils import allowed_file, evaluate_submission
import subprocess
import threading
from threading import Thread
import json


progress = 0
status_message = "Booting Script..."

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password here in production!
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            # For security, implement password hashing!
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    submissions = Submission.query.filter_by(author=current_user)
    return render_template('dashboard.html', title='Dashboard', submissions=submissions)

@app.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmissionForm()
    if form.validate_on_submit():
        if form.data_file.data and allowed_file(form.data_file.data.filename):
            filename = secure_filename(form.data_file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.data_file.data.save(file_path)
            # Evaluate the submission
            evaluation_result = evaluate_submission(file_path)
            # Save submission to the database
            submission = Submission(data_file=filename, evaluation_result=evaluation_result, author=current_user)
            db.session.add(submission)
            db.session.commit()
            flash('Submission successful!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload.html', title='Submit Prediction', form=form)

@app.route("/submission/<int:submission_id>")
@login_required
def submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    if submission.author != current_user:
        abort(403)
    return render_template('submission.html', title='Submission Detail', submission=submission)

@app.route("/data")
def data():
    return render_template('data.html', title='Data')

@app.route("/challenge3", methods=['GET', 'POST'])
def challenge3():
    return render_template("challenge3.html")

@app.route("/run_script", methods=["POST"])
def run_script():
    global progress, status_message

    # Reset progress and status message
    progress = 0
    status_message = "Starting Script..."

    # Get file and form data from the request
    file = request.files.get('file')
    organism = request.form.get('organism')
    platform = request.form.get('platform')
    library_preparation = request.form.get('library_preparation')
    tool = request.form.get('tool')  # Default to 'your_tool' if not providedor
    data_category = request.form.get('data_category')  # Default to 'NA' if not provided

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Run the script in a separate thread with the additional parameters
    thread = Thread(target=run_script_process, args=(file_path, organism, platform, library_preparation, tool, data_category))
    thread.start()

    return jsonify({"status": "Script started successfully!"})


def run_script_process(file_path, organism, platform, library_preparation, tool, data_category):
    global progress, status_message

    # Set initial status
    status_message = f"Processing for organism: {organism}, platform: {platform}, library: {library_preparation}, tool: {tool}, category: {data_category}"

    # Define the path to the script
    script_path = "lrgasp_event2_metrics/sqanti3_lrgasp.challenge3.py"

    # Run the script
    try:
        print('Script is Running with parameters:', 'org:', organism, ' platform:', platform, ' Lib prep:',library_preparation, ' Tool name:' ,tool, ' Data Cat:',data_category)
        process = subprocess.Popen(
            ['python', script_path, file_path, organism, platform, library_preparation, tool, data_category],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line.strip())
            if 'PROGRESS:' in line:
                progress = int(line.strip().split('PROGRESS:')[1])
                print(f"Progress updated to {progress}%")
            elif 'STATUS:' in line:
                status_message = line.strip().split('STATUS:')[1].strip()
                print(f"Status message updated to: {status_message}")

        process.wait()
        progress = 100
        status_message = 'Script Finished'

        # Move the generated report
        source = "sqanti_results/rna_Evaluation_report.html"
        destination = "lrgasp_platform/static/report.html"
        shutil.move(source, destination)

    except Exception as e:
        print(f"Error running script: {e}")
        status_message = "Error running script"
        progress = 100  # Ensure progress reaches 100 on error


@app.route("/progress_stream")
def progress_stream():
    """Stream progress updates to the client."""
    def generate():
        while True:
            global progress
            global status_message
            time.sleep(0.5)  # Check progress every 500ms
            data = json.dumps({'progress': progress, 'message': status_message})
            yield f"data: {data}\n\n"
            if progress >= 100:
                break
    return Response(generate(), mimetype="text/event-stream")



@app.route('/challenge3_results')
def challenge3_results():
    return render_template("show_report.html")



if __name__ == '__main__':
    app.run(debug=True)