# ==========================================

# 1. 상수 및 가중치 정의

# ==========================================

_WEIGHTS = {

    "MBTI": 0.25,      # S1: MBTI 적합도

    "RELATION": 0.25,  # S2: 취미 연관성

    "PREF": 0.20,      # S3: 개인 선호 매칭

    "COND": 0.15,      # S4: 조건 제약 매칭

    "PURPOSE": 0.10,   # S5: 목표 매칭

    "NOVELTY": 0.05,   # S6: 새로움 점수

}



# hobbies.json, user_input 순위 비교용 랭크 테이블

_BUDGET_RANK = {"FREE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}

_TIME_RANK = {"30MIN": 0, "1HOUR": 1, "HALF_DAY": 2, "FULL_DAY": 3}



# mbti.json 대분류 기준 선호 카테고리 매핑

_MBTI_CATEGORY_MAP = {

    "분석형 (Analysts)": ["🧠 지적 & 탐구", "🎮 디지탈 & 테크"],

    "외교형 (Diplomats)": ["🎨 창작 & 예술", "🧘 웰빙 & 힐링"],

    "관리형 (Sentinels)": ["🍳 요리 & 베이킹", "🧩 수집 & 제작", "🌿 자연 & 아웃도어"],

    "탐험가형 (Explorers)": ["🏃 액티비티 & 스포츠", "🌿 자연 & 아웃도어", "🎵 음악 & 공연"]

}





# ==========================================

# 2. 6대 평가 항목별 점수 계산 함수 (0 ~ 100점)

# ==========================================



def _calc_mbti_score(hobby, mbti_info):

    """S1: MBTI 적합도 (카테고리 40점 + 키워드 일치율 비례 60점)"""

    if not mbti_info:

        return 50



    # 1) 카테고리 궁합 (40점) - mbti.json의 category, hobbies.json의 category 참고

    mbti_category = mbti_info.get("category", "")

    preferred_categories = _MBTI_CATEGORY_MAP.get(mbti_category, [])

    category_score = 40 if hobby.get("category") in preferred_categories else 0



    # 2) 키워드 매칭 (60점) - mbti.json의 recommendedKeywords, hobbies.json의 tags/name 참고

    raw_keywords = mbti_info.get("recommendedKeywords", [])

    hobby_tags = [t.replace(" ", "").lower() for t in hobby.get("tags", [])]

    hobby_name = (hobby.get("name") or "").replace(" ", "").lower()



    match_count = 0

    for kw in raw_keywords:

        clean_kw = kw.replace(" ", "").lower()

        # 키워드가 취미 이름이나 태그에 포함되어 있는지 검사 (띄어쓰기 무시)

        if clean_kw in hobby_name or any(clean_kw in t for t in hobby_tags):

            match_count += 1



    total_kw_len = max(len(raw_keywords), 1)

    tag_score = round((match_count / total_kw_len) * 60)



    return min(100, category_score + tag_score)





def _calc_relation_score(hobby, current_hobbies):

    """S2: 취미 연관성 (Max 70% + Avg 30% 혼합) - hobbies.json의 relatedHobbies, category 참고"""

    if not current_hobbies:

        return 50



    hobby_id = hobby.get("id")

    hobby_rel = set(hobby.get("relatedHobbies") or [])

    hobby_cat = hobby.get("category")



    scores = []

    for other in current_hobbies:

        pts = 0

        other_rel = set(other.get("relatedHobbies") or [])

        if hobby_id in other_rel or other.get("id") in hobby_rel:

            pts += 60

        if hobby_cat and hobby_cat == other.get("category"):

            pts += 40

        scores.append(min(100, pts))



    if not scores:

        return 0



    return round(max(scores) * 0.7 + (sum(scores) / len(scores)) * 0.3)





def _calc_pref_score(hobby, prefs):

    """S3: 개인 선호 매칭 - hobbies.json의 socialType, indoorOutdoor, activityLevel 참고"""

    prefs = prefs or {}

    points = 0.0



    # 1) 활동 인원

    u_soc = prefs.get("socialType", "BOTH")

    h_soc = hobby.get("socialType", "BOTH")

    if u_soc == "BOTH" or h_soc == "BOTH" or u_soc == h_soc:

        points += 33.3



    # 2) 실내/야외

    u_loc = prefs.get("indoorOutdoor", "BOTH")

    h_loc = hobby.get("indoorOutdoor", "BOTH")

    if u_loc == "BOTH" or h_loc == "BOTH" or u_loc == h_loc:

        points += 33.3



    # 3) 신체 활동량

    u_act = prefs.get("activityLevel")

    if not u_act or u_act == hobby.get("activityLevel"):

        points += 33.4



    return min(100, round(points))





def _calc_cond_score(hobby, conds):

    """S4: 조건 제약 매칭 - hobbies.json의 budgetTier, timeRequired 참고"""

    conds = conds or {}

    points = 0



    # 1) 예산 비교 (초과 시 단계별 감점 완화)

    u_bud = _BUDGET_RANK.get(conds.get("budgetTier", "HIGH"), 3)

    h_bud = _BUDGET_RANK.get(hobby.get("budgetTier", "LOW"), 1)

    bud_diff = h_bud - u_bud

    if bud_diff <= 0:

        points += 50

    elif bud_diff == 1:

        points += 25



    # 2) 소요 시간 비교 (초과 시 단계별 감점 완화)

    u_time = _TIME_RANK.get(conds.get("timeRequired", "FULL_DAY"), 3)

    h_time = _TIME_RANK.get(hobby.get("timeRequired", "1HOUR"), 1)

    time_diff = h_time - u_time

    if time_diff <= 0:

        points += 50

    elif time_diff == 1:

        points += 25



    return points





def _calc_purpose_score(hobby, user_purposes):

    """S5: 라이프스타일/목적 다중 매칭 (0 ~ 100점) - hobbies.json의 purpose 참고"""

    if not user_purposes:

        return 50  # 선택 항목이 없을 경우 중립 기본값



    # 단일 문자열로 들어올 경우 리스트 형태로 통일

    if isinstance(user_purposes, str):

        user_purposes = [user_purposes]



    user_purposes_set = set(user_purposes)

    hobby_purposes = set(hobby.get("purpose") or [])



    # 선택된 목적과 취미 목적 간의 교집합 추출

    matched = user_purposes_set & hobby_purposes

    if not matched:

        return 0



    # 선택한 개수 대비 일치 비율 (최소 1개 이상 일치 시 40점 + 비율별 최대 60점)

    match_ratio = len(matched) / len(user_purposes_set)

    score = 40 + (match_ratio * 60)

   

    return min(100, round(score))





def _calc_novelty_score(hobby):

    """S6: 새로움 점수 - hobbies.json의 noveltyScore 참고"""

    return (hobby.get("noveltyScore") or 5) * 10





# ==========================================

# 3. 종합 점수 연산

# ==========================================



def evaluate_hobby(hobby, mbti_info, current_hobbies, user_input):

    s1 = _calc_mbti_score(hobby, mbti_info)

    s2 = _calc_relation_score(hobby, current_hobbies)

    s3 = _calc_pref_score(hobby, user_input.get("preference"))

    s4 = _calc_cond_score(hobby, user_input.get("condition"))

    s5 = _calc_purpose_score(hobby, user_input.get("purpose"))

    s6 = _calc_novelty_score(hobby)



    total_score = (

        s1 * _WEIGHTS["MBTI"]

        + s2 * _WEIGHTS["RELATION"]

        + s3 * _WEIGHTS["PREF"]

        + s4 * _WEIGHTS["COND"]

        + s5 * _WEIGHTS["PURPOSE"]

        + s6 * _WEIGHTS["NOVELTY"]

    )



    # 입문자 보정: 기존 취미 이력이 없을 때 EASY 난이도 5점 가산 - hobbies.json의 difficulty 참고

    if not current_hobbies and hobby.get("difficulty") == "EASY":

        total_score += 5.0


    scores = {
        "mbti_score": s1,
        "relation_score": s2,
        "preference_score": s3,
        "condition_score": s4,
        "purpose_score": s5,
        "novelty_score": s6,
    }
    
    return {

        "hobby": hobby,
        "total_score": round(min(100.0, total_score), 1),

        **scores,

        "reasons": _build_reasons(
            scores,
            has_history=bool(current_hobbies)
            )
    }





# ==========================================

# 4. 최종 다양성 추천 추출 (Main API 엔트리)

# ==========================================



def make_recommendations(hobbies, mbti_info, user_input):

    history_ids = set(user_input.get("history") or [])

    current_hobbies = [h for h in hobbies if h.get("id") in history_ids]



    # 1) 전체 취미 평가 (기존 경험 취미 제외)

    scored_list = []

    for hobby in hobbies:

        if hobby.get("id") in history_ids:

            continue

        evaluated = evaluate_hobby(hobby, mbti_info, current_hobbies, user_input)

        scored_list.append(evaluated)



    if not scored_list:

        return []



    scored_list.sort(key=lambda x: x["total_score"], reverse=True)

    recommendations = []



    # 2) Safe Pick (확장형): 취미 연관성 점수 60점 이상 중 최상위 점수

    safe_candidates = [item for item in scored_list if item["relation_score"] >= 60]

    safe_pick = safe_candidates[0] if safe_candidates else scored_list[0]

    safe_pick["badge"] = "Safe Pick (확장형)"

    recommendations.append(safe_pick)



    # 3) Wild Card (도전형): 참신성 중심 (novelty 가중치 부여 및 relation 감점 반영)

    remaining_for_wild = [item for item in scored_list if item != safe_pick]

    if remaining_for_wild:

        wild_pick = max(

            remaining_for_wild,

            key=lambda x: (x["novelty_score"] * 2 - x["relation_score"], x["mbti_score"])

        )

    else:

        wild_pick = safe_pick



    wild_pick["badge"] = "Wild Card (도전형)"

    recommendations.append(wild_pick)



    # 4) Adjacent Pick (보완형): Safe/Wild 제외 남은 목록 중 최상위 점수

    remaining = [item for item in scored_list if item not in (safe_pick, wild_pick)]

    if remaining:

        adjacent_pick = remaining[0]

        adjacent_pick["badge"] = "Adjacent Pick (보완형)"

        recommendations.insert(1, adjacent_pick)



    return recommendations 


# 추천 이유 TOP3 출력을 위한 함수
def _build_reasons(scores, has_history):

    reason_candidates = [
        {
            "score": scores["mbti_score"] * _WEIGHTS["MBTI"],
            "text": "MBTI 성향과 잘 맞는 취미예요."
        },
        {
            "score": scores["preference_score"] * _WEIGHTS["PREF"],
            "text": "선호하는 활동 방식과 잘 맞아요."
        },
        {
            "score": scores["condition_score"] * _WEIGHTS["COND"],
            "text": "예산과 시간 조건에 잘 맞아요."
        },
        {
            "score": scores["purpose_score"] * _WEIGHTS["PURPOSE"],
            "text": "원하는 취미 목적과 잘 맞아요."
        },
        {
            "score": scores["novelty_score"] * _WEIGHTS["NOVELTY"],
            "text": "새롭게 도전해보기 좋은 취미예요."
        }
    ]

    # 기존 취미를 선택한 경우에만 연관성 이유 추가
    if has_history:
        reason_candidates.append({
            "score": scores["relation_score"] * _WEIGHTS["RELATION"],
            "text": "기존 취미와 연관성이 높아요."
        })

    reason_candidates.sort(
        key=lambda reason: reason["score"],
        reverse=True
    )

    return reason_candidates[:3]