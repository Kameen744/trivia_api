# Getting Started

## Introduction

This is quiz application that have multiple category of questions that you can choose from and also alows selection of all so you can answer questions from all categories.

Note - This is a Udacity API assignment which contains two part (Fronend) that uses react to call the (Backend) API and render the json result into webview.

## Setup - Backend

1. Make sure you have python3, pip, python virtualenv installed on you machine
2. Clone the repository and cd into trivia directory
3. Create virtual environment - `python -m venv .venv`
4. Activate virtual environment - `.venv/Scripts/Activate`
5. Install required dependencies - `pip install -r requirements.txt`
6. Set App

## Setup - Frontend

1. Make sure you have nodejs installed on your machine
2. CD into frontend directory and run `npm install`
3. After installation completed run `npm start`

## API Endpoints

`Main URL - example - 'http://localhost:500'`

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

`DELETE '/api/v1/questions/${id}'`

Result:
```{}````


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
