# HobbyMatch · 하비매치

MBTI·기존 취미·시간·예산을 종합해 나에게 맞는 취미를 추천하는 웹 서비스

**Python · Flask · Jinja2 · Vanilla JavaScript · JSON**

**프로젝트 기간** 2026.08.12 ~ 2026.08.19  


[HobbyMatch 바로가기](https://port-0-flaskexample-msx8671h6a4e62ab.sel3.cloudtype.app/)

---

## 프로젝트 소개

HobbyMatch는 사용자의 MBTI, 기존 취미, 활동 성향, 목적, 시간·예산을 바탕으로 새로운 취미를 추천하는 웹 서비스입니다.

간단한 4단계 진단을 통해 사용자 성향을 구조화하고, 취미 데이터와 비교하여 적합도 기반 추천 결과를 제공합니다.

추천 결과뿐 아니라 전체 취미 목록과 Starter Guide를 함께 제공하여 새로운 취미 탐색을 지원합니다.

---

## 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| Backend | Flask |
| Template Engine | Jinja2 |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Data | JSON (`hobbies.json`, `mbti.json`) |
| Deployment | Gunicorn, Cloudtype |
| Collaboration | Git, GitHub |

### 주요 구현 기술

- Flask Blueprint 기반 기능별 라우팅 분리
- Route / Service / Model 구조 분리
- Flask Session 기반 사용자 진단 입력값 관리
- Jinja2 기반 서버 사이드 렌더링
- JSON 데이터 로드 및 캐싱

---

## 주요 기능

- **4단계 취미 진단**
  - MBTI
  - 기존 취미
  - 활동 성향 및 목적
  - 시간 및 예산

- **가중치 기반 맞춤 추천**
  - 사용자 입력값과 취미 데이터 비교를 통한 적합도 계산
  - Safe Pick / Adjacent Pick / Wild Card 3종 추천

- **추천 결과 제공**
  - 추천 취미
  - 추천 점수
  - 추천 이유
  - 난이도·비용·활동량 등 기본 정보 제공

- **취미 탐색**
  - 전체 취미 목록 확인
  - 취미별 설명 확인
  - Starter Guide 팝업 제공

- **진단 상태 유지**
  - 진단 입력값의 Flask Session 저장
  - 다시 진단하기 전까지 기존 입력값 유지

---

## 서비스 흐름

```text
사용자 진단
    ↓
Flask Route
    ↓
Session 입력값 저장
    ↓
Recommendation Service
    ↓
hobbies.json / mbti.json 비교
    ↓
추천 점수 계산 및 순위 선정
    ↓
Jinja2 Template
    ↓
추천 결과 출력
```

---

## 프로젝트 구조

```text
HobbyMatch/
├── app.py
├── config.py
├── requirements.txt
│
├── backend/
│   ├── data/
│   │   ├── hobbies.json
│   │   └── mbti.json
│   │
│   ├── models/
│   │   ├── hobby.py
│   │   └── mbti.py
│   │
│   ├── routes/
│   │   ├── main.py
│   │   ├── diagnosis.py
│   │   ├── recommendation.py
│   │   └── explore.py
│   │
│   └── services/
│       └── recommendation_service.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── diagnosis.html
│   ├── recommendation.html
│   └── explore.html
│
└── static/
    ├── css/
    └── js/
```

### 레이어 역할

- **routes** — URL 매핑, 요청·폼 처리, Session 처리, 템플릿 렌더링
- **services** — 추천 점수 계산 및 추천 결과 생성
- **models** — JSON 데이터 로드 및 캐시
- **templates** — Jinja2 기반 화면 구성
- **static** — CSS 및 JavaScript 관리

---

## 주요 화면

### 메인 화면
<img src="https://github.com/user-attachments/assets/59fd14a7-cab4-427e-91ea-111decb1dfdb" width="900" alt="HobbyMatch 메인 화면">

### 취미 진단 화면
<img src="https://github.com/user-attachments/assets/03b8e160-43b1-461c-aad8-ad06feaac1ad" width="900" alt="HobbyMatch 취미 진단 화면">

### 추천 결과 화면
<img src="https://github.com/user-attachments/assets/bf9a8f6b-c636-454b-8bd9-84df7a10e14a" width="900" alt="HobbyMatch 추천 결과 화면">

### 취미 탐색 및 Starter Guide 화면
<img src="https://github.com/user-attachments/assets/e0c147f1-8f8e-4686-9023-34ec02ad80ed" width="900" alt="HobbyMatch 취미 탐색 화면">

<img src="https://github.com/user-attachments/assets/7c4488ce-87d5-440b-acd0-a002a0377958" width="900" alt="HobbyMatch Starter Guide 화면">

---

## 팀원 및 역할

| 팀원 | 담당 영역 |
|---|---|
| 배민선 | 취미 진단 · 사용자 프로필 |
| 최주원 | 추천 알고리즘 |
| 박재은 | 추천 결과 · 상세 정보 |
| 이제형 | 취미 탐색 · Starter Guide |
| 정현식 | Flask 공통 구조 · 데이터 · 전체 통합 |

---

## 로컬 실행 방법

### 1. 저장소 복제

```bash
git clone https://github.com/HUMAN-Flask-PRJ/HobbyMatch.git
cd HobbyMatch
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
python app.py
```

### 5. 브라우저 접속

```text
http://127.0.0.1:5000
```

---

## 향후 개선 방향

- **LLM 기반 추천 고도화**
  - 자연어 입력 분석을 통한 추천 범위 및 다양성 확장

- **MariaDB 연동 및 사용자별 추천 이력 관리**
  - JSON 기반 취미 데이터의 MariaDB 전환 및 사용자별 진단·추천 이력 관리

- **취미 검색·필터 기능 확장**
  - 취미명, 카테고리, 예산, 활동량, 소요 시간 기반 검색·필터 기능 추가
