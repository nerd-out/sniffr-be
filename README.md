# sniffr-be
The backend of sniffr! an application for finding play dates for your dog!

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


# Backend Routes
## User Routes
#### `/login` 

Success example (*with my correct password cesnored to xxxxxx*):
![login success example](extra\readme_images\user_success.PNG)  

Fail example (*wrong password*):
![login fail example](extra\readme_images\user_fail.PNG)


## Dog Routes
### `/dog/:id` **GET** 

Success example:  
![GET Dog success](extra\readme_images\dog_get_success.PNG)  

Fail example:  
![GET Dog fail](extra\readme_images\dog_get_fail.PNG)

### `/dog:id` **POST**

Successfully adding a new dog example (*request sent without a dog id*):  
![GET Dog success](extra\readme_images\dog_post_success.PNG)  

Editing a dog is broken example (**This route is currently under construction still**):  
![GET Dog fail](extra\readme_images\dog_post_edit_broken.PNG)