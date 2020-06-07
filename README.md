# CSI2132 PROJECT - AirBnB 
Authors: Kyle Pinkerton (8122569) David Hew-wing (300013907)
AirBnB clone for our CSI2132 Winter 2020 Project.

# How to Get the Project Running 
1. pip install -r requirements.txt (PYTHON 3)
2. go to `db.py` file in the `db` directory, at the top you will see you will see the variables: 
- `dbname = "kpink074"` 
- `user = "kpink074"`
- `password = os.environ.get("UOTTAWA_PW")`
- `host = "web0.site.uottawa.ca"` 
- `port = "15432"` 
- `schema = "project"` 
- Enter your relevant information to the above to connect to your specific db instance
2. run `python3 generate_table_data.py` in the `db` directory to automatically create all tables and fill them with generated data (this isn't the fastest process)
- see specific instructions for this setup script below
#### OR 
3. As an alternative to generating your own own data using `generate_table_data.py`, you can instead restore your database using the backup files `defaultdata.backup` and `defaultdata.sql` located in the `db/backups` directory (for more information on how to do this visit https://www.postgresql.org/docs/9.1/backup-dump.html). This data was generated using `generate_table_data.py large`. A caveat to using this approach to populate your database is the fact that during the generation of data user/property pictures are saved to `static/images` in order to be served in the application. This means that your application will not have generated pictures.
3. Run the app `python3 app.py` and then go to `127.0.0.1:5000/`, you will be on the homepage of the app and ready to go!

## Running `generate_table_data.py`, the setup/data-generation script
- When running `python 3 generate_table_data.py` a "medium" dataset will be generated as default, however several command-line arguments can be passed to alter how much data will be generated:
1. `python 3 generate_table_data.py small` - a small amount of data will be generated - ~250 mb of free space required
2. `python 3 generate_table_data.py medium`- (DEFAULT - RECOMMENDED) a significant amount of data (enough to fully experience the project) will be generated - ~550 mb of free space required
3. `python 3 generate_table_data.py large` - a large amount amount of data will be generated - ~2.5 gb of free space required
- If an error occurs during data generation, use `python 3 generate_table_data.py reset` to reset the schema, and then run the script again (if the script "hangs" when using `reset` (e.g. makes no progress), there is most likely issues regarding corrupt cursors in postgresql... try again in a couple minutes or manually the fix cursors using your DBMS interface (e.g. pgadmin4 dashboard))

## ER Diagram
<img src="./docs/ERDiagram.png"/>
