# src/library_management.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Library {self.name}>'
```

```python
# tests/test_library_management.py

from unittest import TestCase
from src.library_management import Library, db

class TestLibraryManagement(TestCase):

    def setUp(self):
        self.app = 'sqlite:///test.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_library_creation(self):
        new_library = Library(name='Test Library')
        db.session.add(new_library)
        db.session.commit()
        retrieved_library = Library.query.filter_by(name='Test Library').first()
        self.assertIsNotNone(retrieved_library)