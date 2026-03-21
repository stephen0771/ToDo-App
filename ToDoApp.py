from flask import Flask,jsonify,request,url_for
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

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    new_todo = Todo(title=title, description=description)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict(),201)

if __name__ == '__ main_':
    db.create_all()
    app.run(debug=True)
