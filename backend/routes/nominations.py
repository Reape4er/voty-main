from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# from utils import arithmetic_calculate, rating_calculate, put_new_scores
from models import (
    Nominations,
    db,
    Events,
    Users,
)
from sqlalchemy.exc import SQLAlchemyError

nominations_bp = Blueprint("nominations", __name__)
@nominations_bp.route("/events/<int:event_id>/nominations", methods=["GET"])
@jwt_required()
def get_nominations_by_event_id(event_id):
    event = Events.query.get(event_id)
    nominations = event.nominations
    nominations_data = []
    for n in nominations:
        nomination_data = n.to_dict()  # Получаем данные номинации
        # Предполагаем, что у модели Nominations есть связь 'user' с Users
        experts = n.users
        print(experts)
        if experts:
            experts_list = []
            for u in experts:
                experts_list.append(u.to_dict())
            nomination_data['users'] = experts_list  # Добавляем данные пользователя к номинации
            print(nomination_data)
        nominations_data.append(nomination_data)
    return jsonify(nominations_data)

@nominations_bp.route("/events/<int:event_id>/nominations/<int:nomination_id>", methods=["GET"])
@jwt_required()
def get_nomination_by_id(nomination_id):
    nomination = Nominations.query.get(nomination_id)
    return jsonify(nomination.to_dict())

@nominations_bp.route("/events/<int:event_id>/nominations", methods=["POST"])
@jwt_required()
def create_nomination(event_id):
    #nomination_data = request.get_json()
    new_nomination = Nominations(
        nomination_name = "Новая номинация",
        nomination_description = "Описание номинации",
        event_id = event_id,
        nomination_status = 0,
    )
    db.session.add(new_nomination)
    db.session.commit()
    return jsonify(new_nomination.to_dict()), 201

@nominations_bp.route("/events/<int:event_id>/nominations/<int:nomination_id>", methods=["PUT"])
@jwt_required()
def update_nomination(event_id, nomination_id):
    # поля которые можно менять
    try:
        ALLOWED_UPDATE_FIELDS = [
            'nomination_name',
            'nomination_description',
            'nomination_status',
            ]
        # обновляем поля для Nominations
        nomination_data = request.get_json()
        print(nomination_data)
        #print(nomination_data)
        nomination = Nominations.query.get(nomination_id)
        for field in ALLOWED_UPDATE_FIELDS:
            if field in nomination_data:
                setattr(nomination, field, nomination_data[field])
        # обновляем список пользовтелей
        if 'users'  in nomination_data:
            user_ids = [user['id'] for user in nomination_data['users'] if 'id' in user]

            updated_users = Users.query.filter(Users.id.in_(user_ids)).all()
            
            current_users = set(nomination.users)
            updated_users_set = set(updated_users)

            users_to_add = updated_users_set - current_users
            users_to_remove = current_users - updated_users_set

            for user in users_to_add:
                nomination.users.append(user)
            
            for user in users_to_remove:
                nomination.users.remove(user)
                
        db.session.commit()
        return jsonify({}), 204
    
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        
        return jsonify({"error": f"Ошибка при обновлении мероприятия: {str(e)}"}), 500

@nominations_bp.route("/events/<int:event_id>/nominations/<int:nomination_id>", methods=["DELETE"])
@jwt_required()
def delete_nomination(event_id, nomination_id):
    nomination = Nominations.query.get(nomination_id)
    if not nomination:
        return jsonify({"error": "Мероприятие не найдено"}), 404

    try:
        db.session.delete(nomination)
        db.session.commit()
        return jsonify({"message": "Мероприятие успешно удалено"}), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": f"Ошибка при удалении мероприятия: {str(e)}"}), 500

@nominations_bp.route("/check_status", methods=["GET"])
@jwt_required()
def check_status():
    event_id = request.args.get("eventId")
    user_id = int(request.args.get("id"))
    event = Events.query.get(event_id)
    if event is None:
        return jsonify({"error": "Events not found"}), 404
    eventStatus = event.status
    if eventStatus == 0:
        return jsonify({"error": "Мероприятие выключено"}), 403
    if user_id not in event.selected_experts:
        return jsonify({"error": "User is not in the selected experts list"}), 403
    return jsonify({"status": "success"}), 200
