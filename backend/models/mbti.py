import json
import config

_cache = None


def load_all():
    global _cache
    if _cache is None:
        with config.MBTI_PATH.open(encoding="utf-8") as handle:
            _cache = json.load(handle)
            
    return _cache