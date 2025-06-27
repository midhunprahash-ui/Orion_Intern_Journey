# Username Matcher Web App

This Django application helps identify **unauthorized usernames** by comparing a list of provided usernames (typically from a CSV file) against a predefined set of authorized employees. It's designed to provide a web interface for easy uploading, processing, and viewing of the matching results.

---

## Features

- **CSV Upload**: Easily upload CSV files containing usernames.
- **Username Matching**: Utilizes string matching libraries like `thefuzz` and `jellyfish` to find similar or potentially unauthorized usernames.
- **Authentication**: Secure access to the application via Django's built-in authentication system.
- **Web Interface**: User-friendly web pages for interacting with the application.

---

## Technologies Used

- **Django**: Web framework
- **Python**: Programming language
- **Pandas**: Data manipulation (for CSV processing)
- **thefuzz**: Library for string matching
- **jellyfish**: Library for approximate string matching algorithms
- **HTML/CSS/JavaScript**: Frontend development

---

## Setup and Installation

Follow these steps to get the project up and running on your local machine:

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-name>  # e.g., cd username_matcher_project

```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Migrations

``` bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Start the Development Server

``` bash
python manage.py runserver
```

