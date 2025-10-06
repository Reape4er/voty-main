from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# from utils import put_new_scores
from models import (
    db,
    Events,
    Nominations,
    ArithmeticEvaluations,
    RatingEvaluations,
)

scores_bp = Blueprint("scores", __name__)

@scores_bp.route("/get_score", methods=["GET"])
@jwt_required()
def get_score():
    """
    Получение оценки нужного эксперта по нужной заявке определённой номинации.

    Request parameters:
        - event_id: id мероприятия.
        - nomination_id: id номинации.
        - expert_id: id эксперта.
        - application_id: id заявки.
        - criteria_id: id критерия (для арифметического метода).
    """

    nomination_id = request.args.get("nomination_id")
    expert_id = request.args.get("expert_id")
    application_id = request.args.get("application_id")
    # criteria_id = request.args.get("criteria_id")
    if (not nomination_id) or (not expert_id) or (not application_id):
        return jsonify({"error": "Не указаны необходимые данные."}), 400

    event_id = Nominations.query.get(nomination_id).event_id
    evaluation_method = Events.query.get(event_id).evaluation_method

    if event_id is None or evaluation_method is None:
        return jsonify({"error": "Ошибка поиска."}), 500

    if int(evaluation_method) == 0:
        # Арифметический метод:
        # if not criteria_id:
        #     return jsonify({"error": "Не указан id критерия."}), 400

        existing_score = ArithmeticEvaluations.query.filter(
            ArithmeticEvaluations.nomination_id == nomination_id,
            ArithmeticEvaluations.expert_id == expert_id,
            ArithmeticEvaluations.application_id == application_id,
            # ArithmeticEvaluations.criteria_id == criteria_id,
        ).all()#.first()

    elif int(evaluation_method) == 1:
        # Рейтинговый метод:
        existing_score = RatingEvaluations.query.filter(
            RatingEvaluations.nomination_id == nomination_id,
            RatingEvaluations.expert_id == expert_id,
            RatingEvaluations.application_id == application_id,
        ).all()

    if not existing_score:
        return jsonify({"error": "Оценка не найдена."}), 404

    if int(evaluation_method) == 0:
        return jsonify([evaluation.to_dict() for evaluation in existing_score]), 200
    elif int(evaluation_method) == 1:
        return jsonify({"position": existing_score.position}), 200


@scores_bp.route("/update_scores", methods=["PUT"])
@jwt_required()
def update_scores():
    """
    Функция для обновления оценок в базе данных (их проставления).

    Parameters:
        - nomination_id (int): id номинации.
        - expert_id (int): id эксперта, который проставляет оценки.
        - score_data (dict???): словарь заявок и оценок
        (содержит criteria_id при арифметическом методе).

    Returns:
        - bool: успех / ошибка.
    """
    try:
        data = request.get_json()
        event_id = data.get("eventId")
        nomination_id = data.get("nominationId")
        application_id = data.get("selectedParticipantId")
        expert_id = data.get("expertId")
        score_data = data.get("criteria")

        evaluation_method = Events.query.get(event_id).evaluation_method

        if int(evaluation_method) == 0:
            if not (event_id and nomination_id and application_id and expert_id and score_data):
                return jsonify({"error": "Не все необходимые данные предоставлены"}), 400
            # Арифметический метод:
            #удаление старых оценок по участнику
            existing_scores = ArithmeticEvaluations.query.filter_by(
                nomination_id=nomination_id,
                expert_id=expert_id,
                application_id=application_id
            ).all()
            for score in existing_scores:
                db.session.delete(score)
            #добавление новых оценок по участнику
            for criteria in score_data:
                application_score = ArithmeticEvaluations(
                    nomination_id=nomination_id,
                    expert_id=expert_id,
                    application_id=application_id,
                    criteria_id=criteria['id'],
                    value=criteria['value'],
                )

                db.session.add(application_score)

        if int(evaluation_method) == 1:
            print(score_data)
            if not (event_id and nomination_id and expert_id and score_data):
                return jsonify({"error": "Не все необходимые данные предоставлены"}), 400
            #удаление старых оценок по участнику
            existing_scores = RatingEvaluations.query.filter_by(
                nomination_id=nomination_id,
                expert_id=expert_id
            ).all()
            for score in existing_scores:
                db.session.delete(score)
            # Рейтинговый метод:
            for criteria in score_data:
                application_score = RatingEvaluations(
                    nomination_id=nomination_id,
                    expert_id=expert_id,
                    application_id=criteria['app_id'],
                    position=criteria['position'],
                )
                db.session.add(application_score)

        db.session.commit()

        return jsonify({}), 204
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": f"Ошибка при обновлении оценок: {str(e)}"}), 500



