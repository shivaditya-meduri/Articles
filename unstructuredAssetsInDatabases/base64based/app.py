import base64
import os
import uuid

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# — Configuration —
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'files.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# — Model —
class FileRecord(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    data = Column(Text, nullable=False)       # base64 string
    description = Column(String, default='')

Base.metadata.create_all(engine)

# — App setup —
app = Flask(__name__)

# — Routes —
@app.route('/')
def index():
    session = Session()
    files = session.query(FileRecord).all()
    session.close()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    upload = request.files.get('file')
    desc   = request.form.get('description', '')

    if not upload:
        return redirect(url_for('index'))

    raw = upload.read()
    b64  = base64.b64encode(raw).decode('ascii')
    rec  = FileRecord(
        filename=upload.filename,
        mimetype=upload.mimetype,
        data=b64,
        description=desc
    )

    session = Session()
    session.add(rec)
    session.commit()
    session.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
