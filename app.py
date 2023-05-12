"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/', methods=["GET"])
def home():
    return render_template('base.html')

@app.route('/api/cupcakes', methods=["GET"])
def list_all_cupcakes():
    """GET data about all cupcakes."""
    cupcakes_json = dict()
    cupcakes_json = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes_json)

@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def list_single_cupcakes(id):
    """GET data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id).serialize()
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """POST a new cupcake onto the database."""
    flavor = request.json.get('flavor')
    size = request.json.get('size')
    rating = request.json.get('rating')
    image = request.json.get('image')
    cupcake=Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    json_cupcake = jsonify(cupcake=cupcake.serialize())
    json_cupcake.status_code = 201
    return json_cupcake
    
@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """PATCHES some new properties over the old cupcake's stuff."""

    cupcake=Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('cupcake').get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('cupcake').get('size', cupcake.size)
    cupcake.rating = request.json.get('cupcake').get('rating', cupcake.rating)
    cupcake.image = request.json.get('cupcake').get('image', cupcake.image)
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """DELETEs a cupcake from the server."""
    Cupcake.query.get_or_404(id)
    cupcake=Cupcake.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify({'message': "Deleted"})