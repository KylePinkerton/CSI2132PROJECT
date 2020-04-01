# CSI2132 PROJECT - AirBnB 
Authors: Kyle Pinkerton (8122569) David Hew-wing ()
Our attempt at cloning AirBnB for our CSI2132 Winter 2020 Project.

## ER Diagram
<img src="./docs/ERDiagram.png"/>

## Using dbconnection, queries:
connection = new_connection(schema="lab")
query = new_query(connection)
query.example()
rows = query.fetch_all()
print(rows)

## fix?
# make rent_rate NOT NULL in property table
# make type to propety_type in propety table
# accessible mispelled in property table (accesible)
# give property picture column