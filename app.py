from flask import Flask, request
import sys
sys.path.insert(1, './db')
from dbconnection import new_connection
from queries import new_query

app = Flask(__name__)

@app.route('/')
def index():
  connection = new_connection(schema="lab")
  query = new_query(connection)
  query.example()
  rows = query.fetch_all()
  print(rows)
  return str(rows[0])

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