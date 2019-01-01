from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    blogs = db.relationship("Blog", backref="user", lazy="dynamic")
    comment = db.relationship("Comments", backref="user", lazy ="dynamic")



    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)
    def __repr__(self):
        return f'User {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):
    '''
    defines the table instance of our blog table
    '''
    __tablename__= 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    Blog_post = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_blog(self):
        '''
        function to save blog
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_blogs(cls):
        '''
        function that clears all the blogs in the form after submission
        '''
        Blog.all_blogs.clear()

    @classmethod
    def get_blogs(cls,id):
        '''
        function that gets particular blogs when requested by date posted
        '''
        blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
        return blogs

class Comments(db.Model):
    '''
    comment class that create instance of comment
    '''
    __tablename__ = 'comment'

    #add columns
    id = db.Column(db. Integer, primary_key=True)
    comment_name = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def save_comment(self):
        '''
        save the comment per blog
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comment = Comments.query.order_by (Comments.date_posted.desc()).all()
        return comment

    @classmethod
    def delete_comment(cls,id):
        comment = Comments.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

class Subscriber(UserMixin, db.Model):
    __tablename__="subscribers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_subscribers(cls,id):
        return Subscriber.query.all()

    def __repr__(self):
       return f'User {self.email}'
