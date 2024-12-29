from flask_caching import Cache
from datetime import datetime, timedelta
import json

cache = Cache(config={
    'CACHE_TYPE': 'simple'  # Pode ser alterado para 'redis' se preferir
})

def init_cache(app):
    cache.init_app(app)

def cache_key(prefix, **kwargs):
    """Gera uma chave única para o cache"""
    key_parts = [prefix]
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)

def get_cached_data(key, callback, expires_in=3600):
    """
    Obtém dados do cache ou da fonte original
    expires_in: tempo em segundos (padrão 1 hora)
    """
    data = cache.get(key)
    if data is None:
        data = callback()
        if data:
            cache.set(key, data, timeout=expires_in)
    return data