from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from models import db, Topic, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db.init_app(app)

admin_username = 'admin'
admin_password = 'password'  # Замените на более безопасный пароль

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_topic')
def select_topic():
    topics = Topic.query.all()
    return render_template('select_topic.html', topics=topics)

@app.route('/test/<int:topic_id>')
def test(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('test.html', questions=topic.questions, topic=topic, enumerate=enumerate)

@app.route('/result/<int:topic_id>', methods=['POST'])
def result(topic_id):
    score = 0
    topic = Topic.query.get_or_404(topic_id)
    for i, question in enumerate(topic.questions):
        user_answer = request.form.get(f"question-{i}")
        if user_answer == question.answer:
            score += 1
    return render_template('result.html', score=score, total=len(topic.questions))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' in session:
        topics = Topic.query.all()
        return render_template('admin.html', topics=topics)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if 'logged_in' not in session:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        topic_name = request.form.get('topic')
        new_topic_name = request.form.get('new_topic')

        if topic_name == 'new' and not new_topic_name:
            topics = Topic.query.all()
            return render_template('add_question.html', topics=topics, error="New topic name is required")
        
        if topic_name == 'new':
            topic_name = new_topic_name
        
        question_text = request.form['question']
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        choice3 = request.form['choice3']
        choice4 = request.form['choice4']
        answer = request.form['answer']
        
        topic = Topic.query.filter_by(name=topic_name).first()
        if not topic:
            topic = Topic(name=topic_name)
            db.session.add(topic)
            db.session.commit()
        
        question = Question(
            question_text=question_text,
            choice1=choice1,
            choice2=choice2,
            choice3=choice3,
            choice4=choice4,
            answer=answer,
            topic=topic
        )
        db.session.add(question)
        db.session.commit()
        
        return redirect(url_for('admin'))
    
    topics = Topic.query.all()
    return render_template('add_question.html', topics=topics)

@app.route('/delete_question/<int:question_id>')
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    topic_id = question.topic_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_topic/<int:topic_id>')
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/rename_topic/<int:topic_id>', methods=['GET', 'POST'])
def rename_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if request.method == 'POST':
        new_name = request.form['new_name']
        if new_name:
            topic.name = new_name
            db.session.commit()
            return redirect(url_for('admin'))
    return render_template('rename_topic.html', topic=topic)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
