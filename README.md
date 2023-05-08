# Improvado chatbot

This project implements a chatbot interface to LLM that allows the user to asks questions about Improvado's blog entries
by Sergio Marchio


## Initial setup - extra files required

To run this project, you must create the file
 - `secret.key` in the root directory of the project (where you can also find [manage.py](manage.py) file), containing the django secure key in plain text format (ideally created with more than 50 random characters and more than 5 unique characters).


### To run the server *locally*

The project is configured by default for its local execution, for debugging/testing purposes

From the project's root directory, in the console:

 - Create virtual environment
`python -m venv improvado`

 - Activate it

   - linux / MacOS:
   - `source improvado/bin/activate`

   - Windows
   - `improvado\Scripts\activate.bat`

 - install required packages
```
pip install -r requirements.txt
```

 - Start the server in the desired port, e.g. 8080
```
python manage.py runserver 8080 
```

 - Now you can access the chatbot from your browser:
```
http://localhost:8080/
```

