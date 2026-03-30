from flask import Flask,jsonify,request,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__) 


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://stephen:password@localhost:5432/todoapp"

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "todos"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
    onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "completed": self.completed,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        }


@app.route('/')
def index():
    return jsonify({
        "message":"welcome to simple ToDo List API",
        "status":"online",
        "version":"1.0.0",
        "created_by":"s.k mulwa",
        "inspected_by":"Slyvester Musyoki"
    })

@app.route('/todo', methods=['POST'])
def add():
    req= request.get_json(silent=True)
    title = req.get('title')
    description = req.get('description')
    new_todo = Todo(title=title, description=description)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict())


@app.route('/todo', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())

@app.route('/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    req = request.get_json(silent=True)
    todo.title = req.get('title', todo.title)
    todo.description = req.get('description', todo.description)
    todo.completed = req.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"})
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict())

@app.route('/todo/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    task = Task.query.get_or_404(todo_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({ ... }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    total = Todo.query.count()
    completed = Todo.query.filter_by(completed=True).count()
    pending = total - completed
    
    rate = round((completed / total) * 100, 2) if total > 0 else 0
    
    return {
        "total_todos": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": rate
    }, 200

 



if __name__ == '__ main_':
    db.create_all()
    app.run(debug=True)
