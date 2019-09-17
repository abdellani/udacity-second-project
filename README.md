# About the program
This is the second project in the Full-Stack Developer Nanondegree program from udacity.
In this application user can :
- Create his account, and login.
- Login using his github account.
- Create items under any existing category, and he will be the only one who can edit/delete them.
- Can list categories and items in json format.
- Only the first user (who has id=1), will be able to add/edit/delete categories.
# Installation 
You can get a copy of this code by running the following command in your operating system
```
git@github.com:abdellani/udacity-second-project.git
```
Another way is download directely archive file (but you'll not be able to get the updates): 
```
wget https://github.com/abdellani/udacity-second-project/archive/master.zip
```
To run this command to assert that required python packages are installed in your system.
```bash
pip install requirements.txt
```
# Configuration 
No configuration are needed to run the program. 
## Database
Before you run the program, you need to run the following commande to create the database with the schema.
```bash 
python database.py
```
# Run the code
To run the code, you need to get into the project folder and run the following command
```
python main.py
```
The application will be listening on http://localhost:8000/

Only the first user (with id=1) will be able to add/remove/edit categories. 

# Get updates
To receive the lastest updates, use the following command
```
git pull origin master
```
# Author
Mohamed ABDELLANI

# Addictional details

## Routes related to users

|action |method(http)|path |function|
|index  |get    |/signup            |registrationsNew|
|index  |post   |/signup            |registrationsCreate|
|index  |get   |/login            |sessionsNew|
|index  |post   |/login            |sessionsCreate|
|index  |get   |/login/github            |loginGithub|
|index  |get   |/github-callback            |authorized|
|index  |post   |/logout            |sessionsDestroy|

## Routes related to categories

|action |method(http)|path |function|
|-------|-------|-----|--------| 
|index  |get    |/categories            |categoriesIndex|
|index  |get    |/categories/json       |categoriesIndexJson|
|edit   |edit   |/categories/:id/edit   |categoriesEdit|
|update |post   |/categories/:id/edit   |categoriesUpdate|
|new    |get    |/categories/new        |categoriesNew|
|create |post   |/categories            |categoriesCreate|
|destroy|post   |/categories/:id/delete |categoriesDestroy|

## Routes related to Items

|action |method(http)|path |function|
|-------|-------|-----                            |--------| 
|index  |get    |/categories/:id/items            |ItemsIndex|
|index  |get    |/categories/:id/items/json       |ItemsIndexJson|
|show   |get    |/categories/:id/items/:id        |ItemsShow|
|show   |get    |/categories/:id/items/:id/json   |ItemsShowJson|
|edit   |get    |/categories/:id/items/:id/edit   |ItemsEdit|
|update |post   |/categories/:id/items/:id/edit   |ItemsUpdate|
|new    |get    |/categories/:id/items/new        |ItemsNew|
|create |post   |/categories/:id/items            |ItemsCreate|
|destroy|post   |/categories/:id/items/:id/delete |ItemsDestroy|
