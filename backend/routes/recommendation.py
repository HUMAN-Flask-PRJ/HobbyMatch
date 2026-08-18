from flask import Blueprint, render_template, request
from backend.models import hobby, mbti
from backend.services.recommendation_service import make_recommendations

bp = Blueprint("recommendation", __name__)


@bp.route("/recommendation", methods=["POST"])
def recommendation():

    # diagnosis.html에서 값 받기
    mbti_type = request.form.get("mbti")
    selected_hobbies = request.form.getlist("hobby")
    purposes = request.form.getlist("purpose")

    social_type = request.form.get("socialType")
    indoor_outdoor = request.form.get("indoorOutdoor")
    activity_level = request.form.get("activityLevel")

    budget_tier = request.form.get("budgetTier")
    time_required = request.form.get("timeRequired")


    # 전체 취미 데이터
    hobbies = hobby.load_all()


    #사용자 입력을 추천 서비스 형식으로 정리
    user_input = {
        "history": selected_hobbies,

        "preference": {
            "socialType": social_type,
            "indoorOutdoor": indoor_outdoor,
            "activityLevel": activity_level
        },

        "condition": {
            "budgetTier": budget_tier,
            "timeRequired": time_required
        },

        "purpose": purposes
    }


    # MBTI 정보 찾기
    mbti_list = mbti.load_all()

    mbti_info = None

    #사용자가 선택한 mbti와 일치하는 상세 정보 찾기
    for item in mbti_list:
        if item["type"] == mbti_type:
            mbti_info = item
            break


    # 실제 추천 알고리즘 실행
    picks = make_recommendations(hobbies,mbti_info,  user_input)

    return render_template( "recommendation.html", active_tab="recommendation",picks=picks)