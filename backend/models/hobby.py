import json
import config

_cache = None


def load_all():
    global _cache
    if _cache is None:
        with config.HOBBIES_PATH.open(encoding="utf-8") as handle: 
            _cache = json.load(handle)  # _cache에는 
            
    return _cache
