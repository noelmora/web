import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Usar variable de entorno DATABASE_URL configurada en Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://user:pass@localhost:5432/dbname'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.before_first_request
def create_db():
    db.create_all()

@app.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', records=records)

@app.route('/record/<int:id>')
def detail(id):
    record = Record.query.get_or_404(id)
    return render_template('detail.html', record=record)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        new = Record(
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', action='Add', record=None)

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    record = Record.query.get_or_404(id)
    if request.method == 'POST':
        record.name = request.form['name']
        record.description = request.form['description']
        db.session.commit()
        return redirect(url_for('detail', id=record.id))
    return render_template('form.html', action='Edit', record=record)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))