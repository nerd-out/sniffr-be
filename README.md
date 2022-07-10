# sniffr-be
The backend of sniffr! an application for finding play dates for your dog!

#  Project Stack
A python flask app, which is dockerizerd

# Want to run this in developlment?
## First-Time Setup
1. Clone the backend repo to a folder on your machine  
![clone this repo](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/clone_repo.png)  

2. If you are going to be changing code then switch to a new branch using
```
git checkout xxxx
```
3. Move into the cloned repo with 
```bash
cd sniffr-be
```

4. Add a blank file called `.env` into the repo so the app can pull sensitive information. Fill the `.env` file with the information in the discord pinned messages.  
![env file](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/env_directory.png)  

5. Set up a virtual environment (a mini python development workspace) using `pipenv` by running `pipenv install` when in the app's base directory:  
🚨 *This step will produce more code than just shown below and could take a few minutes depending on dependancy installation / your machine.*  
![pipenv install](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/pipenv_install.png) 

6. Activate your environment by running `pipenv shell` as the prompt says. This will load the things you placed in .env and activate the necessary python imports.  
![pipenv shell](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/pipenv_shell.png) 

7. We need to set up the database next. You are going to run 3 commands in sequence into your bash terminal once you have started your pipenv shell in step 6:

    i. `flask db init`  
    ii. `flask db migrate`  
    iii. `flask db upgrade`  

    The above commands will set up the **init**ial sqlite db, create a **migrat***tion script that will set up the db as we have written it in `models.py` and the third command will run the migration script (`ii`) and **upgrade** (`iii`) our initial (`i`) sqlite database. 

    💻 *You should end up with a folder called `migrations/` and the file `sniffrdb.db`, which contains our blank tables, if everything went well.* 

8. Lastly, we need to seed our database with starter information. To do so, run `python seed_db.py` when in the base directory to run the seed script. If successful, it should print out new entries in each of the tables that were seeded. Example:  
![seed db output](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/seed_db.png)

## Running the app (after the first-time installation steps above)
Supposing you did steps 1-8 above already...

1. Make sure you are in the correct branch, and then activate your pipenv shell:  
    ```bash
    pipenv shell
    ``` 
    ![pipenv shell 2](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/pipenv_shell.png) 

2. Once active, you can run the flask app:  
    ```bash
    flask run
    ```
    ![flask run](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/flask_run.png) 

    ✔️ *This should run up the app. You can now use* curl *,* postman *,* thunder client *, or* a browser *to access routes*

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
![login success example](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/user_success.png)  


Fail example (*wrong password*):  
![login fail example](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/user_fail.png)  



## Dog Routes
### `/dog/:id` **GET** 

Success example:  
![GET Dog success](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/dog_get_success.png)  


Fail example:  
![GET Dog fail](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/dog_get_fail.png)  


### `/dog:id` **POST**

Successfully adding a new dog example (*request sent without a dog id*):  
![Post Dog success](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/dog_post_success.png)  


Editing a dog is broken example (**This route is currently under construction still**):  
![Post Dog edit](https://raw.githubusercontent.com/the-best-team-seven/sniffr-be/finish-user-login-routes/extra/readme_images/dog_post_edit_broken.png)  
