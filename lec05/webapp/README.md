# Web App
Run:
```shell
docker build -t flaskapp . 
docker run -p 5000:80 --volume=${pwd}:/app flaskapp
```
And access [localhost:5000](http://localhost:5000). 
(Commands may differ slightly for Windows machines)

Alternatively, you can run the following lines of command:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
This will start running the application on a Flask development server.
(Commands may differ slightly for Windows computers)