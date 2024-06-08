from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class InstitutionsAndCollections:
    """
    A class for interacting with the institutions and collections section of the Registry API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="institutions_and_collections_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "grscicoll/search"
        self.auth_type = auth_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        
        if auth_type == 'OAuth':
            if not all([client_id, client_secret, token_url]):
                raise ValueError("Client ID, client secret, and token URL must be provided for OAuth authentication.")
            self.auth_headers = hc.get_oauth_headers(client_id, client_secret, token_url)
          
        if use_caching:
            requests_cache.install_cache(cache_name, backend=backend, expire_after=expire_after)
       
    def search_institutions_and_collections(self, country,
                                   query: Optional[str]=None,
                                   highlight: Optional[bool]=None,
                                   entity_type: Optional[str]=None,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns data on collections and institutions matching the search parameters.
        
        Args:
            country (str): Required. The 2-letter country code (as per ISO-3166-1) of the country. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            highlight (bool): Optional. Set hl=true to highlight terms matching the query when in fulltext search fields. The highlight will be an emphasis tag of class gbifHl.
            entity_type (str): Optional. Code of a GrSciColl institution or collection.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing data about collections and institutions.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("country", country),
                    ("q", query),
                    ("hl", highlight),
                    ("entityType", entity_type),
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)
          