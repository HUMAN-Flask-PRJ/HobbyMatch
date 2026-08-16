import os
from pathlib import Path
from dotenv import load_dotenv

#.env 파일에 있는 값을 읽어온다.
load_dotenv()

class Config:
    #환경변수 FLASK_ENV 값이 development 라면 DEBUG 모드 실행
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    

# 현재 파일 경로 저장
BASE_DIR = Path(__file__).resolve().parent

# 취미, MBTI JSON 파일이 있는 경로
HOBBIES_PATH = BASE_DIR / "backend" / "data" / "hobbies.json"
MBTI_PATH = BASE_DIR / "backend" / "data" / "mbti.json"
