from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, new_name):
        if not new_name:
            raise ValueError("Author requires a name")
        if db.session.query(Author.id).filter(new_name == Author.name).first() is not None:
            raise ValueError("Duplicate author name.")
        return new_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, new_phone_number):
        if not new_phone_number.isdigit() or len(new_phone_number) != 10:
            raise ValueError("Phone numbers must be 10 digits.")
        return new_phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, new_content):
        if len(new_content) < 250:
            raise ValueError('Post content must be at least 250 characters long')
        return new_content 
        
    @validates('summary')
    def validate_summary(self, key, new_summary):
        if len(new_summary) > 250:
            raise ValueError('Post summary cannot be more than 250 characters long')
        return new_summary
    
    @validates('category')
    def validate_category(self, key, new_category):
        if new_category not in ('Fiction', 'Non-Fiction'):
            raise ValueError('Post category must be either Fiction or Non-Fiction')
        return new_category
    
    @validates('title')
    def validate_title(self, key, new_title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in new_title for keyword in clickbait_keywords):
                raise ValueError('Post title must contain clickbait keywords')
        return new_title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
