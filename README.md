# Pre-Requisites

Install python 3.7 or above on your machine:

 * Mac OS X: https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.6.pkg
 * Linux: see your distro docs

Install pip:

Download this script: https://bootstrap.pypa.io/get-pip.py

Run (you may need to specify python3 if you also have python2 installed)

    $ python get-pip.py

Install git (Linux):

    $ sudo apt-get install git

    
Install Docker:

 * Linux/Mac OS - https://docs.docker.com/install/
 * Linux also needs docker-compose: https://docs.docker.com/compose/install/
    
    Run this command to download the current stable release of Docker Compose:

        $ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    Apply executable permissions to the binary:

        $ sudo chmod +x /usr/local/bin/docker-compose
      

# Download albert

    $ git clone https://github.com/orion3000/albert
    $ cd albert

# Project structure

Created one api app with startapp.  If this was more a more extensive api with more models would have used a core app
and added additional apps like user, card, etc, etc.
Used json for default renderers and parsers.  Included docker and docker compose files to allow for locally using posgres
as db. 

    ├── ccvalidate
    │   ├── api
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── __init__.py
    │   │   ├── management
    │   │   │   ├── commands
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── wait_for_db.py
    │   │   │   ├── __init__.py
    │   │   ├── middleware.py
    │   │   ├── models.py
    │   │   ├── permissions.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   ├── test_admin.py
    │   │   │   ├── test_commands.py
    │   │   │   ├── test_models.py
    │   │   │   └── test_views.py
    │   │   ├── urls.py
    │   │   ├── utils.py
    │   │   └── views.py
    │   ├── ccvalidate
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   └── manage.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    └── requirements.txt
  

# Run api locally

Go to project directory, make migrations, migrate, and create superuser. *Mac users might not need sudo

    $ cd ccvalidate
    
    $ sudo docker-compose build
    
    $ sudo docker-compose run ccvalidate sh -c "python manage.py makemigrations api"
    
        Starting albert_db_1 ... done
        Migrations for 'api':
            api/migrations/0001_initial.py
                - Create model User
                - Create model Creditcard
            
    $ sudo docker-compose run ccvalidate sh -c "python manage.py migrate"

        Starting albert_db_1 ... done
        Operations to perform:
        Apply all migrations: admin, api, auth, contenttypes, sessions
        Running migrations:
        Applying contenttypes.0001_initial... OK
        Applying contenttypes.0002_remove_content_type_name... OK
        Applying auth.0001_initial... OK
        Applying auth.0002_alter_permission_name_max_length... OK
        Applying auth.0003_alter_user_email_max_length... OK
        Applying auth.0004_alter_user_username_opts... OK
        Applying auth.0005_alter_user_last_login_null... OK
        Applying auth.0006_require_contenttypes_0002... OK
        Applying auth.0007_alter_validators_add_error_messages... OK
        Applying auth.0008_alter_user_username_max_length... OK
        Applying auth.0009_alter_user_last_name_max_length... OK
        Applying auth.0010_alter_group_name_max_length... OK
        Applying auth.0011_update_proxy_permissions... OK
        Applying api.0001_initial... OK
        Applying admin.0001_initial... OK
        Applying admin.0002_logentry_remove_auto_add... OK
        Applying admin.0003_logentry_add_action_flag_choices... OK
        Applying sessions.0001_initial... OK

    $ sudo docker-compose run ccvalidate sh -c "python manage.py createsuperuser"

        Starting albert_db_1 ... done
        Email: admin@example.com
        Password: adminpass 
        Password (again): adminpass
        The password is too similar to the email.
        Bypass password validation and create user anyway? [y/N]: y
        Superuser created successfully.


Run tests:

    $ sudo docker-compose run ccvalidate sh -c "python manage.py test && flake8"
        
    Starting albert_db_1 ... done
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ...Waiting for database...
    Database unavailable, waiting 1 second...
    Database unavailable, waiting 1 second...
    Database unavailable, waiting 1 second...
    Database unavailable, waiting 1 second...
    Database unavailable, waiting 1 second...
    Database available =)
    .Waiting for database...
    Database available =)
    ..................
    ----------------------------------------------------------------------
    Ran 22 tests in 2.335s

    OK
    Destroying test database for alias 'default'...


    
Start server:

    $ sudo docker-compose up

# Admin Login

`http://127.0.0.1:8000/admin/api/user/`

# API endpoints

Ccvalidate api provides users with the ability to perform CRUD operations on credit card models, submit a credit card 
for validation, and generate a random valid credit card given a network.



## creditcard

This endpoint lets you create, read, update, delete a creditcard record.
Given a credit card 
the api will return the following fields:

id - The record id

ccnumber - The credit card number

email - The users email
 
valid - true, none

mii - Major Industry Identifier

mii_details - Major Industry Identifier Details

iin - Issuer Identifier Number

iin_details - Issuer Identifier Name

pan - Person account number

network - Network name

check_digit - The check digit

#### HTTP Request

`POST/GET/PUT/DELETE http://localhost:8000/creditcard/<id>/`

Content-Type
```shell script
application/json
```

#### HTTP Response codes

Code | Description
---- | -----------
200  | Request successful
201  | Created
204  | No Content
400  | Bad Request

#### URL Parameters

Parameter | Description
--------- | -----------
id | the id associated with the credit card record (optional) 

#### Payload Parameters

Parameter | Description
--------- | ----------- 
ccnumber | required for PUT, POST
mii | optional for PUT
mii_details | optional for PUT
iin | optional for PUT
iin_details | optional for PUT
pan | optional for PUT
network | optional for PUT
check_digit | optional for PUT

#### Sending data

You can send data by posting it as json in the request body. You must use Basic Auth with email and password set in 
superuser command.

