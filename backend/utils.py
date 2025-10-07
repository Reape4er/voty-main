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