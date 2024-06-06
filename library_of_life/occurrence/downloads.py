from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class OccurrenceDownload:
    """
    A class for interacting with the download section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, cache_name="occurrence_download_cache", backend="sqlite", expire_after=3600):
        self.endpoint = "occurrence/download"
          
        if use_caching:
            requests_cache.install_cache(cache_name, backend=backend, expire_after=expire_after)
    
    # Requires authentication. User must have an account with GBIF.
    def request_download(self, username, password, request_body):
        """
        Starts the process of creating a download file. See the predicates section to consult the requests accepted by this service and the limits section to refer for information of how this service is limited per user.
        
        Args:
            username (str): The username.
            password (str): The user's password.
            request_body (dict): The JSON request body. See this endpoint's docs for schema.
            
        Returns:
            string: A download key.
        """
        resource = "/request"        
        return hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=(username, password), json=request_body)

    def retrieve_download(self, download_key):
        """
        Retrieves the download file if it is available.
        
        Args:
            download_key (str): An identifier for a download. Example : 0001005-130906152512535
            
        Returns:
            binary: A zip file of the downloaded data.
        """
        resource = f"/request/{download_key}"
        data = hc.get_for_content(base_url+self.endpoint+resource)
        with open(f"{download_key}.zip", "wb") as f:
            print(f"{download_key}.zip successfully downloaded")
            f.write(data)
        return f"{download_key}.zip"