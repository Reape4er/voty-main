from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from models import  Events, NominationResults, Nominations, RatingEvaluations, db
from utils import arithmetic_calculate, rating_calculate
result_bp = Blueprint("result", __name__)

@result_bp.route("/result", methods=["POST"])
@jwt_required()
def create_nomination_result():
    data = request.get_json()
    nomination_id = data.get('nomination_id')
    evaluation_method = Nominations.query.get(nomination_id).events.evaluation_method
    if evaluation_method == 0:
        result = arithmetic_calculate(nomination_id)
    elif evaluation_method == 1:
        result = rating_calculate(nomination_id)
    if not result:
        return jsonify(),500
    return jsonify(),200

@result_bp.route("/result", methods=["GET"])
@jwt_required()
def get_nomination_results():
    """
    Получение результатов подсчёта рейтинга / очков для указанной номинации.

    Request parameters:
        - nomination_id: id необходимой номинации.
    """

    nomination_id = request.args.get("nomination_id")
    print(nomination_id)
    if not nomination_id:
        return jsonify({"error": "Не указан id номинации."}), 400

    nomination_results = NominationResults.query.filter(
        NominationResults.nomination_id == nomination_id
    ).all()
    print(nomination_results)
    if not nomination_results:
        return (
            jsonify(
                {"error": "Результаты не найдены или номинация ещё не завершилась."}
            ),
            400,
        )

    return (jsonify([nomination_result.to_dict() for nomination_result in nomination_results]),200)

@result_bp.route("/result", methods=["PUT"])
@jwt_required()
def update_results():
    data = request.get_json()
    print(data)
    try:    
        for result in data:
            print(result)
            result_id = result['id']
            if not result_id:
                return jsonify({"error": "Result ID is required."}), 400

            result_record = NominationResults.query.get(result_id)
            if not result_record:
                return jsonify({"error": "Result not found."}), 404

            # Update fields if they are in the request, except 'result'
            if 'additional_score' in result:
                result_record.additional_score = result['additional_score']
            if 'application_id' in result:
                result_record.application_id = result['application_id']
            if 'nomination_id' in result:
                result_record.nomination_id = result['nomination_id']
            if 'rank' in result:
                result_record.rank = result['rank']
            if 'total_result' in result:
                result_record.total_result = result['total_result']
            if 'comments' in result:
                if result['comments'] != '':
                    result_record.comments = result['comments']
                else:
                    result_record.comments = None

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update result due to an error: {}".format(str(e))}), 500
    return jsonify({"success": "Result updated successfully."}), 204