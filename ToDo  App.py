from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
ToDoApp =__name__
app = Flask(ToDoApp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLITE:///todo.db'
db = SQLAlchemy(app)
class ToDo(db.Model):
    id = db.column(db.integer,primary_key=True)
    title = db.column(db.string(100), nullable=False)
    description = db.column(db.string(200), nullable=False)
    def __repr__(self):
        return f'<ToDo {self.id}>'
    @app.route('/')
    def index():
        todos = ToDo.query.all()
        return render_template('index.html', todos=todos)
    @app.route('/add', methods=['POST'])
    def add():
        title = request.form['title']
        description = request.form['description']
        new_todo = ToDo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for())
        @app.route('/delete/<int:id>')
        def delete(id):
            ToDo.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('index'))
if __name__ == '__ main_':
    db.create_all()
    app.run(debug=True)

    