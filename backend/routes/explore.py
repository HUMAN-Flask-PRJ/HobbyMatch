import json # 파이썬의 기본 라이브러리인 json 객체를 불러온다
import os
from flask import Blueprint, render_template, current_app

explore_bp = Blueprint("explore", __name__)

@explore_bp.route('/explore') # 데코레이터
def explore(): # 일반 함수
    # hobbies.json 파일 경로 설정
    json_path = os.path.join(current_app.root_path, 'backend', 'data', 'hobbies.json')
    
    # JSON 파일 읽기
    with open(json_path, 'r', encoding="utf-8") as f:
        hobbies_data = json.load(f)
        
    # explore.html에 데이터 전달
    return render_template('explore.html', hobbies=hobbies_data, active_tab="explore")