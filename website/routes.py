from importlib.resources import contents
from typing import Type
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Post
from requests_cache import ExpirationTime
from .models import Post
from datetime import datetime
from . import db
import json

routes = Blueprint('routes', __name__)

@routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('contents')
            try:
                expirationdate = datetime.strptime(request.form.get('expirationdate'), '%Y-%m-%d')
            except ValueError as e:
                flash('Invalid date format.', category='error')
                print(e)
                return render_template('upload.html', user=current_user) 
            current_date = datetime.strftime(datetime.today(), '%Y-%m-%d')
            if len(title) < 1:
                flash('Title is too short!', category='error')
                return render_template('upload.html', user=current_user)
            elif len(content) < 1:
                flash('Content is too short!', category='error')
                return render_template('upload.html', user=current_user)
            elif len(content) > 100000:
                flash('Content is too long!', category='error')
                return render_template('upload.html', user=current_user)
            elif len(title) > 250:
                flash('Title is too long!', category='error')
                return render_template('upload.html', user=current_user)
            elif title == '':
                flash('Title is empty!', category='error')
                return render_template('upload.html', user=current_user)
            elif content == '':
                flash('Content is empty!', category='error')
                return render_template('upload.html', user=current_user)
            if(expirationdate <= datetime.now()):
                flash('Expiration date must be in the future!', category='error')
                return render_template('upload.html', user=current_user) 
            else:
                expirationdate = request.form.get('expirationdate')
                new_upload = Post(title=title, content=content, exipration_date=expirationdate, user_id=current_user.id, username=current_user.username, date_posted=current_date)
                db.session.add(new_upload)
                db.session.commit()
                flash('Post made!', category='success')
                return render_template('upload.html', user=current_user)
        return render_template('upload.html', user=current_user)

@routes.route('/', methods=['GET'])
def home():
    try:
        if(current_user.rank == "admin"):
            return render_template("home.html", user=current_user, posts = Post.query.filter().order_by(Post.id.desc()))
        else:
            return render_template("home.html", user=current_user, posts = Post.query.filter().order_by(Post.id.desc()))
    except AttributeError:
        return render_template("home.html", user=current_user, posts = Post.query.filter().order_by(Post.id.desc()))

@routes.route('/user/<username>')
def user(username):
    profile = User.query.filter_by(username=username).first()
    if profile is None:
        return render_template('404.html', user=current_user)
    else:
        if(current_user.rank == "admin"):
            return render_template('admin-user.html', user=profile)
        else:
            return render_template('user.html', user=profile)

@routes.route('/upload/<id>')
def dispost(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return render_template('404.html', user=current_user)
    else:
        try:
            if(datetime.strptime(post.exipration_date, '%Y-%m-%d') < datetime.now()):
                db.session.delete(post)
                db.session.commit()
                flash('Error: The post you are looking for has expired.', category='error')
                return render_template('404.html', user=current_user)
            else:
                Post.query.filter_by(id=id).update(dict(views=post.views + 1))
                db.session.commit()
                try:
                    if(current_user.rank == "admin"):
                        return render_template('admin-post.html', post=post, user=current_user, creator=User.query.filter_by(id=post.user_id).first())
                    else:
                        return render_template('post.html', post=post, user=current_user, creator=User.query.filter_by(id=post.user_id).first())
                except AttributeError as e:
                    return render_template('post.html', post=post, user=current_user, creator=User.query.filter_by(id=post.user_id).first())
        except ValueError as e:
            flash('Error: The post you are looking for has expired.', category='error')
            print(e)
            return render_template('404.html', user=current_user)

@routes.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if current_user.rank == "admin":
            db.session.delete(post)
            db.session.commit()
        else:
            flash('Error: You do not have permission to delete this post.', category='error')
            return render_template('404.html', user=current_user)

    return render_template('home.html', user=current_user, posts = Post.query.filter().order_by(Post.id.desc()))

@routes.route('/ban-user', methods=['POST'])
def ban_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        if current_user.rank == "admin":
            if user.banned == True:
                User.query.filter_by(id=userId).update(dict(banned = False))
            elif user.banned == False:
                User.query.filter_by(id=userId).update(dict(banned = True))
            db.session.commit()
        else:
            flash('Error: You do not have permission to delete this post.', category='error')
            return render_template('404.html', user=current_user)

    return render_template('home.html', user=current_user, posts = Post.query.filter().order_by(Post.id.desc()))