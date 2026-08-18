from flask import Blueprint, render_template, request
from backend.models import hobby, mbti
from backend.services.recommendation_service import make_recommendations

bp = Blueprint("recommended", __name__)

@bp.route("/recommendation", methods=["GET", "POST"])
def result():
    
    if request.method == "GET":
        return render_template("recommendation.html")
    
    mbti_type = request.form.get("mbti")
    current_hobbies = request.form.getlist("hobby")
    purpose = request.form.getlist("purpose")
    
    prefs = {
        "socialType" : request.form.get("socialType"),
        "indoorOutdoor" : request.form.get("indoorOutdoor"),
        # 파이썬에서는 마지막에서도 쉼표를 붙일 수 있음
        # 나중에 추가할 때를 생각해서 마지막에도 쉼표를 붙이는 방식을 주로 사용함
        "activityLevel" : request.form.get("activityLevel"),
    }
    
    conds = {
        "budgetTier" : request.form.get("budgetTier"),
        "timeRequired" : request.form.get("timeRequered"),
    }
    
    user_input = {
        "history" : current_hobbies,
        "preference" : prefs,
        "condition" : conds,
        "purpose" : purpose,
    }
    
    hobbies = hobby.load_all()
    mbti_list = mbti.load_all()
    
    mbti_info = next(
        (item for item in mbti_list if item["type"] == mbti_type),
        None
    )
    
    picks = make_recommendations(
        hobbies,
        mbti_info,
        user_input
    )
    
    return render_template(
        "recommendation.html",
        active_tab = "recommendation",
        mbti=mbti_type,
        picks=picks
    )
