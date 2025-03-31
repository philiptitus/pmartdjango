# PMart Backend

This is the backend service for PMart, an e-commerce platform that i made to sell my tech services as  freelance. It is built with Django and Django REST Framework. The frontend of this project is built on NextJs.

## Tech Stack

- Python 3.x
- Django 5.0.2
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.1
- SQLite Database

## Prerequisites

- Python 3.x installed
- pip (Python package manager)

## Setup Instructions

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (if available)
   - Configure your environment variables in `.env`

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

The backend server will be available at `http://localhost:8000`

## API Documentation

The API documentation is available at `/api/docs/` when the server is running.

## Project Structure

- `ecommerce/` - Main application directory
- `media/` - Directory for user-uploaded files
- `manage.py` - Django's command-line utility for administrative tasks
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked in git)

## Development

- The backend uses Django REST Framework for API development
- CORS is configured to allow frontend requests
- SQLite is used as the database for development 
