# Eccomerce-APi

An E-commerce API built using Django Rest Framework.

# Table of Contents
* [Introduction](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#introduction)
* [Features](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#features)
* [technology](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#technology)
* [Installation](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#installation)
  * [pip](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#pip)
  * [docker](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#dokcer)
* [Next Steps](https://github.com/ronin1777/Eccomerce-APi/tree/main?tab=readme-ov-file#next-steps)

# Introduction
This is an e-commerce API built using Django REST Framework (DRF). It allows you to (CRUD) products, users, orders, and order items base on Entity-Attribute-Value Model.

# Features
* Django 4.2 & Python 3.11
* Install via Pip or Docker
* Implement Entity Attribute Value model(EAV) 
* Authentication via JWT
* Media storage using Amazon S3
* Create Multiple Wishlists
* Rating for product

# technology
* Celery
* Postgres
* JWT
* Django Rest Framework
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
  (.venv) $ python manage.py makemigrations
  (.venv) $ python manage.py migrate
  (.venv) $ python manage.py createsuperuser
  (.venv) $ python manage.py runserver
  # Load the site at http://127.0.0.1:8000
  ```
  ### dokcer
  First in project root Create a directory named scripts and inside it create a file named run.sh with the same content:
```
#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
then run docker-compose
  ```
  docker-compose up -d --build
  ```
# Next Steps
If you want to use Docker, follow these steps:
* Add environment variables:
  > 1. server: docker
  > 2. configuration files: select docker-compose file
  > 3. sevice: select app
  > 4. Next and create
* Enable Django support(pycharm):
  > 1. go to Languages & Frameworks and select Django
  > 2. Django project root: select crs as root
  > 3. settings: go to src/shop/envs and select development.py
* Run &Dbuge Configurations:
  > 1. edit configuration add Djnago server
  > 2. Host: 0.0.0.0
  > 3. python interpereter: select Remote python Docker compose(that environment you created it)
> [!NOTE]
> Django support Available only in PyCharm Professional 

