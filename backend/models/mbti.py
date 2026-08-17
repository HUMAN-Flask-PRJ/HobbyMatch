import json
import config


# app.py에서 서버 시작 시 mbti.load_all() 호출
# 처음 한 번 읽은 뒤 _cache에 저장
# 다음 호출부터는 JSON 파일을 다시 읽지 않고 캐시에 들어있는 값을 반환
_cache = None


def load_all():
    global _cache
    if _cache is None:
        with config.MBTI_PATH.open(encoding="utf-8") as handle:
            _cache = json.load(handle)
            
    return _cache