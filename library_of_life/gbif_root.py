import requests_cache

class GBIF:
    """
    A root class for the GBIF API.
    
    Attributes:
        base_url: The base URL for the GBIF API.
    """            
    def __init__(self, use_caching=False, cache_name="gbif_cache", backend="sqlite", expire_after=3600):
        self.base_url = "https://api.gbif.org/v1/"
          
        if use_caching:
            requests_cache.install_cache(cache_name, backend=backend, expire_after=expire_after)