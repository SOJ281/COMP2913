# COMP2913

Repository for the project implementing a scooter renting web application. \
Implemented by Team 6: Deep Waghulde, Kaiwen Bao, Natalia Nikliborc, Ruilin Li, Scott James, Zhan Feng and Zhanpeng Zhu.

## Running the project files

This is an instruction how to run the project on a Linux machine (assumming that Flask is installed on the machine):

1. Open the terminal and activate the flask environment by typing:

`source flask/bin/activate`

2. Navigate to the project directory.
3. Type the below commands, one after another:

`export FLASK_APP=run.py` \
`export FLASK_ENV=development`

4. Run the Flask server by typing:

`flask run`

5. Open a browser and go to "localhost:5000". This should load the project in the browser. 

## Staff login

Staff details will be pre-saved in the database meaning there will be no registration option for staff, only login. 
There are two types of staff: employee and manager.

One staff member of each type has been added for now: 

Employee: \
email: staff_1@gmail.com \
password: password12345

Manager: \
email: manager@gmail.com \
password: 1234567




