import datetime
from flask import  render_template, Blueprint, redirect, url_for
from sqlalchemy import func
from flask_login import login_required, current_user

from webapp.models import Post, User, db, Tag, Comment, tags
from webapp.forms import CommentForm, PostForm


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix="/blog"
)


'''视图函数'''


def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_time.desc()
    ).limit(5).all()

    toptags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, toptags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_time.desc()
    ).paginate(page, 5)
    recent, toptags = sidebar_data()

    return render_template('index.html', posts=posts, recent=recent, toptags=toptags)


@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    user = User.query.filter_by(id=post.user_id).first_or_404()
    comments = post.comments.order_by(Comment.date.desc()).all()
    tags = post.tags
    recent, toptags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           user=user,
                           comments=comments,
                           tags=tags,
                           recent=recent,
                           toptags=toptags,
                           form=form
                           )


@blog_blueprint.route('/tag/<string:tag_name>/')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_time.desc()).all()
    recent, toptags = sidebar_data()

    return render_template('tag.html', tag=tag, posts=posts, recent=recent, toptags=toptags)


@blog_blueprint.route('/user/<string:user_name>')
def user(user_name):
    user = User.query.filter_by(username=user_name).first_or_404()
    posts = user.posts.order_by(Post.publish_time.desc())
    recent, toptags = sidebar_data()

    return render_template('user.html', user=user, posts=posts, recent=recent, toptags=toptags)


@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.body = form.text.data
        new_post.publish_time = datetime.datetime.now()
        new_post.user = current_user
        db.session.add(new_post)
        db.session.commit()

    return render_template('new.html', form=form)


@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id=id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.text.data
        post.publish_time = datetime.datetime.now()

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', post_id=post.id))

    form.text.data = post.body
    return render_template('edit.html', form=form, post=post)