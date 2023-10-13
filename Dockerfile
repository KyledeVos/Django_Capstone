# provides web server and python library
FROM python:3.11-alpine

# retrieve dependencies from requirements.txt
COPY requirements.txt requirements.txt
# install dependencies
RUN pip install -r requirements.txt

# set working directory
WORKDIR /django_capstone
# copy all content from the current directory
COPY . /

# instruct docker which port to listen to for application run
EXPOSE 8000/tcp

# command to start running of server at desired port
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]