from typing import Optional, Dict, Any

import requests
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
    def __init__(self, use_caching=False, 
                cache_name="occurrence_download_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/download"
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
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=auth, json=request_body)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, headers=headers, json=request_body)
   
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

    #Requires authentication. User must have an account with GBIF.      
    def cancel_running_download(self, username=None, password=None, download_key=None):
        """
        Cancel a running download.
        
        Args:
            download_key (str): An identifier for a download. Example : 0001005-130906152512535
        
        Returns:
            string: Success or failure message for download deletion.
        """
        resource = f"/request/{download_key}"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.delete_with_auth(base_url+self.endpoint+resource, auth=auth)
            if response == 204:
                return("Occurrence download canceled")
            elif response == 404:
                return("Invalid occurrence download key")
            else:
                return(response)
        else: #OAuth
            headers = self.auth_headers
            response = hc.delete_with_auth(base_url+self.endpoint+resource, headers=headers)
            if response == 204:
                return "Occurrence download canceled"
            elif response == 404:
                return "Invalid occurrence download key"
            else:
                return response

    # Requires authentication. User must have an account with GBIF.
    def validate_sql(self, username, password, request_body):
        """
        Validates the SQL in an SQL download request. See the SQL section for information on what queries are accepted.  
        
        Args:
            username (str): The username.
            password (str): The user's password.
            request_body (dict): The JSON request body. See this endpoint's docs for schema.
            
        Returns:
            string: A message indicating if the SQL is valid or not.
        """
        resource = "/request/validate"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=auth, json=request_body)
            if "404" in response["error"]:
                return "Invalid query, see other documentation."
            else:
                return response
                
        else: #OAuth
            headers = self.auth_headers
            response = hc.post_with_auth_and_json(base_url+self.endpoint+resource, headers=headers, json=request_body)
            if "404" in response["error"]:
                return "Invalid query, see other documentation."
            else:
                return response
                
    def convert_query_into_download_predicate(self, download_format, 
                                notification_address: Optional[str]=None,
                                verbatim_extensions: Optional[str]=None):
        """
        Takes a search query used for the ordinary search API and returns a predicate suitable for the download API. In many cases, a query from the website can be converted using this method.
        
        Args:
            download_format (str): The download format (Note: I haven't been able to find from the API documentation what the possible values are here.)
            notification_address (str): Email notification address.
            verbatim_extensions (str): Verbatim extensions to include in a Darwin Core Archive download.
            
        Returns:
            dict: A dictionary containing the response.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("notification_address", notification_address),
            ("format", download_format),
            ("verbatimExtensions", verbatim_extensions)]
        hc.add_params(params, params_list)
        resource = "request/predicate"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        