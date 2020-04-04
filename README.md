# CSI2132 PROJECT - AirBnB 
Authors: Kyle Pinkerton (8122569) David Hew-wing ()
Our attempt at cloning AirBnB for our CSI2132 Winter 2020 Project.

# How to get the project running 
1. pip install -r requirements.txt (PYTHON 3)
2. go to `db.py` file in the `db` directory, at the top you will see you will see the variables: `dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project"`
3. Enter your relevant information to the above to connect to your specific db instance
4. Use create table statements in `DDL.sql` file in the `db` directory to create all the required tables in pgadmin4 (statements lower in the file depend on statements higher in the file) then you insert the data by yourself using pgadmin4 
- ALTERNATIVE TO 4 : run `python3 generate_table_data.py` (W.I.P. - currently creates tables, inserts data into branches, person, users, person_phone_number, person_email_address, employees, admins, properties, payment_method, payout_method, works_at, rental_agreement, property_taken_dates, payment)
5. Run the app `python3 app.py`


## Front-end constraints (cuz of yolo)
1. Reference country.js to see countries supported
2. No spaces in propertynames or usernames (ez to fix but ya...)
3. You can only have 1 payment method, 1 payout method, 1 phone, 1 email 
4. probably other things...

## ER Diagram
<img src="./docs/ERDiagram.png"/>

## fix?
- payment/payout tables should have all keys as primary keys... or not? (right now there is if statement on payment/payout pages not letting u add more than 1)
