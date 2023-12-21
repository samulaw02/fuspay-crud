# Simple CRUD Application Using Python(Flask), Postgres and Docker

### OverView

CRUD stands for Create, Read, Update, Delete. It is a basic business operation for building a RESTFUL Service.

### What I have done
* Flask: I implemented the CRUD application using a Python microframework called flask. Flask is a popular Python web framework, it is lightweight and easy to set up. It also posseses some other benefits that are useful ffor building Restful Services.
* Postgres: A relational DB was used. Postgres is a very powerful, high scale SQL database.
* Containerization: Docker was used for containerizing the application
* CI/CD: Github actions was used to setup continious integration and deployment


### Added Features

* **Authentication Middleware:** I integrated JWT web token to handle authentications on the various endpoints(Update, Read, Delete). 

* **Test:** I also wrote some unit tests using python pytest library


### Quality Of Code

I have focused on writing clean, maintainable, and well-documented code. The code is organized into classes and functions for clarity and reusability. Comments have been added to explain the logic and purpose of each section of the code. The codebase is designed to be extensible, allowing for easy addition of future features.


### Authentication
For endpoints that requires authentication pass the JWT access token to the request header in this format
*   { "Authorization"  : "Bearer {access token}" }

Access token can be gotten from the login endpoint. Token expiration is an hour


### Endpoints
* Create A New User: POST : '/users'  (No Auth Required), Request Body should contain firstName, lastName, email, password

* Login : POST '/users/login'  (No Auth Required), Request Body should contain email and password

* Get All Users : GET '/users'  (Auth Required)

* Get A User : GET '/users/{id}'  (Auth Required)

* Update A User : PUT '/users/{id}'  (Auth Required), Request Body should contain firstName and lastName


* Delete A User : DELETE '/users/{id}'  (Auth Required)






### How to Run Locally

To run the game locally, follow these steps:

1. Clone the repository: `git clone https://github.com/samulaw02/fuspay-crud.git`

1. Navigate to the project directory: `cd fuspay`

1. Create a .env file, it should contain the following
    -   FLASK_ENV=staging
    -   DATABASE_URL_STAGING=postgresql://postgres@db:5432/simple_crud
    -   DATABASE_URL_PROD=postgresql://...

1. Build Docker Image: `docker-compose build`

1. Run the Image the game: `docker-compose up -d`


### Todo
I didn't implement the functionality that allow token rotation, i.e expired acccess token can be exchange for a new access token via the refresh token.


### Conclusion
I thoroughly enjoyed working on this take home assessment. If you have any questions or need further information, please feel free to reach out. Thank you for this opportunity!