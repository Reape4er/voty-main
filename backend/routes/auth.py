from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from models import Users, db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        RegisterData = request.get_json()

        user = Users(
            firstname=RegisterData["firstName"],
            surname=RegisterData["lastName"],
            patronymic=RegisterData["middleName"],
            email=RegisterData["email"],
            role=RegisterData["role"],
        )
        user.password = RegisterData["password"]

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Регистрация прошла успешно"}), 201
    except Exception as e:
        print(f"Error registering: {e}")
        return jsonify({"error": "Ошибка регистрации"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    login_data = request.get_json()

    email = login_data.get("email")
    password = login_data.get("password")

    user = Users.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"message": "Invalid credentials"}),401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    return jsonify(access_token=access_token)


@auth_bp.route("/check_token", methods=["GET"])
@jwt_required()
def check_token():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)

    return (
        jsonify(
            id=user.id,
            firstName=user.firstname,
            lastName=user.surname,
            middleName=user.patronymic,
            email=user.email,
            role=user.role,
        ),
        200,
    )
