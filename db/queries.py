from dbconnection import new_connection

class Query:
  def __init__(self, connection):
    self.connection = connection
    self.cursor = self.connection.cursor
  
  def fetch_all(self):
    return self.cursor.fetchall()

  def example(self):
    self.cursor.execute("select * from artist")

def new_query(connection):
  return Query(connection)
