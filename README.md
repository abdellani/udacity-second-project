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

# Additional details

## Routes related to users

|action |method(http)|path |function|
|-------|-------|-----|--------| 
|index  |get    |/signup            |registrations.new|
|index  |post   |/signup            |registrations.create|
|index  |get   |/login            |sessions.new|
|index  |post   |/login            |sessions.create|
|index  |get   |/login/github            |loginGithub|
|index  |get   |/github-callback            |authorized|
|index  |post   |/logout            |sessions.destroy|

## Routes related to categories

|action |method(http)|path |function|
|-------|-------|-----|--------| 
|index  |get    |/categories            |categories.index|
|index  |get    |/categories/json       |categories.indexJson|
|edit   |edit   |/categories/:id/edit   |categories.edit|
|update |post   |/categories/:id/edit   |categories.update|
|new    |get    |/categories/new        |categories.new|
|create |post   |/categories            |categories.create|
|destroy|post   |/categories/:id/delete |categories.destroy|

## Routes related to Items

|action |method(http)|path |function|
|-------|-------|-----                            |--------| 
|index  |get    |/categories/:id/items            |items.index|
|index  |get    |/categories/:id/items/json       |items.indexJson|
|show   |get    |/categories/:id/items/:id        |items.show|
|show   |get    |/categories/:id/items/:id/json   |items.showJson|
|edit   |get    |/categories/:id/items/:id/edit   |items.edit|
|update |post   |/categories/:id/items/:id/edit   |items.update|
|new    |get    |/categories/:id/items/new        |items.new|
|create |post   |/categories/:id/items            |items.create|
|destroy|post   |/categories/:id/items/:id/delete |items.destroy|
