# Eccomerce-APi

An E-commerce API built using Django Rest Framework.

# Table of Contents
* [Introduction](https://github.com/ronin1777/Eccomerce-APi/blob/main/README.md#introduction)
* [Features](https://github.com/ronin1777/H_dubbed/blob/main/README.md#features)
* [technology](https://github.com/ronin1777/H_dubbed/blob/main/README.md#technology)
* [Installation](https://github.com/ronin1777/H_dubbed/blob/main/README.md#setup-and-run)
  * [pip](https://github.com/ronin1777/Eccomerce-APi/blob/main/README.md#pip)
  * [docker](https://github.com/ronin1777/Eccomerce-APi/blob/main/README.md#dokcer)
* [Next Steps]()

# Introduction
This is an e-commerce API built using Django REST Framework (DRF). It allows you to (CRUD) products, users, orders, and order items base on Entity-Attribute-Value Model.

# Features
* Django 4.2 & Python 3.11
* Install via Pip or Docker
* Authentication via JWT
* Media storage using Amazon S3
* create Multiple Wishlists
* 

# technology
* Celery
* Postgres
* JWT
* Django Rest Framework
* Redis
* docker
# Installation
Eccomerce-APi can be installed via Pip or Docker. To start, clone the repo to your local computer and change into the proper directory.
```
git clone https://github.com/ronin1777/Eccomerce-APi.git
```
  ### pip
  ```
  python -m venv .venv
  # Windows
  .venv\Scripts\Activate
  
  macOS
  source .venv/bin/activate
  
  (.venv) $ pip install -r requirements.txt
  (.venv) $ python manage.py migrate
  (.venv) $ python manage.py createsuperuser
  (.venv) $ python manage.py runserver
  # Load the site at http://127.0.0.1:8000
  ```
  ### dokcer
  ```
  docker-compose up -d --build
  ```
# Next Steps
If you want to use Docker, follow these steps:
* Add environment variables:
  > 1. server: docker
  2. configuration files: select docker-compose file
  3. sevice: select app
  4. Next and create
* Enavle Django support(pycharm):
  1. go to Languages & Frameworks and select Django
  2. Django project root: select crs as root
  3. settings: go to src/shop/envs and select development.py
* Run &Dbuge Configurations:
  1. edit configuration add Djnago server
  2. Host: 0.0.0.0
  3. python interpereter: select Remote python Docker compose(that environment you created it)

