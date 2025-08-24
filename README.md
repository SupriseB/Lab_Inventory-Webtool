# Laboratory Inventory Management Webtool

A Django-based web application for laboratories to manage and track inventory items. This project allows users to securely manage categories and items, track quantities, and generate reports.

# Features

# User Authentication

Registration, login, logout, and profile management.

JWT authentication for API endpoints.

Secure password hashing and CSRF protection.

# Inventory Management

CRUD operations for Categories and Items.

Items include fields: name, description, quantity, purchase date, location, category, and reorder level.

Users can only manage their own data.

# Dashboard

Summary statistics: total items, total quantity, low-stock alerts.

Category distribution charts using Chart.js.

# Reporting & Export

Export inventory and low-stock items to CSV and PDF.

Styled PDF tables for professional reports.
