from flask import Blueprint, request
from flask import send_file
from datetime import datetime
from docxtpl import DocxTemplate

from models import Applications, db, Events, Users, Nominations

protocol_bp = Blueprint("protocol", __name__)


@protocol_bp.route("/get_protocol", methods=["GET"])
def get_protocol():
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")  # формат: день.месяц.год

    nomination_id = request.args.get("nomination_id")
    doc = DocxTemplate("./static/template.docx")

    nomination = Nominations.query.get(nomination_id)
    nomiantion_name = nomination.nomination_name

    event_name = nomination.events.event_name
    
    experts = [u.to_dict() for u in nomination.users]
    # print(experts)
    applications = nomination.applications
    applications_count = len(applications)

    evaluation_method = nomination.events.evaluation_method
    print(nomination.events.ratings_parameters)
    if evaluation_method == 1:
        rating_position = nomination.events.ratings_parameters[0].position_count 
    else:
        rating_position = None
    nomination_result = [r.to_dict() for r in nomination.nomination_results]
    sorted_nomination_result = sorted(nomination_result, key=lambda x: x['rank'])
    nomination_results = []
    for result in sorted_nomination_result:
        application_id = result['application_id']
        application = Applications.query.get(application_id)
        full_application = application.full_application_dict()
        
        # Merge dictionaries with result keys first
        merged_dict = {**result, **full_application}
        
        nomination_results.append(merged_dict)
    
    context = {
        "date": date_str,
        "expert_list": experts,
        "applications_count": applications_count,
        "evaluation_method": evaluation_method, 
        "nomination_results": nomination_results,
        "event_name": event_name,
        "nomination_name": nomiantion_name,
        "rating_position": rating_position,
        "rating1": nomination_results[0],
        "rating2": nomination_results[1],
        "rating3": nomination_results[2],
        # "comments": comments,
    }

    doc.render(context)
    doc.save("generated_doc.docx")
    try:
        return send_file("generated_doc.docx", as_attachment=True)
    except Exception as e:
        return str(e)
