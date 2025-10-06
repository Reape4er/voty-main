from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from models import  Events, Nominations, RatingEvaluations, db


criteria_bp = Blueprint("criteria", __name__)


@criteria_bp.route("/events/<event_id>/criteria", methods=["GET"])
def get_criteria(event_id):
    event = Events.query.get(event_id)
    #проверка на Арифметический метод
    if event.evaluation_method == 0:
        criteria = event.arithmetics_parameters
        return jsonify([c.to_dict() for c in criteria]), 200
    elif event.evaluation_method == 1:
        #ДОДЕЛАТЬ ФУНКЦИЮ
        nomination_id = request.args.get('nomination_id', type=int)
        expert_id = request.args.get('expert_id', type=int)
        rating_evaluations = RatingEvaluations.query.filter_by(nomination_id=nomination_id, expert_id=expert_id).all()
        criteria = event.ratings_parameters[0]
        response = criteria.to_dict()
        print(response)
        response['rating_table'] = [r.to_dict() for r in rating_evaluations]
        print(response)
        return jsonify(response), 200
    return jsonify(), 403