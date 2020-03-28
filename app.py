from flask import Flask, request, render_template
import sys
sys.path.insert(1, './db')
from dbconnection import new_connection
from queries import new_query

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("homepage.html")

@app.route('/post_user', methods=['POST'])
def post_user():
  return "post user"

@app.route('/shutdown', methods=['GET'])
def shutdown():
    def shutdown_server():
      func = request.environ.get('werkzeug.server.shutdown')
      if func is None:
          raise RuntimeError('Not running with the Werkzeug Server')
      func()
    shutdown_server()
    return "Server shutting down..."

if __name__ == "__main__":
  app.run()