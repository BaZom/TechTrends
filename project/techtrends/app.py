import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
from datetime import datetime
import sys

current_connections_counter = 0
all_connections_counter = 0


def check_db_connection(connection):
     try:
        conn.cursor()
        return True
     except Exception as exception:
        app.logger.error('db connection failed ', exception)
        return False

def get_db_connection():
    """This function connects to database with the name database.db."""
    global current_connections_counter, all_connections_counter
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    if check_db_connection:
        current_connections_counter +=1
        all_connections_counter +=1
        return connection

def get_post(post_id):
    """Function to get a post using its ID"""
    global current_connections_counter
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    current_connections_counter -=1
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    global current_connections_counter
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    current_connections_counter -=1
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    """
    Define how each individual article is rendered 
    If the post ID is not found a 404 page is shown
    """
    post = get_post(post_id)
    if post is None:
        app.logger.debug('Article not found')
        return render_template('404.html'), 404
    else:
        app.logger.debug(f'Article "{post["title"]}" retrieved!')
        return render_template('post.html', post=post)

@app.route('/about')
def about():
    """ Define the About Us page"""
    app.logger.info('About Us page is retrieved.')
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    """ Define the post creation functionality """
    global current_connections_counter
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            current_connections_counter -=1

            app.logger.debug(f'new article "{title}" created!')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    global current_connections_counter
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    
    response = app.response_class(
            response=json.dumps({"db_curr_connection_count": current_connections_counter, "db_all_connection_count": all_connections_counter, "post_count": len(posts)}),
            status=200,
            mimetype='application/json'
    )
    connection.close()
    current_connections_counter -=1
    app.logger.info('Metrics request successfull')
    return response
   
# start the application on port 3111
if __name__ == "__main__":

    # Set logger to handle STDOUT and STDERR
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [stderr_handler, stdout_handler]

    # Create the log file and format each log
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
        level=logging.DEBUG,
        datefmt='%m-%d-%Y, %H:%M:%S',
        handlers=handlers
    )
    app.run(host='0.0.0.0', port='3111')
