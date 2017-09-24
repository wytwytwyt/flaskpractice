from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


'''模型类'''


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


tags = db.Table('post_tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment',
                               backref='post',
                               lazy='dynamic',
                               )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag: {}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment: {}>'.format(self.text[:15])


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


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_time.desc()
    ).paginate(page, 10)
    recent, toptags = sidebar_data()

    return render_template('index.html', posts=posts, recent=recent, toptags=toptags)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404('post_id')
    comments = Post.comments.order_by(Comment.date.desc()).all()
    tags = post.tags
    recent, toptags = sidebar_data()

    return render_template('post.html', post=post, comments=comments, tags=tags, recent=recent, toptags=toptags)


@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    post = tag.posts.order_by(Post.publish_time.desc()).all()
    recent, toptags = sidebar_data()

    return render_template('tag.html', tag=tag, post=post, recent=recent, toptags=toptags)


@app.route('/user/<string:user_name>')
def user(user_name):
    user = User.query.filter_by(username=user_name).first_or_404()
    posts = User.posts.order_by(Post.publish_time.desc()).all()
    recent, toptags = sidebar_data()

    return render_template('user.html', user=user, posts=posts, recent=recent, toptags=toptags)


if __name__ == '__main__':
    app.run()
