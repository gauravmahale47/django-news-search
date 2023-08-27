# Django News Search Web Application

This is a Django-based web application that allows users to search for news articles and view their search history.

## Features

- User registration and login system.
- User authentication and authorization using Django's built-in features.
- Search for news articles based on keywords using the [News API](https://newsapi.org/).
- Store and display search history for each user.
- Sort search results by date published.

## Installation and Setup

1. Clone the repository to your local machine:

    ```
    https://github.com/gauravmahale47/django-news-search.git
    cd django-news-search/
    ```

2. Create a virtual environment and install dependencies
   
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Configure the Database

    - Update the DATABASES settings in settings.py with your database configuration.
    - Or create a file named as db.sqlite3 and use that database


4. Create a .env File
    - Create a file named .env in the same directory as settings.py. Add the following line to the .env file.
    
    ```
    NEWS_API_KEY=your_news_api_key_here
    ```

5. News API Integration

    
    - This project integrates the News API to fetch news articles based on user-entered keywords. You will need to sign up on the News API website to get an API key.

    - Sign up on the News API website to obtain an API key.
    - Add your News API key to the .env file.


6. Apply Migrations

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```


7. Create a Superuser
   
    ```
    python manage.py createsuperuser
    ```


8. Run the Development Server
    ```
    python manage.py runserver
    ```


9. Access the application in your web browser at http://127.0.0.1:8000/