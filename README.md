# django_empathy_laboratory
Empathy Lab "Lab Log" website written in Django.

----

This web application creates an online lablog, where users can browse available experiments, manage their accounts and create new records.

The main features that have currently been implemented are:

* There are models for experiments, records, stimulate, feedback and subjects.
* Users can view list and detail information for experiments and subjects.
* Admin users can create and manage models. The admin has been optimized (the basic registration is present in admin.py, but commented out).


# EmpathyLab

Installation and running on developer's machine
-----------------------------------------------

1. Instal `postgresql-devel` and `python3-devel` packages if you are using Fedora, or `postgresql-dev` and `python3-dev` on Ubuntu:
    ```sh
    sudo dnf install postgresql-devel python3-devel
    ```
1. Clone repository:
    ```sh
    git clone https://github.com/raylab/EmpathyLab.git
    ```
1. Go to source root:
    ```sh
    cd EmpathyLab
    ```
1. Create virtualenv for dependencies:
    ```sh
    python3 -m venv .venv
    ```
1. Activate virtualenv in your shell:
    ```sh
    source .venv/bin/activate
    ```
1. Install requirements using `pip`:
    ```sh
    pip install -r ./requirements.txt
    ```
1. Create database schema:
    ```sh
    ./manage.py migrate
    ```
1. Collect static files:
    ```sh
    ./manage.py collectstatic
    ```
1. Create superuser:
    ```sh
    ./manage.py createsuperuser
    ```
1. Run `redis` using for example `docker`:
    ```sh
    docker pull redis
    docker run --rm -p127.0.0.1:6379:6379 --name some-redis -d redis
    ```
1. Run application:
    ```sh
    ./manage.py runserver
    ```
