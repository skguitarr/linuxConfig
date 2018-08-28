# Project Title

Guitar Catalog Project - Linux Configuration

## Getting Started

IP ADDRESS:
http://18.222.119.170

SSH PORT:
2200

Launch the web app by navigating to the following url:
http://18.222.119.170/catalog

NOTE TO INSTRUCTOR:  The only thing I didn't get working was the Google OAuth.  I believe that I'm getting the oauth error because google doesn't like IP addresses in client_secrets.json file, they only allow hostnames not IP addys.  Since the Rubric did not mention Oauth, I'd prefer to avoid the montly fee to set up a DNS hostname definition. Or if there's an easy way to work around this can you help?  Thanks in advance.

## Summary of Software Installed
certifi==2018.8.24
chardet==3.0.4
click==6.7
docopt==0.6.2
Flask==1.0.2
Flask-SQLAlchemy==2.3.2
httplib2==0.11.3
idna==2.7
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
oauth2client==4.1.2
pipreqs==0.4.9
psycopg2-binary==2.7.5
pyasn1==0.4.4
pyasn1-modules==0.2.2
requests==2.19.1
rsa==3.4.2
six==1.11.0
SQLAlchemy==1.2.11
urllib3==1.23
virtualenv==16.0.0
Werkzeug==0.14.1
yarg==0.1.9

## Summary of configurations made
1)  Ran "sudo apt-get update" to update installed software.
2)  Changed the ssh port from 22 to 2200.
3)  Set up the firewall to only allow the 3 ports:  2200, 80, 123.
4)  Created user grader and gave sudo access.
5)  Created public and private keys with sshkeygen, installed the public keys on the server in the .ssh directories.
6)  Set up wsgi for Python 2.
7)  Set up the catalog database by installing postgresql, creating "catalog" user after sudo su to postgres user, created catalog DB, ran DB setup files.
8)  Set up wsgi and __init__.py files in /var/www/FlaskApp dirs. Changed original python file to __init__.py.
9)  Updated the python DB setup files and __init__.py file to point to the postgresql catalog DB.

## Third-party resources
Amazon Web Services (AWS)
Linux open source
Ubuntu open source

## Authors
Sean Kelley, Udacity
