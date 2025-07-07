import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# — Configuration —
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db_path = os.path.join(BASE_DIR, 'files.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# — Model —
class FileRecord(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    description = Column(String)

Base.metadata.create_all(engine)

# — App setup —
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# — Routes —
@app.route('/')
def index():
    session = Session()
    files = session.query(FileRecord).all()
    session.close()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    desc = request.form.get('description', '')
    if not f:
        return redirect(url_for('index'))

    ext = os.path.splitext(f.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    f.save(save_path)

    session = Session()
    rec = FileRecord(filename=unique_name, description=desc)
    session.add(rec)
    session.commit()
    session.close()

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)