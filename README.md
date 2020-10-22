# Initial Setup

## Prerequisites

### PostgreSQL
PostgreSQL is used on the back-end for database management. We'll also need some other libraries so Django can communicate with the database. 
These can all be installed via package manager. For Ubuntu, use the following command:
```
sudo apt install python-dev libpq-dev postgresql postgresql-contrib
```

### Python Packages
Several Python packages are required. They can easy be installed using `pip` and one of the requirements files in the `requirements` subdirectory.

Clone this repo or download the source files. To easily clone:
```
git clone https://github.com/tao558/parflow_data_management.git
```

Navigate to the project root. Then, to install the python packages, run:
```
pip install -r requirements/<local | production>.txt
```
Choose the requirements file that corresponds to the environment that the application will be run in (e.g., for local development, choose `local.txt`)

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

Leave the PostgreSQL session:
```
\q
```

Switch out of the `postgres` user's bash session:
```
exit
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
| ``DJANGO_ALLOWED_HOSTS`` |     Required for production. List of allowed hosts for the application to run on. Default to an empty list for `production`, and `["localhost", "0.0.0.0", "127.0.0.1"]` for `local` environments. Read in as a comma-separated list (e.g. `DJANGO_ALLOWED_HOSTS=host1,host2`) |
| ``REDIS_URL``            |     Required for production. `<ip:port>` value where ip is the IP address of the Memcached daemon used for cache management, and `port` is the port on which the daemon is running |
| ``DJANGO_ADMIN_URL``     |     Required for production. URL for admin page. Defaults to `admin/` for local environments. |


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
./manage.py makemigrations
```

Then apply those migrations:
```
./manage.py migrate
```

Then start the application:
```
./manage.py runserver <IP:port> --settings=config.settings.<environment_type>
```
Where:
* `IP` is the IP address to host the application. Defaults to `127.0.0.1`.
* `port` is the corresponding port. Defaults to `8000`.
* `<environment_type>` is either `local` or `production`, depending on which settings you would like to use. This is similar to python dependency install step above.
