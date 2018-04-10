# Project Title

Guitar Catalog Project

## Getting Started

The catalog.db file is checked in and can be used as is.  If you want to create a new database from scratch following these steps:
1)  python database_setup.py - Run this to create the database for the application.
2)  python populate_catalog_database.py - Run this file to populate the database.

Next, run the main project python file like so:
python catalog_project.py

Launch the web app by navigating to the following url:
http://localhost:5000/catalog

### Prerequisites

Database should be set up, or use existing/checked-in DB (See "Getting Started" section).

## Additional Info

The following JSON Endpoints are available:
http://localhost:5000/catalog/1/items/JSON (where '1' is the category number)
http://localhost:5000/catalog/JSON (this shows the categories which make up the catalog)

At any point, click on the home icon or the "Guitar Catalog" header to go back to the main page.

User must login prior to doing Add, Edit, and Delete functionality.  If a user attempts to access these, the app will redirect to the login.


## Authors

Sean Kelley, Udacity