from ast import Try
import json
from sys import prefix
from flask import Blueprint, Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from error_handler import ApiError

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10
PREFIX = "/api/v1"

# trivia_bp = Blueprint('trivia_bp', __name__, url_prefix=PREFIX)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # app.register_blueprint(trivia_bp, url_prefix=PREFIX)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}},
         supports_credentials=None)
    setup_db(app)

    # """
    # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    # """

    # """
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    # """

    @app.after_request
    def add_headers(response):
        http_origin = request.environ['HTTP_ORIGIN']
        response.headers['Access-Control-Allow-Origin'] = f'{http_origin}'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, ')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # """
    # Format question categories
    def format_categories(categories):
        data = {}

        for category in categories:
            data[category.id] = category.type

        return data

    # Format questions
    def format_questions(questions):
        data = []

        for question in questions:
            data.append(Question.format(question))

        return data

    # Raise errors
    def raise_error(code=500):

        if code == 500:
            raise ApiError('Server Error', code)

        elif code == 410:
            raise ApiError('Resource Deleted', code)

        elif code == 404:
            raise ApiError('Not Found', code)

    # Check resource and throw erorr if not found
    def check_resource(resource, code):
        if not resource:
            raise_error(code)

    @app.route(f'{PREFIX}/')
    def index():
        return "The URL for this page is {}".format(url_for("index"))

    @app.route(f'{PREFIX}/categories')
    def get_categories():

        categories = Category.query.all()

        check_resource(categories, 404)

        response_data = {"categories": format_categories(categories)}

        return jsonify(response_data)

    # """
    # @TODO:
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    @app.route(f'{PREFIX}/questions')
    def get_paginated_questions():

        page = request.args.get('page', 1, type=int)

        questions = Question.query.paginate(
            page=page, per_page=QUESTIONS_PER_PAGE)

        check_resource(questions, 404)

        categories = Category.query.all()

        all_formated_questions = format_questions(questions.items)
        all_formated_categories = format_categories(categories)

        response_data = {
            "questions": all_formated_questions,
            "totalQuestions": len(all_formated_questions),
            "categories": all_formated_categories,
            "currentCategory": "History"
        }

        return jsonify(response_data)

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # """

    # """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    @app.route(f'{PREFIX}/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        check_resource(question, 410)

        Question.delete(question)

        return jsonify({'id': question.id, 'status': 200})

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # """

    # """
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    @app.route(f'{PREFIX}/questions', methods=['POST'])
    def add_new_question():
        try:
            request_data = request.get_json()

            question = Question(
                question=request_data['question'],
                answer=request_data['answer'],
                category=request_data['category'],
                difficulty=request_data['difficulty']
            )

            Question.insert(question)

            return jsonify({'status': 200, 'message': 'Success'})
        except:
            raise_error(500)
    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # """

    # """
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.
    @app.route(f'{PREFIX}/questions/search', methods=['POST'])
    def search_question():

        request_data = request.get_json()
        search_term = f"%{request_data['searchTerm']}%"

        questions = Question.query.filter(
            Question.question.ilike(search_term)).all()

        check_resource(questions, 404)

        formated_questions = format_questions(questions)

        return jsonify({
            "questions": formated_questions,
            "totalQuestions": len(formated_questions),
            "currentCategory": "Entertainment"
        })
    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # """

    # """
    # @TODO:
    # Create a GET endpoint to get questions based on category.

    @app.route(f'{PREFIX}/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()

        check_resource(questions, 404)

        all_formated_questions = format_questions(questions)

        response_data = {
            "questions": all_formated_questions,
            "totalQuestions": len(all_formated_questions),
            "currentCategory": "History"
        }

        return jsonify(response_data)

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # """

    # """
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.
    @app.route(f'{PREFIX}/quizzes', methods=['POST'])
    def get_quiz_question():
        request_data = request.get_json()

        previous_qeustions = request_data['previous_questions']
        current_category = request_data['quiz_category']

        # Filter questions based on category and filter previous questions
        if current_category['type'] == 'click':
            question_by_category = Question.query.filter(
                Question.id.notin_(previous_qeustions)).all()
        else:
            question_by_category = Question.query.filter(
                Question.category == current_category['id']).filter(
                Question.id.notin_(previous_qeustions)).all()

        # throw 404 if there's no question
        if len(question_by_category) > 0:
            # Pick random question
            random_question = Question.format(
                random.choice(question_by_category))
        else:
            raise_error(404)

        return jsonify({"question": random_question})

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # """

    # """
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # """

    @app.errorhandler(ApiError)
    def handle_api_errors(error):
        return error.to_json()

    return app
