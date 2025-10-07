from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import Applications, ApplicationsFields, EventQuestions, Nominations, db

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/applications/upload", methods=["POST"])
@jwt_required()
def upload_applications():
    """
    Загружает заявки для определенного мероприятия.

    Параметры:
    - event_id (int): Идентификатор мероприятия, для которого загружаются заявки.
    - applications (list): Список словарей, представляющих заявки для загрузки. Каждый словарь должен содержать следующие ключи:
        - ID (int): Идентификатор заявки.
        - Другие ключи: Ключи представляют вопросы для заявки, а значения - ответы на эти вопросы.

    Возвращает:
    - response (str): JSON-ответ, указывающий на успешность загрузки.

    Пример использования:
    data = { "event_id": 123, "applications": [ { "ID": 1, "Вопрос 1": "Ответ 1", "Вопрос 2": "Ответ 2" }, { "ID": 2, "Вопрос 1": "Ответ 3", "Вопрос 2": "Ответ 4" } ] }

    response = upload_applications(data)

    """
    data = request.get_json()
    event_id = data.get('event_id')
    applications = data.get('applications')
    nomination_column = data.get('nomination_column')
    to_show_column = data.get('to_show_column')
    try:
        if event_id and applications:
            existing_nominations = Nominations.query.filter_by(event_id=event_id).all()
            for nomination in existing_nominations:
                db.session.delete(nomination)

            existing_questions = EventQuestions.query.filter_by(event_id=event_id).all()
            for question in existing_questions:
                db.session.delete(question)

            db.session.commit()
            
        #Создаем вопросы к мероприятию
        questions_id_map = {}
        for key in applications[0].keys():
            if key != "ID":
                event_question = EventQuestions(event_id=event_id, question_field=key, required=True, question_number=1)
                if key in to_show_column:
                    event_question.display = True
                    print(key)
                db.session.add(event_question)
                db.session.flush()
                questions_id_map[key] = event_question.id
        
        Nominations_id_map = {}
        for application in applications:
            #Создаем номинации к мероприятию   
            nomination = application[nomination_column]
            if nomination not in Nominations_id_map:
                new_nomination = Nominations(nomination_name=nomination, event_id=event_id, nomination_status = 0)
                db.session.add(new_nomination)
                db.session.flush()  # Это гарантирует, что объекту будет присвоен ID до коммита
                Nominations_id_map[nomination] = new_nomination.id
            #Создаем заявки к мероприятию   
            new_application = Applications(application_status = False, nomination_id=Nominations_id_map[nomination])
            db.session.add(new_application)
            db.session.flush()
            #Создаем заполненные поля заявки
            for question, question_answer in application.items():
                if question != "ID":
                    new_field = ApplicationsFields(application_id = new_application.id, question_id = questions_id_map[question], question_answer = question_answer)
                    db.session.add(new_field)
                    db.session.flush()
        db.session.commit()
        return jsonify("Загрузка участников успешна"), 267
    except Exception as e:
        db.session.rollback()
        return jsonify(f"Ошибка при загрузке: {str(e)}"), 500

@applications_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_all_applications_by_nomination_id():
    nomination_id = request.args.get("nomination_id")
    accepted = request.args.get("accepted", type=bool)  # Ensure 'accepted' is interpreted as a boolean
    nomination = Nominations.query.get(nomination_id)
    if not nomination:
        return jsonify({"error": "Nomination not found"}), 404
    
    if accepted:
        applications_list = [app.full_application_dict() for app in nomination.applications if app.application_status]
    else:
        applications_list = [app.full_application_dict() for app in nomination.applications]
    
    return jsonify(applications_list), 200

@applications_bp.route("/applications", methods=["PUT"])
@jwt_required()
def update_application():
    data = request.get_json()
    application_id = request.args.get("application_id")
    try:
        application = Applications.query.get(application_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404
        application.application_status = data.get("application_status")
        db.session.commit()
        return jsonify({}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify(f"Ошибка при обновление: {str(e)}"), 500