#####GET all
```shell script
curl -X GET \
  http://127.0.0.1:8000/creditcard/ \
  -H 'Authorization: Basic YWRtaW5AZXhhbXBsZS5jb206YWRtaW5wYXNz' \
  -H 'cache-control: no-cache'
```
Response
```shell script
Status: 200 OK
Content-Type: application/json
```
```json
[
    {
        "id": 2,
        "ccnumber": "371559102252018",
        "email": "admin@example.com",
        "mii": "3",
        "mii_details": "Banking & Financial (Visa, Switch, and Electron)",
        "iin": "371559",
        "iin_details": "American Express",
        "pan": "10225201",
        "network": "American Express",
        "check_digit": "8",
        "valid": true
    },
    {
        "id": 3,
        "ccnumber": "4815880016564363",
        "email": "admin@example.com",
        "mii": "4",
        "mii_details": "Banking & Financial (Visa, Switch, and Electron)",
        "iin": "481588",
        "iin_details": "Visa",
        "pan": "0016564363",
        "network": "NewNetwork2",
        "check_digit": "3",
        "valid": true
    }
]
```

#####GET id
```shell script
curl -X GET \
  http://127.0.0.1:8000/creditcard/4/ \
  -H 'Authorization: Basic YWRtaW5AZXhhbXBsZS5jb206YWRtaW5wYXNz' \
  -H 'cache-control: no-cache'
```
Response
```shell script
Status: 200 OK
Content-Type: application/json
```
```json
{
    "id": 4,
    "ccnumber": "371559102252018",
    "email": "admin@example.com",
    "mii": "3",
    "mii_details": "Banking & Financial (Visa, Switch, and Electron)",
    "iin": "371559",
    "iin_details": "American Express",
    "pan": "10225201",
    "network": "American Express",
    "check_digit": "8",
    "valid": true
}
```
#####POST

```shell
curl -X POST \
  http://127.0.0.1:8000/creditcard/ \
  -H 'Authorization: Basic YWRtaW5AZXhhbXBsZS5jb206YWRtaW5wYXNz' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"ccnumber": "371559102252018"}'
```

Response
```shell script
Status: 201 Created
Content-Type: application/json
```
```json
{
   "id":1,
   "ccnumber":"371559102252018",
   "email":"admin@example.com",
   "mii":"3",
   "mii_details":"Banking & Financial (Visa, Switch, and Electron)",
   "iin":"371559",
   "iin_details":"American Express",
   "pan":"10225201",
   "network":"American Express",
   "check_digit":"8",
   "valid":true
}
```

#####PUT
```shell script
curl -X PUT \
  http://127.0.0.1:8000/creditcard/3/ \
  -H 'Authorization: Basic YWRtaW5AZXhhbXBsZS5jb206YWRtaW5wYXNz' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"network": "NewNetwork", "ccnumber": "371559102252018"}'
```       
Response
```shell script
Status: 201 Created
Content-Type: application/json
```
```json
{
    "id": 3,
    "ccnumber": "371559102252018",
    "email": "admin@example.com",
    "mii": "3",
    "mii_details": "Banking & Financial (Visa, Switch, and Electron)",
    "iin": "371559",
    "iin_details": "American Express",
    "pan": "10225201",
    "network": "NewNetwork",
    "check_digit": "8",
    "valid": true
}
```

#####DELETE
```shell script
curl -X DELETE \
  http://127.0.0.1:8000/creditcard/4/ \
  -H 'Authorization: Basic YWRtaW5AZXhhbXBsZS5jb206YWRtaW5wYXNz' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
```
Response
```shell script
Status: 204 No Content
Content-Length: 0
```


## validatecard
This endpoint lets you POST a credit card number in a json payload in the 'ccnumber' field without authorization.

#### HTTP Request

`POST http://localhost:8000/validatecard/`

Content-Type
```shell script
application/json
```

#### HTTP Response codes

Code | Description
---- | -----------
200  | Request successful
400  | Bad Request 

#### Payload Parameters

Parameter | Description
--------- | ----------- 
ccnumber | required for POST

#### Sending data

You can send data by posting it as json in the request body.

#####POST
```shell script
curl -X POST \
  http://127.0.0.1:8000/validatecard/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"network": "Visa"}'
```
Response
```shell script
Status: 200 OK
Content-Type: application/json
```
```json
{
    "ccnumber": "371559102252018",
    "valid": true,
    "mii": "3",
    "mii_details": "Banking & Financial (Visa, Switch, and Electron)",
    "iin": "371559",
    "iin_details": "American Express",
    "pan": "10225201",
    "network": "American Express",
    "check_digit": "8"
}
```

## gencard
This endpoint lets you POST a network in a json payload in the 'network' field without authorization and a randomly 
generated valid credit card will be returned.

#### HTTP Request

`POST http://localhost:8000/gencard/`

Content-Type
```shell script
application/json
```

#### HTTP Response codes

Code | Description
---- | -----------
200  | Request successful
400  | Bad Request 

#### Payload Parameters

Parameter | Description
--------- | ----------- 
network | required for POST

Valid network values

    Visa
    Discover
    JCB
    Diners Club
    China UnionPay
    Maestro
    American Express
    MasterCard

#### Sending data

You can send data by posting it as json in the request body.

#####POST
```shell script
curl -X POST \
  http://127.0.0.1:8000/validatecard/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"network": "Visa"}'
```
Response
```shell script
Status: 200 OK
Content-Type: application/json
```
```json
{
    "ccnumber": "4076078604777059",
    "valid": true,
    "mii": "4",
    "mii_details": "Banking & Financial (Mastercard and Bankcard)",
    "iin": "407607",
    "iin_details": "Visa",
    "pan": "860477705",
    "network": "Visa",
    "check_digit": "9"
}
```