import json
import config

_cache = None


def load_all():
    global _cache
    if _cache is None:
        with config.HOBBIES_PATH.open(encoding="utf-8") as handle: 
            _cache = json.load(handle)  # _cache에는 
            
    return _cache


def filter_all(q, category):
    """
    탐색 화면용 필터.

    q        : 이름·소개·태그 안에 포함된 검색어 (대소문자 무시)
    category : 카테고리가 정확히 일치하는 것만. 빈 값이면 전체.
    """
    items = load_all()
    query = (q or "").strip().lower()
    selected = (category or "").strip()
    result = []
    for item in items:
        # 카테고리를 고른 경우, 다른 분류는 건너뛴다.
        if selected and item.get("category") != selected:
            continue
        if query:
            # 한 문자열로 이어 붙여 "어디에든 있으면" 통과시킨다.
            blob = " ".join(
                [
                    item.get("name", ""),
                    item.get("summary", ""),
                    " ".join(item.get("tags") or []),
                ]
            ).lower()
            if query not in blob:
                continue
        result.append(item)
    return result