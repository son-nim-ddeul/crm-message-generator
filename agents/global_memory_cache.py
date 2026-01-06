
_global_memory_cache = {}


def set_global_memory_cache(key: str, value: dict):
    global _global_memory_cache
    if key not in _global_memory_cache:
        _global_memory_cache[key] = {}
    _global_memory_cache[key].update(value)
    print(f"set_global_memory_cache: {key} = {_global_memory_cache[key]}")


def get_global_memory_cache(key: str):
    global _global_memory_cache
    print(f"get_global_memory_cache: {key} = {_global_memory_cache.get(key)}")
    return _global_memory_cache.get(key)
