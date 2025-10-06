from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import jwt_required

from models import ArithmeticalMethodParams, RatingMethodParams, db, Events


events_bp = Blueprint("events", __name__)


@events_bp.route("/events", methods=["GET"])  # /get_event
@jwt_required()
def get_events():
    events = Events.query.all()

    if not events:
        abort(404)

    return jsonify([e.to_dict() for e in events])


@events_bp.route("/events/<int:event_id>", methods=["GET"])  # /get_event
@jwt_required()
def get_event_by_id(event_id):
    event = Events.query.get(event_id)
    response = event.to_dict()
    if not event:
        return jsonify({"message": "Мероприятие не найдено"}), 404
    # получаем список арифметических параметров
    arithmetics_parameters = event.arithmetics_parameters
    if arithmetics_parameters:
        arithmetics_parameters_list = []
        for parameter in arithmetics_parameters:
            arithmetics_parameters_list.append(parameter.to_dict())
        response['arithmetics_parameters'] = arithmetics_parameters_list
    # получаем список рейтинговых параметров
    ratings_parameters = event.ratings_parameters
    print(ratings_parameters)
    if ratings_parameters:
        response['ratings_parameters'] = ratings_parameters[0].to_dict()['position_count']
        print(response['ratings_parameters'])
    return jsonify(response)


@events_bp.route("/events", methods=["POST"])  # create_event
@jwt_required()
def create_event():
    # event_data = request.get_json()

    new_event = Events(
        event_name = "Новое мероприятие",
        event_description = "Описание мероприятия",
        event_level = 0,
        # Метод оценивания: 0 - Арифметический, 1 - Рейтинговый.
        evaluation_method = 0,
    )
    # Добавляем мероприятие в базу данных
    db.session.add(new_event)
    db.session.commit()

    return (
        jsonify(new_event.to_dict()),
        201,
    )


@events_bp.route("/events/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event_by_id(event_id):
    event = Events.query.get(event_id)
    
    if not event:
        return jsonify({"message": "Мероприятие не найдено"}), 404

    event_data = request.get_json()
    evaluation_method = event_data.get("evaluation_method")
    print(event_data)
    # Обновляем свойства мероприятия
    event.event_name = event_data.get("event_name")
    event.event_description = event_data.get("event_description")
    event.event_level = event_data.get("event_level")
    # Метод оценивания: 0 - Арифметический, 1 - Рейтинговый.
    event.evaluation_method = evaluation_method
    # Добавляем критерии
    if evaluation_method == 0:
        # Удаляем существующие параметры
        for param in event.arithmetics_parameters:
            db.session.delete(param)

        new_params_data = event_data.get("arithmetics_parameters")
        # Предполагается, что new_params_data - это список словарей с данными параметров
        for param_data in new_params_data:
            new_a_param = ArithmeticalMethodParams(
                event_id = event_id,
                criteria = param_data['criteria'],
                criteria_weight = param_data['criteria_weight'],
            )
            event.arithmetics_parameters.append(new_a_param)
    elif evaluation_method == 1:
        for param in event.ratings_parameters:
            db.session.delete(param)
        position_count = event_data.get("ratings_parameters")
        print(position_count)
        new_r_param = RatingMethodParams(
            event_id = event_id,
            position_count = position_count
        )
        event.ratings_parameters.append(new_r_param)
    db.session.commit()
    return jsonify({"message": "Мероприятие успешно обновлено"})


@events_bp.route("/events/<int:event_id>",methods=["DELETE"])  # /delete_event"
@jwt_required()
def delete_event_by_id(event_id):
    event = Events.query.get(event_id)
    if not event:
        return jsonify({"error": "Мероприятие не найдено"}), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Мероприятие успешно удалено"}), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": f"Ошибка при удалении мероприятия: {str(e)}"}), 500
