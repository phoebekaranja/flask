from flask import render_template,request,redirect,url_for,abort
from ..models import User, Blog, Role, Comments
from . import main
from flask_login import login_required,current_user
from .forms import UpdateProfile, BlogForm,CommentForm,SubscriberForm
from .. import db,photos
import markdown2

@main.route('/')
def index():
    '''
    view root page function that returns the index page
    '''
    title = 'Home - Welcome to The Best Blog Site Worldwide You Think of It We help share It.'
    blog = Blog.query.filter_by(category='Personal_Blog')
    blogone = Blog.query.filter_by(category='Institutional')
    return render_template('index.html',title = title, blog = blog, blogone = blogone)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        Blog_post = form.content.data
        new_blog = Blog(Blog_post=Blog_post,category= form.category.data,user=current_user)
        new_blog.save_blog()
        return redirect(url_for('main.view_blog'))
    return render_template('blog.html',form = form)

@main.route('/blog/new/view')
def view_blog():
    blog = Blog.query.filter_by(category='Personal_Blog')
    blogone = Blog.query.filter_by(category='Institutional')
    return render_template('index.html',blog=blog,blogone=blogone)


@main.route('/blog/new/comment/<int:id>',methods = ['GET','POST'])
def new_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comments(comment_name = form.comment_name.data,user=current_user, blog_id =id)
        new_comment.save_comment()
        return redirect(url_for('.index'))
    return render_template('new_comment.html',form = form)

@main.route('/blog/new/comment/<int:id>/view')
def view_comments(id):
    comment = Comments.query.filter_by(blog_id = id)
    return render_template('comment.html',comment = comment)

@main.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    if current_user.is_authenticated:
        comment = Comments.query.filter_by(id = id).first()
        # comment.delete_comment()
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('comment.html')



#routing for subscribers
@main.route('/subscribe', methods=['GET','POST'])
def subscriber():
    subscriber_form=SubscriberForm()
    if subscriber_form.validate_on_submit():
        subscriber= Subscriber(email=subscriber_form.email.data,title = subscriber_form.title.data)
        db.session.add(subscriber)
        db.session.commit()
        mail_message("Hey Welcome To My Blog phoebe ","email/welcome_subscriber",subscriber.email,subscriber=subscriber)
        subscriber = Blog.query.all()
        blog = Blog.query.all()
    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blog)
