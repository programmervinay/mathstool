from flask import Flask, render_template, request, redirect, session, jsonify
import random
import os
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# File to store progress
PROGRESS_FILE = "progress.json"

# Ensure progress file exists
if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'w') as file:
        json.dump({}, file)

# Load or save progress
def load_progress():
    with open(PROGRESS_FILE, 'r') as file:
        return json.load(file)

def save_progress(data):
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        
        progress = load_progress()
        if name not in progress:
            progress[name] = {"score": 0}
            save_progress(progress)
        return redirect('/select_table')
    return render_template('login.html')

@app.route('/select_table', methods=['GET', 'POST'])
def select_table():
    if request.method == 'POST':
        table = int(request.form['table'])
        session['table'] = table
        return redirect('/quiz')
    return render_template('select_table.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'name' not in session or 'table' not in session:
        return redirect('/')
    
    name = session['name']
    table = session['table']
    progress = load_progress()

    if request.method == 'POST':
        answer = int(request.form['answer'])
        correct_answer = session['question']['correct']
        if answer == correct_answer:
            progress[name]['score'] += 1
        else:
            progress[name]['score'] -= 1
        save_progress(progress)
        return redirect('/quiz')

    # Generate random question
    num = random.randint(1, 10)
    question = {
        "num1": table,
        "num2": num,
        "correct": table * num
    }
    session['question'] = question
    return render_template('quiz.html', question=question, score=progress[name]['score'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
