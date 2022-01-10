from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymssql, os

#pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
'''
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(pjdir, 'data.sqlite')#建立資料庫
    '''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://username:Password@server/database'
db = SQLAlchemy(app)

class Todo1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.String(20))
    name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(50))
    article = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_change = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        IP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        task_name = request.form['name']
        task_title = request.form['title']
        task_article = request.form['article']
        new_task1 = Todo1(IP=IP,name=task_name,title=task_title,article=task_article)
        try:
            db.session.add(new_task1)
            db.session.commit()
            return redirect('/')
        except:
            return '出現錯誤了，請返回上一頁。'

    else:
        tasks = Todo1.query.order_by(Todo1.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo1.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '出現錯誤了，請返回上一頁。'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo1.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.title = request.form['title']
        task.article = request.form['article']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return '出現錯誤了，請返回上一頁。'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,host='0.0.0.0' ,port=8888)
