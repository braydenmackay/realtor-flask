from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ybnubyzlotvoqq:28d26e4e1365d94072a6aee691c3fcb806d49ecdb81681e5d22f72e587dc06c6@ec2-18-210-214-86.compute-1.amazonaws.com:5432/d9mdnpua10nig0'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    brokerage = db.Column(db.String(100))
    state = db.Column(db.String(2))
    city = db.Column(db.String(100))
    post_code = db.Column(db.String(5))
    phone = db.Column(db.String(13))
    realtor_email = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    rating = db.Column(db.Float)
    review = db.Column(db.Text)

    def __init__(self, first_name, last_name, brokerage, state, city, post_code, phone, realtor_email, user_email, rating, review):
        self.first_name = first_name
        self.last_name = last_name
        self.brokerage = brokerage
        self.state = state
        self.city = city
        self.post_code = post_code
        self.phone = phone
        self.realtor_email = realtor_email
        self.user_email = user_email
        self.rating = rating
        self.review = review

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'brokerage', 'state', 'city', 'post_code', 'phone', 'realtor_email', 'user_email', 'rating', 'review')

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@app.route('/review', methods=["POST"])
def add_review():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    brokerage = request.json['brokerage']
    state = request.json['state']
    city = request.json['city']
    post_code = request.json['post_code']
    phone = request.json['phone']
    realtor_email = request.json['realtor_email']
    user_email = request.json['user_email']
    rating = request.json['rating']
    review = request.json['review']

    new_review = Review(first_name, last_name, brokerage, state, city, post_code, phone, realtor_email, user_email, rating, review)

    db.session.add(new_review)
    db.session.commit()

    item = Review.query.get(new_review.id)

    return review_schema.jsonify(item)

@app.route('/reviews', methods=["GET"])
def get_reviews():
    all_reviews = Review.query.all()
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)

@app.route('/review/<id>', methods=["GET"])
def get_review(id):
    item = Review.query.get(id)
    return review_schema.jsonify(item)

@app.route('/review/<id>', methods=["PUT"])
def update_review(id):
    item = Review.query.get(id)
    item.first_name = request.json['first_name']
    item.last_name = request.json['last_name']
    item.brokerage = request.json['brokerage']
    item.state = request.json['state']
    item.city = request.json['city']
    item.post_code = request.json['post_code']
    item.phone = request.json['phone']
    item.realtor_email = request.json['realtor_email']
    item.user_email = request.json['user_email']
    item.rating = request.json['rating']
    item.review = request.json['review']

    db.session.commit()
    return review_schema.jsonify(item)

@app.route('/review/remove/<id>', methods=["DELETE"])
def delete_review(id):
    item = Review.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return review_schema.jsonify(item)

if __name__ == "__main__":
    app.run(debug=True)