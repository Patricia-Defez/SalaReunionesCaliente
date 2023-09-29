# La Sala de Reuniones Caliente

 ## Description:
The project is a small REST API that allows to know all the information related to the meeting rooms of a coworking company: the clients who can reserve them, the reservations, the status of the rooms and different reports of the use of the rooms.<br/>
It is made entirely in Python using the FastAPI framework and a MongoDB database.<br/>
Python version is 3.10.11<br/>
Fastapi version is 0.103.1<br/>
## Instructions to launch the REST API service:
### Previous requirements:
To deploy this project, it is necessary to have a MongoDB. That is possible for free by registering a MongoDB Atlas account.
[Atlas register page](https://www.mongodb.com/cloud/atlas/register)<br/>
The procedure is:
- Create a new cluster.<br/>
- Create a new user for the database.<br/>
- Allow connection from any IP.<br/>
- Connect to your cluster. When you get the connection URL, you should copy it inside the project code in the db.py file:<br/>
  ```conn = MongoClient("your url")```<br/><br/>
For more information: [Atlas gide](https://www.mongodb.com/docs/guides/atlas/cluster/)
### Create a virtual env:
After cloning the project, it is recommended to create a virtual env.<br/>
- To create the virtual env, got to the project root in a terminal and write:<br/>
  ```python3 -m venv env```<br/>
- To activate it:
  In Windows:
  ```source env/bin/activate```<br/>
  In Unix/macOS:
  ```.\env\Scripts\activate```<br/>
- To leave it:
  ```deactivate```<br/><br/>
For more information: [Python gide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
### Installations:
It is necessary to have Python3 installed, but also, some dependencies are necessary.<br/>
With the venv activate:
```
   pip install fastapi
   pip install uvicorn
   pip install pymongo
```
### Start server
```uvicorn app:app --reload```

   
   

