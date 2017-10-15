from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123asd@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(100000))
    title = db.Column(db.String(120))

    def __init__(self, post, title):
        self.post = post
        self.title = title


@app.route('/post', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_post = request.form['blog']
        title_post = request.form['title']
        new_blog = Blog(blog_post, title_post)
        db.session.add(new_blog)
        db.session.commit()
        id = str(new_blog.id)
        return redirect('/blog?id=' + id)

    
    return render_template('post.html',title="Build a Blog!")

@app.route('/', methods=['POST', 'GET'])
def index():
    post = Blog.query.all()
    return render_template('blog.html',title="Build a Blog!", post=post)

@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    blogid = request.args.get('id')
    if blogid:

        individual_blog = Blog.query.get(int(blogid))
        return render_template('individual.html', title="Build a Blog!", post=individual_blog)
    else:
        return redirect('/')



# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#   task_id = int(request.form['task-id'])
#   task = Task.query.get(task_id)
#    task.completed = True
#   db.session.add(task)
#   db.session.commit()

#   return redirect('/')


if __name__ == '__main__':
    app.run()