# Eccomerce-APi

An E-commerce API built using Django Rest Framework.

# Table of Contents
* [Introduction](https://github.com/ronin1777/Eccomerce-APi/blob/main/README.md#introduction)
* [Features](https://github.com/ronin1777/H_dubbed/blob/main/README.md#features)
* [technology](https://github.com/ronin1777/H_dubbed/blob/main/README.md#technology)
* [How to use](https://github.com/ronin1777/H_dubbed/blob/main/README.md#setup-and-run)

# Introduction
This is an e-commerce API built using Django REST Framework (DRF). It allows you to (CRUD) products, users, orders, and order items base on Entity-Attribute-Value Model.

# Features
* Authentication via JWT
* Media storage using Amazon S3
* 

# technology
* Celery
* Postgres
* JWT
* Django Rest Framework
* Redis
* docker
# Setup and Run
1. Clone the repo:
```python
git clone https://github.com/ronin1777/H_dubbed.git
```
2. Configure a virtual
```python
python3 -m venv .venv
```
3. install -r requirements
```python
pip install -r requirements.txt
```
4. set up database
```python
python3 manage.py makemigrations
python3 manage.py migrate
```

