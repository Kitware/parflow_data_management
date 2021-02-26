# Initial Setup

## Prerequisites

### PostgreSQL
PostgreSQL is used on the back-end for database management. We'll also need some other libraries so Django can communicate with the database.
These can all be installed via package manager. For Ubuntu, use the following command:
```
sudo apt install python-dev libpq-dev postgresql postgresql-contrib
```

### Redis
Redis is used by Django channels as a back-end for communicating between instances. Unfortunately, the version available through `apt` is out of date (version >= 5.0 is required). For linux, installation instructions can be found at https://redis.io/download#installation.

### RabbitMQ
RabbitMQ is used by Celery in a similar manner as Redis. Simple instructions for installing and configuring RabbitMQ can be found at the following link, but will be repeated below: https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html#installing-rabbitmq-on-ubuntu-1604

Install `erlang` and `rabbitmq-server`:
```
sudo apt-get install -y erlang
sudo apt-get install rabbitmq-server
```

### Python Packages
Several Python packages are required. They can easy be installed using `pip` to install this repo as a Python package.

Clone this repo or download the source files. To easily clone:
```
git clone https://github.com/tao558/parflow_data_management.git
```

Navigate to the project root. Then, to install this package and all dependencies:
```
pip install -e parflow_data_management/
```

## Create a PostgreSQL Database
Django needs a database to store the application's models. Simple instructions can be found at https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04. The instructions are also copied below.

On the machine that you would like to host the database, first switch over to the postgres user:
```
sudo su - postgres
```

Start a PostgreSQL session:
```
psql
```

Create a database for Django to use:
```
CREATE DATABASE <my_db>;
```
Where ```my_db``` is the name of your database. Remember this value.

Create a new user for Django to interact with the database:
```
CREATE USER <my_user> WITH PASSWORD '<my_pass>';
```
Where ```my_user``` is the name of the new user and ```my_pass``` is the user's secure password.
Remember both of these for later.

Set some other misc. settings for our database. The first line sets the encoding to UTF-8, and the second prevents "dirty reads":
```
ALTER ROLE <my_user> SET client_encoding TO 'utf8';
ALTER ROLE <my_user> SET default_transaction_isolation TO 'read committed';
```

Grant the requisite privelages to our new user:
```
GRANT ALL PRIVILEGES ON DATABASE <my_db> TO <my_user>;
```

If you wish to run tests, an additional permission is required:
```
ALTER USER <my_user> CREATEDB;
```
This allows Django to create temporary databases when running tests.

Leave the PostgreSQL session:
```
\q
```

Switch out of the `postgres` user's bash session:
```
exit
```

## Setting Up a Redis Server
To run a redis server, navigate to the install directory from the instructions above and run `src/redis-server`.

## Setting Up a RabbitMQ Server
Start `RabbitMQ`:
```
systemctl enable rabbitmq-server
systemctl start rabbitmq-server
```
Check that the service is running with:
```
systemctl status rabbitmq-server
```

## Start a Celery worker
From the root directory of the project, run:
```
celery -A parflow_data_management worker -l INFO
```

## Passing Sensitive Settings Variables to Django via .env File
It's convention to store any sensitive configuration data required by Django in a `.env` file in the project root.
This keeps sensitive variables like the `DJANGO_SECRET_KEY` from being shared, while also allowing the application source code to be public. See the list of required and optional variables and their descriptions below:
|         Variable         |                     Description                    |
| -------------------------|----------------------------------------------------|
| ``DJANGO_SECRET_KEY``    |     Required. Encryption key for this application. |
| ``DATABASE_NAME``        |     Required. Name of the database for Django to use. `<my_db>` in the above example. |
| ``DATABASE_USER``        |     Required. User for Django to interact with the database. `<my_user>` in the above example. |
| ``DATABASE_PASSWORD``    |     Required. Password to the database. `<my_pass>` in the above example. |
| ``DATABASE_HOST``        |     Optional. IP address that the database is hosted on. Defaults to `localhost` |
| ``DATABASE_PORT``        |     Optional. Port that the database is hosted on at the above IP address. Defaults to `5432` |
| ``DJANGO_ALLOWED_HOSTS`` |     Required for production and test. List of allowed hosts for the application to run on. Default to `["localhost", "0.0.0.0", "127.0.0.1"]` for `local` environments. Read in as a comma-separated list (e.g. `DJANGO_ALLOWED_HOSTS=host1,host2`) |
| ``DJANGO_ADMIN_URL``     |     Required for production. URL for admin page. Defaults to `admin/` for local environments. |
| ``REDIS_HOST``           |     Required. IP address for the Redis server used by Django Channels and the cache backend. Defaults to `127.0.0.1:6379` |
| ``CELERY_BROKER_URL``    |     Required. URL for the broker service used by celery for asynchronous tasks. Defaults to `amqp://127.0.0.1:5672` |


Valid `DJANGO_SECRET_KEY` values can be generated via the `get_random_secret_key` function from the `django.core.management.utils` submodule. For example, to generate a new secret key, simply run:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
from the terminal, or
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
from an interactive python session. Either way, the returned value can be copied and pasted into the .env file.

# Execution
## Development
Note: These instructions are *not* suited for a production environment.

To run the application, first check for any new migrations:
```
./manage.py makemigrations --settings=config.settings.<environment_type>
```

Then apply those migrations:
```
./manage.py migrate --settings=config.settings.<environment_type>
```

Then start the application:
```
./manage.py runserver <IP:port> --settings=config.settings.<environment_type>
```
Where:
* `IP` is the IP address to host the application. Defaults to `127.0.0.1`.
* `port` is the corresponding port. Defaults to `8000`.
* `<environment_type>` is `local`, `test`, or `production`, depending on which settings you would like to use. This is similar to python dependency install step above.

## Testing
First, make sure that the DATABASE_USER of your choice, `<my_user>`, has permission to create and remove databases. See the "Creating a PostgreSQL Database" section.

To run the tests, simply run `./manage.py test --settings=config.settings.test` from the root directory of the project.

## Develop with Docker

### Initial Setup
1. Run `docker-compose run --rm django ./manage.py migrate`
2. Run `docker-compose run --rm django ./manage.py createsuperuser`
   and follow the prompts to create your own user

### Run Application
1. Run `docker-compose up`
2. Access the site, starting at http://localhost:8000/admin/
3. When finished, use `Ctrl+C`

### Application Maintenance
Occasionally, new package dependencies or schema changes will necessitate
maintenance. To non-destructively update your development stack at any time:
1. Run `docker-compose pull`
2. Run `docker-compose build`
3. Run `docker-compose run --rm django ./manage.py migrate`

# Submitting To a Remote Machine

## Setup
1. Create a new project from the admin site.
2. Create a new simulation from the admin site, pointing it to the cluster in step 1. "Arguments" is the command to be run on the remote machine.
3. Create a new cluster for the remote resource from the admin site.
4. Create a new assetstore from the admin site and assign it to the cluster create in the previous step.
5. Generate a new key_pair from key-generation-test/. Remember the password and id, and copy the public key to the authorized_keys file of the remote machine. If doing this manually, be sure to follow the structure of an authorized_keys file.
6. Create a new authorized_key instance from the admin site and point it to the cluster and key_pair previously created.
7. Visit the endpoint test-unlock-key_pair/ and enter your password and key id to unlock. This will need to be done after each login.

## Job / Command Execution
To test that a cluster has been configured properly, visit execute/ and provide the cluster id. This will run `ls` on the remot machine and display the output.

To submit a simulation, visit the endpoint test-submit and fill out the necessary fields.
