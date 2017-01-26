# Delivery Calculator
This application calculates the earliest time for delivering products to a destination warehouse.
## Important Considerations
This project was done with extensibility in mind so that the most important elements of it could easily be changed.
This decision has the following effects:  
1. In its current form, the efficiency of the underlying algorithms is not a priority.  
But, due to its extensibility, the most important algorithms can easily be changed or extended.  
2. The Delivery Calculator feature of the application runs simulations.  
This means that when you calculate a delivery time, no changes are made to the database.
## Running the Project
### Getting Ready
This project requires the latest version of `python 2.7` and `Django 1.7`.    
It was tested on `macOS 10.12.2`. Any errors from running the following commands might be platform-specific.  
### Create the Database
Go to the `deliver_calculator` folder which has `manage.py` in it.  
To create the dev db, run these commands
```bash
python manage.py migrate
```   
To populate the db with test data, run this command
```bash
python manage.py shell
```
Once in django's python shell, run these commands
```python
>>> from load_test_data import *
>>> load_warehouses()
>>> load_connections()
>>> load_products()
>>> load_inventory()
```
Note that the test CSV files are already included with the project.
### Using the Web Application
First, run the dev server
```bash
python manage.py runserver
```  
This command runs the dev server and tells you the url for accessing the web application.
After vising the page, you'll see a form with 4 fields.
The calculator runs a simulation after each submission, so no data from the database is modified.
### Run Tests
```bash
python manage.py test
```
## Suggested Improvements
If I were to review/refactor this project, I would make the following improvements:  
There are many improvements to be made on the UI and UX side of the application.  
On the back-end side, some of the logic of algorithms could be simplified to make the code more readable.  
Also, many of the algorithms could be made faster.  
Structural, logical, and object oriented design of the application can also be made more intuitive.  