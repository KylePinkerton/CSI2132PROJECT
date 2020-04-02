# CSI2132 PROJECT - AirBnB 
Authors: Kyle Pinkerton (8122569) David Hew-wing ()
Our attempt at cloning AirBnB for our CSI2132 Winter 2020 Project.

# How to get the project running 
1. pip install -r requirements.txt (PYTHON 3)
2. go to the bottom of db.py file, you will see: `connection = new_connection(dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project")`
3. Enter your relevant information to the above
4. Use create table statements in `DDL.sql` to create all the required tables in pgadmin4
5. Run the app `python app.py`

## ER Diagram
<img src="./docs/ERDiagram.png"/>

## fix?
- payment/payout tables should have all keys as primary keys... or not? (right now there is if statement on payment/payout pages not letting u add more than 1)
- make sidebar statistics?