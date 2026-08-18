from flask import Flask
from config import Config

def create_app():
    #현재 파일이 있는 폴더 기준으로 templates/ 와 static/ 을 자동으로 찾는다.
    app = Flask(__name__)

    #routes bp 만들기
    from backend.routes.main import bp as main_bp
    from backend.routes.recommendation import bp as recommend_bp
    from backend.routes.diagnosis import bp as diagnosis_bp
    from backend.routes.explore import explore_bp 

    #만든 bp 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(explore_bp)
    
    from backend.models import hobby, mbti
    
    #Json 파일 처음에 로드해 메모리에 올려두기
    hobby.load_all()
    mbti.load_all()
    # 세션 암호화에 필요한 키 설정
    app.secret_key = "hobbymatch_secret_key"
    
    return app

app = create_app()

if __name__=='__main__':
    app.run(debug=app.config.get('DEBUG'))

