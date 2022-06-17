# sniffr-be
Backend of sniffr application

#  Project Stack
A python flask app, which is dockerizerd

# Want to run this in developlment?
## First-Time Setup
1. Download this repo
2. Set up the virtual environment and install things using `requirements.txt`
3. Set up the enviromental variables correctly (see below or ask Jon)
4. Run `flask db init`
5. Run `flask db migrate`
6. Run `flask db upgrade`
7. Run `flask run`

This should set up the app, the necessities, a local sqllite database, and run the app.

# DOCKER -- UNDER CONSTRUCTION
If you want to quickly run a docker container of this app then you can:
1. Download the repo
2. Run `docker-compose up --build`
## Docker Container Usage
1. docker start sniffr-be...
2. docker stop sniffr-be...
