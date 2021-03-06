from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    name = db.Column(db.String(120))

    def  __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET']) 
def blog_posts():
    print(request.args)

    if request.args.get('id') == None:
        return render_template('blog.html', blogs = get_blog_posts())
    else:
        new_id = request.args.get('id')
        blog_post = db.session.query(Blog).filter_by(id=new_id).first()
        body = blog_post.body
        title = blog_post.title
        return render_template('blogpost.html', title=title, body=body)


def get_blog_posts():
    return Blog.query.all()

@app.route('/')  
def home():
    return render_template('blog.html', blogs = get_blog_posts())

@app.route('/newpost', methods=['POST', 'GET'])
def index():
    
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == '':
            flash('Uh Oh! Please enter a title for your blog post.', 'error')
            return render_template('newpost.html', body=body)
        if body == '':
            flash('Uh OH! Please enter a thing or two about your blog post.', 'error')
            return render_template('newpost.html', title=title)
        blog = Blog(title=title, body=body)
        db.session.add(blog)
        db.session.commit()
        return render_template('blogpost.html', title=title, body=body)
    
    return render_template('newpost.html')


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()