# @scores_bp.route("/update_score", methods=["POST"])
# @jwt_required()
# def update_score():
#     try:
#         data = request.get_json()
#         event_id = request.args.get("eventId")
#         eventType = Event.query.get(event_id).evaluation_method
#         # ОБРАБОТКА ИЗ РЕЙТИНГА
#         if eventType == "rating":
#             # Удаляем все существующие оценки для данного эксперта перед обработкой новых данных
#             expert_id = data[0]["expertId"]
#             scores_to_delete = ParticipantScore.query.filter_by(expertId=expert_id)
#             print(
#                 f"Found {scores_to_delete.count()} scores to delete for expert {expert_id}"
#             )

#             deleted_count = scores_to_delete.delete()
#             print(f"Deleted {deleted_count} scores")
#             for item in data:  # обрабатываем каждый элемент в массиве data
#                 # теперь нам не нужно искать существующие записи, просто создаем новые
#                 new_score = ParticipantScore(
#                     eventId=item["eventId"],
#                     expertId=item["expertId"],
#                     selectedParticipantId=item[
#                         "id"
#                     ],  # используем id вместо selectedParticipantId
#                     criteria=item["position"],  # используем position вместо criteria
#                     comments="",  # используем пустую строку для comments, так как в data нет подходящего поля
#                 )
#                 db.session.add(new_score)
#         # ОБРАБОТКА ИЗ АРИФМЕТИЧЕСКОЙ
#         else:
#             # пытаемся найти существующий объект ParticipantScore
#             existing_score = ParticipantScore.query.filter_by(
#                 eventId=data["eventId"],
#                 expertId=data["expertId"],
#                 selectedParticipantId=data["selectedParticipantId"],
#             ).first()

#             if existing_score is not None:
#                 # если объект найден, обновляем его поля
#                 existing_score.criteria = data["criteria"]
#                 existing_score.comments = data["comments"]
#             else:
#                 # если объект не найден, создаем новый
#                 new_score = ParticipantScore(
#                     eventId=data["eventId"],
#                     expertId=data["expertId"],
#                     selectedParticipantId=data["selectedParticipantId"],
#                     criteria=data["criteria"],
#                     comments=data["comments"],
#                 )
#                 db.session.add(new_score)

#         # коммитим изменения в базу данных
#         db.session.commit()

#         return jsonify({"message": "Оценки успешно обновлены"}), 200

#     except Exception as e:
#         # откатываем изменения в случае ошибки
#         db.session.rollback()
#         print(str(e))
#         return (
#             jsonify({"message": "Произошла ошибка при добавлении в базу данных"}),
#             500,
#         )


# @scores_bp.route("/get_average_scores", methods=["GET"])
# def get_average_scores():
#     event_id = request.args.get("eventId")
#     participant_averages = ParticipantAverage.query.filter_by(eventId=event_id).all()

#     results = []

#     for participant_average in participant_averages:
#         participant = Participants.query.get(participant_average.participantId)
#         results.append(
#             {
#                 "id": participant.id,
#                 "last_name": participant.last_name,
#                 "first_name": participant.first_name,
#                 "middle_name": participant.middle_name,
#                 "report_title": participant.report_title,
#                 "average_score": participant_average.averageScore,
#             }
#         )

#     return jsonify(results)
