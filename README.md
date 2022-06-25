# Getting Started

## Introduction

This is quiz application that have multiple category of questions that you can choose from and also allows selection of all so you can get questions from all categories.

Note - This is a Udacity API assignment which contains two part (Fronend) that uses react to call the (Backend) API and render the json result into webview.

Below are the instructions on how to start both the front and backend.

## Setup - Backend

Make sure you have python3, pip, python virtualenv and postgresql installed on your machine

1. In the project folder cd into backend and run `psql` then create database `CREATE DATABASE trivia`.
Now that you have created a database named `trivia` press `CTRL+C` to exit the psql CLI and run `psql -U username -d trivia -f trivia.psql` default username is (postgres)

2. Clone the repository and cd into the project directory
3. Create virtual environment - `python -m venv .venv`
4. Activate virtual environment - `.venv/Scripts/Activate`
5. Install required dependencies - `pip install -r requirements.txt`
6. Set Flask App and Environment - Windows: `$env:FLASK_APP='flaskr'  $env:FLASK_ENV='development'` Other-Os: `export FLASK_APP=flaskr` `export FLASK_ENV=development`
7. Run the api dev server - `flask run --reload --debugger`


## Setup - Frontend

1. Make sure you have nodejs installed on your machine
2. CD into frontend directory and run `npm install`
3. After installation completed run `npm start`

## API Endpoints

`Main URL - example - 'http://localhost:500'`

To get list of categories
`GET '/api/v1/categories'`

Result:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
Get list of paginated questions
`GET '/api/v1/questions?page=${integer}'`

Result:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

To add a new question send a post request with json data 

`POST '/questions'`

Request body:
```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

To search for a question make a post request

`POST '/questions/search'`

Request body:
```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
Result:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

Get a question based on a category by providing category_id
`GET '/api/v1/categories/${id}/questions'`

Result:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

Delete a question by passing the question_id
`DELETE '/api/v1/questions/${id}'`

Result:
```{}````

Get the next question by providing a list of previous questions and current category string

`POST '/api/v1/quizzes'`

Example of post body:
```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": "current category"   
}
```

Result:
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```
