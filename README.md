# Laboratory Inventory Management Webtool

A Django-based web application designed to help laboratories efficiently manage and track inventory items. This tool allows users to securely manage categories and items, monitor quantities, and generate reports.

<img width="1880" height="1011" alt="Screenshot 2025-08-29 215239" src="https://github.com/user-attachments/assets/ad463500-2186-446c-898f-07c486e5324b" />


# Features

User Authentication

Registration, login, logout, and profile management.

JWT authentication for API endpoints.

Secure password hashing and CSRF protection.

# Inventory Management

CRUD operations for Categories and Items.

Item details include: name, description, quantity, purchase date, location, category, and reorder level.

Users can only manage their own data.

# Dashboard

Summary statistics: total items, total quantity, low-stock alerts.

Category distribution charts using Chart.js.

Reporting & Export

Export inventory data in CSV/PDF format.

# Installation Prerequisites

Python 3.10+

Django 5.2+

pip (Python package manager)

# Steps

Clone the repository:

git clone https://github.com/SupriseB/Lab_Inventory-Webtool.git
cd Lab_Inventory-Webtool


Create and activate a virtual environment:

python -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Access the application at:

http://127.0.0.1:8000/

# Demo

Experience the Lab Inventory Webtool in action: https://www.loom.com/share/fc190a1bbf1d487598a65cd6b6975d9c?sid=e0f93e90-b34a-4ce9-916c-d3de097566fb


# Technology Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript (Chart.js)

Authentication: JWT

Database: SQLite (default)


# Contact

SupriseB – suprisebaloyi17@gmail.com

GitHub: https://github.com/SupriseB
