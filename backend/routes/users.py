from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required

from models import Users, Nominations

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
@jwt_required()
def get_user():
    user_id = request.args.get("id")

    if user_id:
        user = Users.query.get(user_id)

    if not user:
        abort(404, description="Пользователь не найден.")

    return jsonify(
        {
            "firstname": user.firstname,
            "surname": user.surname,
            "patronymic": user.patronymic,
            "email": user.email,
            "role": user.role,
        }
    )


@users_bp.route("/users/experts", methods=["GET"])
@jwt_required()
def get_all_experts():
    experts = Users.query.filter_by(role='expert').all()
    
    if not experts:
        abort(404, description="Эксперты не найдены.")

    return jsonify([expert.to_dict() for expert in experts])

@users_bp.route("/nominations/<int:nomination_id>/experts", methods=["GET"])
@jwt_required()
def get_experts_by_nomination_id(nomination_id):
    if nomination_id:
        experts = Nominations.query.get(nomination_id).users
    if not experts:
        abort(404, description="Эксперты не найдены.")

    return jsonify([expert.to_dict() for expert in experts])