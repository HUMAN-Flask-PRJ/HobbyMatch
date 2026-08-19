# HobbyMatch · 하비매치

내가 좋아하는 것에서 출발해, 아직 몰랐던 새로운 취미를 발견하는 웹 서비스입니다.

MBTI, 기존 취미, 목적·성향, 시간·예산을 입력하면 6개 항목을 가중 합산해 취미 3종을 추천합니다.

- **Safe Pick (확장형)** — 지금 취미와 잘 이어지는 추천
- **Adjacent Pick (보완형)** — 무난한 차선
- **Wild Card (도전형)** — 익숙하지 않은 새로운 도전

## 주요 기능

- 4단계 취미 진단 (MBTI → 기존 취미 → 성향·목적 → 시간·예산)
- 가중치 기반 맞춤 추천과 시작 가이드 팝업
- 취미 탐색 목록에서 전체 취미와 입문 가이드 확인
- 진단 결과는 세션에 저장되어, 다시 진단하기 전까지 유지

## 기술 스택

- Python, Flask, Jinja2
- Vanilla JavaScript, CSS
- JSON 데이터 (`hobbies.json`, `mbti.json`) — DB 없음

## 실행 방법

Python 3가 필요합니다.

```bash
# 저장소 클론 후 프로젝트 폴더로 이동
cd HobbyMatch

# 가상환경 (선택)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python app.py
```

브라우저에서 [http://127.0.0.1:5000](http://127.0.0.1:5000) 으로 접속합니다.

디버그 모드로 실행하려면 `.env`에 아래를 넣거나, 실행 전에 환경 변수를 설정합니다.

```
FLASK_ENV=development
```

## 페이지

| 경로 | 설명 |
|------|------|
| `/` | 홈 |
| `/diagnosis` | 취미 진단 |
| `/diagnosis/reset` | 진단 세션 초기화 |
| `/recommendation` | 추천 결과 |
| `/explore` | 취미 탐색 |

## 추천 알고리즘

`backend/services/recommendation_service.py`에서 취미마다 0~100점을 매긴 뒤 가중 합산합니다.

| 항목 | 비중 | 내용 |
|------|------|------|
| S1 MBTI | 25% | 성격 대분류 카테고리 + 추천 키워드 |
| S2 연관성 | 25% | 기존 취미와의 관련·같은 카테고리 |
| S3 선호 | 20% | 혼자/함께, 실내/야외, 활동량 |
| S4 조건 | 15% | 예산·시간 |
| S5 목적 | 10% | 스트레스 해소, 창작 등 |
| S6 새로움 | 5% | 익숙한 취미만 나오지 않도록 보정 |

기존 취미가 없고 난이도가 `EASY`이면 입문자 보정(+5점)을 더합니다. 총점 상위 목록에서 Safe / Adjacent / Wild Card 3장을 고릅니다.

## 프로젝트 구조

```
HobbyMatch/
├── app.py                              # Flask 앱 생성, Blueprint 등록, JSON 선로드
├── config.py                           # 환경설정, 데이터 파일 경로
├── requirements.txt
├── backend/
│   ├── data/hobbies.json, mbti.json
│   ├── models/hobby.py, mbti.py        # JSON 로드 + 캐시
│   ├── routes/                         # URL, 폼 처리, 템플릿 렌더
│   │   ├── main.py                     # 홈
│   │   ├── diagnosis.py                # 취미 진단
│   │   ├── recommendation.py           # 추천 결과
│   │   └── explore.py                  # 취미 탐색
│   └── services/recommendation_service.py   # 추천 알고리즘
├── templates/                          # Jinja2 (base 상속)
│   ├── base.html
│   ├── home.html
│   ├── diagnosis.html
│   ├── recommendation.html
│   └── explore.html
└── static/
    ├── css/style.css, diagnosis.css
    └── js/diagnosis.js                 # 진단 단계 UI
```

레이어 역할은 다음과 같습니다.

- **routes** — URL, 폼, 템플릿 렌더
- **services** — 추천 점수 계산 (Flask request / 파일 I/O 없음)
- **models** — JSON 로드와 캐시 (추천 공식은 넣지 않음)
