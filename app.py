from flask import Flask, render_template
from data import Articles

app = Flask(__name__)

Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('index.html')

# About 
@app.route('/about')
def about():
    return render_template('about.html')

# Get Articles
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

#Single Articles
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


if __name__ == '__main__':
    app.run(debug=True)