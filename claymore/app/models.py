####################################################
####The Data Schema for the application ############
####################################################

from .exts import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user


class User(db.Model,UserMixin):

    __tablename__='users'
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    password=db.Column(db.Text,nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
    
    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def create(cls,username,email,password):
        new_user=cls(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()


    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(25),nullable=False)
    body=db.Column(db.Text(),nullable=False)
    comments=db.relationship('Comment',backref='post',lazy=True)
    user_id=db.Column(db.Integer(),db.ForeignKey('users.id'))




    @classmethod
    def create(cls,title,body,password):
        '''Create a new post and save it to db'''
        new_post=cls(title=title,body=body,author=current_user)
        db.session.add(new_post)
        db.session.commit()

        return new_post

    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Delete a post '''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        ''' get all posts '''
        return cls.query.all()


    @classmethod
    def get_by_id(cls,id):
        '''Get a post by its ID '''
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_title(cls,title):
        '''Get a post by title '''
        return cls.query.filter_by(title=title).first()


class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'))

    def save(self):
        '''Save a comment'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Delete a comment '''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        '''Get all comments'''
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        '''Get a comment by its id '''
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_title(title):
        return Comment.query.filter_by(title=title).first()


    @classmethod
    def create(cls,body):
        '''Create a new post and save it to db'''
        new_comment=cls(body=body,author=current_user)
        db.session.add(new_comment)
        db.session.commit()

        return new_comment


