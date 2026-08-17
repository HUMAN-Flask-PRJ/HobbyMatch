from flask import Blueprint, render_template
from backend.models import mbti, hobby

# diagnosis라는 이름의 라우트 묶음
bp = Blueprint("diagnosis", __name__)


# URL 연결
@bp.route("/diagnosis")
def diagnosis():
    # JSON 파일을 직접 열지 않고 model을 통해 호출
    # controller가 repository를 직접 호출하지 않고 service를 통해 호출하는 것과 비슷
    # 현재는 app.py에서 실행한 것이 있기 때문에 메모리에 있는 데이터 반환
    mbti_list=mbti.load_all()
    hobbies = hobby.load_all()

    return render_template(
        "diagnosis.html",
        # base.html에서 현재 메뉴에 {% if active_tab == 'diagnosis' %} 필요
        active_tab="diagnosis",
        mbti_list = mbti_list,   # html로 데이터를 넘김 model.addAttribute()와 비슷
                                # "HTML에서 사용할 변수 이름 = Python에 실제 들어있는 데이터"
                                # html에서 {{ mbti_list }}로 접근 가능
        hobbies = hobbies
        )