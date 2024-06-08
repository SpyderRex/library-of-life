from typing import Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class NameParser:
    """
    A class for interacting with the name parser section of the Species API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="name_parser_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "parser"
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
      
    def parse_scientific_name(self, name):
        """
        Returns the ParsedName version of a scientific name.
        
        Args:
            name (array): A scientific name to parse. Repeat to parse several names.
        
        Returns:
            list: A list containing a parsed scientific name information.
        """
        params: Dict[str, Any] = {}
        params_list = [("name", name)]
        hc.add_params(params, params_list)
        resource = "/name"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def parse_scientific_name_list(self, username=None, password=None, names=None):
        """
        Parses a list of scientific names supplied as a JSON list, a form request or a plain text file with Unix (\\n) line endings. In all cases the names should use UTF-8 encoding.
        
        Args:
            username (str): The username.
            password (str): The user's password.
            names (list): A list of the scientific names to parse, either as a string or a list.
            
        Returns:
            dict: A dictionary containing the parsed names.
        """
        resource = "/name"
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=auth, json=names)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, headers=headers, json=names)
     
            
               