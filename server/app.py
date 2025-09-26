#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User, ArticlesSchema

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-for-development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    def get(self):
        articles = [ArticlesSchema().dump(article) for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):
    def get(self, id):
        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1

        if session['page_views'] <= 3:
            article = Article.query.filter(Article.id == id).first()
            article_json = ArticlesSchema().dump(article)

            return make_response(article_json, 200)

        return {'message': 'Maximum pageview limit reached'}, 401

class Login(Resource):
    def post(self):
        # Get username from request JSON
        data = request.get_json()
        if not data or 'username' not in data:
            return {'error': 'Username is required'}, 400
            
        username = data.get('username')
        
        # Find user by username (usernames are unique)
        user = User.query.filter_by(username=username).first()
        
        if user:
            # Set session user_id to the user's id
            session['user_id'] = user.id
            
            # Return user as JSON with 200 status
            return {
                'id': user.id,
                'username': user.username
            }, 200
        else:
            # Return error if user not found
            return {'error': 'User not found'}, 404

class Logout(Resource):
    def delete(self):
        # Remove user_id from session
        session.pop('user_id', None)
        
        # Return no data with 204 status
        return {}, 204

class CheckSession(Resource):
    def get(self):
        # Get user_id from session
        user_id = session.get('user_id')
        
        if user_id:
            # If session has user_id, return user as JSON with 200 status
            user = User.query.get(user_id)
            if user:
                return {
                    'id': user.id,
                    'username': user.username
                }, 200
        
        # If no user_id in session or user not found, return 401
        return {}, 401

api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)