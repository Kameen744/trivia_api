import os
from turtle import clear
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.api_prefix = '/api/v1'
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Heres a new question string",
            "answer": "Heres a new answer string",
            "difficulty": 1,
            "category": 3
        }

        self.new_question_fail = {
            "answer": "Heres a new answer string",
            "difficulty": 1,
            "category": 3
        }

        self.next_question = {
            "previous_questions": [1, 4, 20, 15],
            "quiz_category": {"type": "History", "id": "4"}
        }

        self.next_question_not_found = {
            "previous_questions": [1, 4, 20, 15],
            "quiz_category": {"type": "History", "id": "100"}
        }

        self.search_question = {
            "searchTerm": "a"
        }

        self.search_question_not_found = {
            "searchTerm": "---"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get(f'{self.api_prefix}/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertIn('1', data['categories'])

    def test_404_get_categories(self):
        res = self.client().get(f'{self.api_prefix}/categories')
        data = json.loads(res.data)
        self.assertNotIn('status', data)

    def test_get_paginated_questions(self):
        res = self.client().get(f'{self.api_prefix}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_404_get_paginated_questions_beyond_pages(self):
        res = self.client().get(f'{self.api_prefix}/questions?page=100')
        self.assertEqual(res.status_code, 404)

    def test_search_question(self):
        res = self.client().post(
            f'{self.api_prefix}/questions/search', json=self.search_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_404_search_question_string_not_in_questions(self):
        res = self.client().post(f'{self.api_prefix}/questions/search',
                                 json=self.search_question_not_found)
        data = json.loads(res.data)
        self.assertTrue(data['status'], 404)

    def test_insert_new_question(self):
        res = self.client().post(f'{self.api_prefix}/questions',
                                 json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['message'], 'Success')

    def test_500_insert_new_question_without_key_element(self):
        res = self.client().post(f'{self.api_prefix}/questions',
                                 json=self.new_question_fail)
        data = json.loads(res.data)
        self.assertTrue(data['status'], 500)

    def test_get_category_questions(self):
        res = self.client().get(f'{self.api_prefix}/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_404_category_questions_number_beyond_categories(self):
        res = self.client().get(f'{self.api_prefix}/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_next_question(self):
        res = self.client().post(
            f'{self.api_prefix}/quizzes', json=self.next_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', data['question'])

    def test_404_next_question(self):
        res = self.client().post(
            f'{self.api_prefix}/quizzes', json=self.next_question_not_found)
        data = json.loads(res.data)
        self.assertTrue(data['status'], 404)

    def test_delete_question(self):
        res = self.client().delete(f'{self.api_prefix}/questions/6')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['status'])

    def test_if_question_has_been_deleted(self):
        res = self.client().delete(f'{self.api_prefix}/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Resource Deleted')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
