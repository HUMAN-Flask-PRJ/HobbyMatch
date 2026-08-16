from flask import Flask
from config import Config


def create_app():
    #현재 파일이 있는 폴더 기준으로 templates/ 와 static/ 을 자동으로 찾는다.
    app = Flask(__name__)

    #routes bp 만들기
    from backend.routes.main import bp as main_bp

    #만든 bp 등록
    app.register_blueprint(main_bp)
    
    from backend.models import hobby, mbti
    
    #Json 파일 처음에 로드해 메모리에 올려두기
    hobby.load_all()
    mbti.load_all()
    
    return app

app = create_app()

if __name__=='__main__':
    app.run(debug=app.config.get('DEBUG'))