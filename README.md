
# Vendor Management System

## Overview
The Vendor Management System is an API built using Django and Django REST Framework. It provides endpoints for managing vendors, purchases, and performance metrics.

## Installation
1. Clone the repository:
git clone <repository-url>


2. Navigate to the project directory:
cd Vendor_Management_System


3. Install dependencies:
pip install -r requirements.txt


4. Set up the database in settings.py file:
  add your database details :
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'vendor_management_data',
        "USER": "          ",  # add your user here
        "PASSWORD": "        ",  # add your password here
        "HOST": "      ",  # add your hostname here
        "PORT": "    ",  # add your port here
    }
}



   after that : 
python manage.py migrate


5. create a superuser for admin page :
  python manage.py createsuperuser   # use this command to create superuser



## Running the Development Server
Start the development server by running:
python manage.py runserver


The server will start running at 'http://localhost:8000/'.

admin page : 'http://127.0.0.1:8000/admin/'

## Token generations : -

  this api's are secured by token based authentication so to access it on postman generate token in admin page by logging in into admin page and then 
  Users need to include their token in the request header when making requests to the API. The token should be included in the Authorization header prefixed with the string "Token".
  ex: - headers = {'Authorization': 'Token your_token_here'} in postman or thunder client
  

## API Endpoints
note : use token to access api's
### Vendors
- `GET /api/vendors/`: List all vendors
- `POST /api/vendors/`: Create a new vendor
- `GET /api/vendors/<vendor_id>/`: Retrieve a specific vendor
- `PUT /api/vendors/<vendor_id>/`: Update a specific vendor
- `DELETE /api/vendors/<vendor_id>/`: Delete a specific vendor

### Purchases
- `GET /api/purchase_orders/`: List all purchase orders
- `POST /api/purchase_orders/`: Create a new purchase order
- `GET /api/purchase_orders/<po_id>/`: Retrieve a specific purchase order
- `PUT /api/purchase_orders/<po_id>/`: Update a specific purchase order
- `DELETE /api/purchase_orders/<po_id>/`: Delete a specific purchase order
- `POST /api/purchase_orders/<po_id>/acknowledge/`: Acknowledge a purchase order

### Performance Metrics
- `GET /api/performance/`: List all performance metrics
- `POST /api/performance/`: Create a new performance metric
- `GET /api/performance/<performance_id>/`: Retrieve a specific performance metric
- `PUT /api/performance/<performance_id>/`: Update a specific performance metric
- `DELETE /api/performance/<performance_id>/`: Delete a specific performance metric
- `GET /api/vendors/<vendor_id>/performance/`: Retrieve performance metrics for a specific vendor

## Running the Test Suite
Execute the following command in your terminal to run the test suite:
python manage.py test

This will run all the tests defined in the `tests.py` file and display the results.

