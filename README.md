# CSI2132 PROJECT - AirBnB
Authors: Kyle Pinkerton (8122569) David Hew-wing (300013907)

This project is an "AirBnB clone" created for our CSI2132 (Databases) Winter 2020 Final Project.

The focus of this project was to apply the fundamentals of database design to create a valid domain-specific schema which could then be utilized for the implementation of a web application resembling airbnb.com.

The following is a video overview of the project: https://www.youtube.com/watch?v=FUaoXAJs5TY

# How to Get the Project Running
## STEPS
1. pip install -r requirements.txt (PYTHON 3)

2. go to `db.py` file in the `db` directory, at the top you will see you will see the variables:
```
dbname = "kpink074"
user = "kpink074"
password = os.environ.get("UOTTAWA_PW")
host = "web0.site.uottawa.ca"
port = "15432"
schema = "project"
```

Enter your relevant information to the above parameters in order to connect to your specific database instance.

3. run `python3 generate_table_data.py` in the `db` directory to automatically create all tables and fill them with generated data (generating the data takes some time, i.e. this isn't a "fast" process - see specific instructions for this setup script below).

### OR

4. As an alternative to Step 3 (generating your own own data using `generate_table_data.py`), you can instead restore your database using the backup files `defaultdata.backup` and `defaultdata.sql` located in the `db/backups` directory (for more information on how to do this visit https://www.postgresql.org/docs/9.1/backup-dump.html). This data was generated using `generate_table_data.py large`. A caveat to using this approach to populate your database is the fact that during the generation of data user/property pictures are saved to `static/images` in order to be served in the application. This means that your application will not have generated pictures. The benefit of this approach is that you will not have to wait for data to be generated using the data generation script.

5. Run the app `python3 app.py` and then go to `127.0.0.1:5000/`, you will be on the homepage of the app and ready to go!

## Running `generate_table_data.py`, the setup/data-generation script
When running `python 3 generate_table_data.py` a "medium" dataset will be generated as default, however several command-line arguments can be passed to alter how much data will be generated:
1. `python 3 generate_table_data.py small` - a relatively small amount of generated data ~250 mb of free space required
2. `python 3 generate_table_data.py medium`- (DEFAULT - RECOMMENDED) a relatively larger amount amount of generated data compared to `small` ~550 mb of free space required
3. `python 3 generate_table_data.py large` - a relatively larger amount amount of generated data compared to `medium` ~2.5 gb of free space required

If an error occurs during data generation, use `python 3 generate_table_data.py reset` to reset the schema, and then run the script again (if the script "hangs" when using `reset` (e.g. makes no progress), there is most likely issues regarding corrupt cursors in postgresql... try again in a couple minutes or manually the fix cursors using your DBMS interface (e.g. pgadmin4 dashboard))

## Entity Relationship (ER) Diagram
<img src="./docs/ERDiagram.png"/>
