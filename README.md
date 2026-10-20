# Student Management API

## Project Overview
The Student Management API is a Python application developed using Flask.
It provides REST API endpoints to manage student records.

## Features
- Create student records
- Retrieve student information
- Update student details
- Delete student records
- Test API endpoints using Postman

## Technologies Used
- Python
- Flask
- REST API
- Postman
- JSON

## Installation

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create a virtual environment:

   python -m venv venv

4. Activate the virtual environment on Windows PowerShell:

   .\venv\Scripts\Activate.ps1

5. Install dependencies:

   pip install -r requirements.txt

6. Run the application:

   python app.py

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Check API status |
| POST | /students | Add a student |
| GET | /students | Retrieve all students |
| PUT | /students/<id> | Update a student |
| DELETE | /students/<id> | Delete a student |

## API Testing
The endpoints were tested using Postman.

## Author
Udita