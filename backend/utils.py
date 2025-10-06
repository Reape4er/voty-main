from models import (
    db,
    Events,
    Nominations,
    NominationResults,
    ArithmeticEvaluations,
    RatingEvaluations,
)


def arithmetic_calculate(nomination_id: int) -> bool:
    """
    Функция для арифметического подсчёта результатов оценивания ArithmeticEvaluations.
    Сохраняет данные в NominationResults.

    Parameters:
        - nomination_id (int): id номинации.

    Returns:
        - bool: успех / ошибка.
    """

    try:
        NominationResults.query.filter_by(nomination_id=nomination_id).delete()
        evaluations = ArithmeticEvaluations.query.filter_by(
            nomination_id=nomination_id
        ).all()

        results = {}

        for evaluation in evaluations:
            application_id = evaluation.application_id
            score = evaluation.value

            if application_id in results:
                results[application_id]["total_score"] += score
                results[application_id]["count"] += 1
            else:
                results[application_id] = {"total_score": score, "count": 1}

        for application_id, data in results.items():
            total_score = data["total_score"]
            count = data["count"]

            average_score = total_score / count

            application_result = NominationResults(
                nomination_id=nomination_id,
                application_id=application_id,
                result=average_score,
            )
            db.session.add(application_result)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка арифметического подсчёта (arithmetic): {e}")
        return False


def rating_calculate(nomination_id: int) -> bool:
    """
    Функция для рейтингового подсчёта результатов оценивания RatingEvaluations.
    Сохраняет данные в NominationResults.

    Parameters:
        - nomination_id (int): id номинации.

    Returns:
        - bool: успех / ошибка.
    """

    try:
        NominationResults.query.filter_by(nomination_id=nomination_id).delete()
        evaluations = RatingEvaluations.query.filter_by(
            nomination_id=nomination_id
        ).all()
        max_positions = Nominations.query.filter_by(id=nomination_id).first().events.ratings_parameters[0].position_count
        reverse_scores = {position: max_positions - position + 1 for position in range(1, max_positions + 1)}
        results = {}

        for evaluation in evaluations:
            application_id = evaluation.application_id
            position = evaluation.position

            if application_id in results:
                results[application_id]["total_position"] += reverse_scores[position]
                results[application_id]["count"] += 1
            else:
                results[application_id] = {"total_position": reverse_scores[position], "count": 1}

        for application_id, data in results.items():
            total_position = data["total_position"]
            count = data["count"]
            average_position = total_position #/ count

            application_result = NominationResults(
                nomination_id=nomination_id,
                application_id=application_id,
                result=average_position,
            )
            db.session.add(application_result)

        db.session.commit()
        return True

    except Exception as e:
        print(e)
        db.session.rollback()
        return False


# def map_input_to_model(input_array):
#     mapped_array = []
#     for input_data in input_array:
#         mapped_data = {
#             "id": input_data.get("ID"),
#             "section": input_data.get("Выбор секции"),
#             "creation_time": input_data.get("Время создания"),
#             "email": input_data.get("Электронная почта"),
#             "last_name": input_data.get("Фамилия полностью"),
#             "first_name": input_data.get("Имя полностью"),
#             "middle_name": input_data.get("Отчество полностью"),
#             "phone": input_data.get("Телефон"),
#             "participation_format": input_data.get("Формат участия"),
#             "training_level": input_data.get("Уровень подготовки"),
#             "education_institution": input_data.get(
#                 "Полное наименование учебного заведения"
#             ),
#             "section_choice": input_data.get("Выбор секции"),
#             "report_title": input_data.get("Название доклада"),
#             "group_info_1": input_data.get("ФИО полностью, номер группы [1]"),
#             "group_info_2": input_data.get("ФИО полностью, номер группы [2]"),
#             "group_info_3": input_data.get("ФИО полностью, номер группы [3]"),
#             "group_info_4": input_data.get("ФИО полностью, номер группы [4]"),
#             "group_info_5": input_data.get("ФИО полностью, номер группы [5]"),
#             "group_info_6": input_data.get("ФИО полностью, номер группы [6]"),
#             "group_info_7": input_data.get("ФИО полностью, номер группы [7]"),
#             "supervisor_name": input_data.get("ФИО научного руководителя полностью"),
#             "department": input_data.get("Ведущая кафедра"),
#             "research_relevance": input_data.get("Актуальность исследования"),
#             "research_goal": input_data.get("Цель исследования"),
#             "research_tasks": input_data.get("Задачи исследования"),
#             "research_methodology": input_data.get("Методика исследования"),
#             "research_results": input_data.get("Результаты исследования"),
#             "conclusions": input_data.get("Выводы"),
#             "data_processing_consent": input_data.get(
#                 "Согласие на обработку персональных данных"
#             ),
#         }
#         mapped_array.append(mapped_data)

