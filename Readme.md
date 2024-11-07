This project is a Django-based data processing solution that reads data from input files, loads it into a PostgreSQL database, exposes RESTful APIs to interact with the data, and creates a materialized view for data summarization. The solution also includes ETL processes and secure endpoints for querying transactions.

PostgreSQL Setup:

Make sure to set up a PostgreSQL instance with the following configuration:

User: postgres
Password: postgres
Database: neo

Running the Project

Using Docker:

Build and run the project:  docker-compose up --build

After the containers are up, apply migrations:  docker-compose exec web python manage.py migrate

Load data into the database using the ETL process: python manage.py run_etl

Refresh the View: python manage.py refresh_materialized_view 

API Endpoints:

Creating the superuser: docker-compose run web python manage.py createsuperuser

Suppose having this user: 	user: root
							pwd: superuser123
							
Getting Token: curl -X POST http://127.0.0.1:8000/api/token/ -d "username=root&password=superuser123"

Fetching Transactions for specific client_id: curl -H "Authorization: Bearer <token>" "http://127.0.0.1:8000/api/clients/456e7890-e12f-23a4-b789-526715184123/transactions/"

Fetching Transactions for specific with date range: curl -H "Authorization: Bearer <token>" "http://127.0.0.1:8000/api/clients/456e7890-e12f-23a4-b789-526715184123/transactions/?start_date=xxxx-xx-xx&end_date=xxxx-xx-xx"

