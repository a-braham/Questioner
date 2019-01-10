[![Build Status](https://travis-ci.org/a-braham/Questioner.svg?branch=develop)](https://travis-ci.org/a-braham/Questioner) 
[![Coverage Status](https://coveralls.io/repos/github/a-braham/Questioner/badge.svg?branch=develop)](https://coveralls.io/github/a-braham/Questioner?branch=develop)

# Questioner
Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log.

## Prerequisites
- Python 3.6.7 
- Postman


## Installation
1. Clone this repository :

	```
    $ git clone https://github.com/ssiva13/Questioner.git
    ```

2. CD into the project folder on your machine

	```
    $ cd Questioner
    $ pip install virtualenv
    ```

3. Create a virtual environment

    ```
    $ virtualenv venv
    ```

4. Activate the virtual environment

	```
    $ source venv/bin/activate
    ```

5. Install the dependencies from the requirements file

	```
    $ pip install -r requirements.txt
    ```

6. Run the application

    ```
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    flask run
    ```

## Testing API endpoints

-------------------------------------------------------------------------------------------------------------
| Endpoint                            				| HTTP Verb   | Functionality           			    |
| ------------------------------------------------- | ----------- | ---------------------------------------- 
| /api/v1/meetups                  				    | POST        | Create a meetup record     			    |
| /api/v1/meetups/<meetup_id>          				| GET         | Fetch a specific meetup record   		|
| /api/v1/meeetups/upcoming/          		 		| GET         | Fetch all upcoming meetup records       |
| /api/v1/questions                				    | POST        | Create a question for a specific meetup |
| /api/v1/questions/<question_id>/upvote			| PATCH       | Up-vote a specific question        	    |
| /api/v1/questions/<question_id>/downvote			| PATCH       | Down-vote a specific question       	|
| /api/v1/add_meetups/<meetup_id>/rsvps   			| POST        | Create a question for a specific meetup |
-------------------------------------------------------------------------------------------------------------

#### Run tests
    ```
    pytest
    ```

## Authors
Abraham Kamau - [Abraham Kamau](https://github.com/a-braham)

## License