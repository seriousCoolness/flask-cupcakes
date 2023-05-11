"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template
from requests import request, Request, Response
from models import db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/api/cupcakes', methods=["GET"])
def list_all_cupcakes():
    """GET data about all cupcakes."""
    return cupcakes_json

@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def list_single_cupcakes(id):
    """GET data about a single cupcake."""
    return cupcake_json

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """POST a new cupcake onto the database."""
