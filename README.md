# TO-DO list
A simple web application to manage your tasks and be more productive.

Functionality:
* adding, deleting, editing, finishing tasks
* adding, deleting, editing projects
* sorting tasks by categories: today, next 7 days and by projects
* adding finished tasks to the archive
* logging and register new users
* an impossibility to look through tasks and to the actions with them without logging
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
### Prerequisites
You need to have Python 3.5.3 at least, pip and virtualenv to run this project properly.

To install pip if you don't have one:
```
$ python get-pip.py
```
To install virtualenv:
```
$ pip install virualenv
```
### Installing
1) Clone the project:
```
$ git clone https://github.com/annie-shlepak/todo_list.git
```
2) Create and run virtualenv:
```
$ virtualenv -p python3 env
$ source env/bin/activate
```
3) Open the project folder and install all requirements needed via pip:
```
pip install requirements.txt
```
4) Run project (be sure that 8000 port is free):
```
$ cd todo_list && python manage.py runserver
```
## Versioning
Python 3.5.3 & Django 1.11.5
### Authors
* **Anna Shlepak**