#     return mapped_array


# def participantsUpdate(participantData):
#     participantList = map_input_to_model(participantData)
#     for data in participantList:
#         participant = Participants.query.filter_by(email=data["email"]).first()
#         if participant is None:
#             participant = Participants(
#                 section=data["section"],
#                 creation_time=data["creation_time"],
#                 email=data["email"],
#                 last_name=data["last_name"],
#                 first_name=data["first_name"],
#                 middle_name=data["middle_name"],
#                 phone=data["phone"],
#                 participation_format=data["participation_format"],
#                 training_level=data["training_level"],
#                 education_institution=data["education_institution"],
#                 section_choice=data["section_choice"],
#                 report_title=data["report_title"],
#                 group_info_1=data["group_info_1"],
#                 supervisor_name=data["supervisor_name"],
#                 department=data["department"],
#                 research_relevance=data["research_relevance"],
#                 research_goal=data["research_goal"],
#                 research_tasks=data["research_tasks"],
#                 research_methodology=data["research_methodology"],
#                 research_results=data["research_results"],
#                 conclusions=data["conclusions"],
#                 data_processing_consent=data["data_processing_consent"],
#             )
#             db.session.add(participant)


# def put_new_scores(nomination_id, expert_id, score_data):
#     """
#     Функция для обновления оценок в базе данных (их проставления).

#     Parameters:
#         - nomination_id (int): id номинации.
#         - expert_id (int): id эксперта, который проставляет оценки.
#         - score_data (dict???): словарь заявок и оценок
#         (содержит criteria_id при арифметическом методе).

#     Returns:
#         - bool: успех / ошибка.
#     """

#     event_id = Nominations.query.get(nomination_id).event_id
#     evaluation_method = Events.query.get(event_id).evaluation_method

#     if (event_id is None) or (evaluation_method is None):
#         return False

#     try:
#         if int(evaluation_method) == 0:
#             # Арифметический метод:
#             for score_info in score_data:
#                 application_id = score_info["application_id"]
#                 criteria_id = score_info["criteria_id"]
#                 score_value = score_info["score"]

#                 application_score = ArithmeticEvaluations(
#                     nomination_id=nomination_id,
#                     expert_id=expert_id,
#                     application_id=application_id,
#                     criteria_id=criteria_id,
#                     score=score_value,
#                 )

#                 db.session.add(application_score)

#         if int(evaluation_method) == 1:
#             # Рейтинговый метод:
#             for score_info in score_data:
#                 application_id = score_info["application_id"]
#                 score_value = score_info["score"]

#                 application_score = RatingEvaluations(
#                     nomination_id=nomination_id,
#                     expert_id=expert_id,
#                     application_id=application_id,
#                     position=score_value,
#                 )
#                 db.session.add(application_score)

#         db.session.commit()

#         return True
#     except Exception as e:
#         db.session.rollback()
#         return False


# def check_evaluations(event_id):
#     # Проверяем наличие данных оценок для данного мероприятия
#     evaluations_exist = db.session.query(
#         ParticipantScore.query.filter_by(eventId=event_id).exists()
#     ).scalar()
#     return evaluations_exist
