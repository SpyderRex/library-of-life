from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class SingleOccurrence:
    """
    A class for interacting with the single occurrences section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="single_occurrence_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence"
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
                     
    def get_occurrence_by_id(self, gbif_id):
        """
        Returns details for a single, interpreted occurrence.
        
        Args:
            gbif_id (int): Integer gbifId for the occurrence. Example : 1258202889.
        
        Returns:
            dict: A dictionary containing details for a single occurrence.
        """
        resource = f"/{gbif_id}"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
        
    def get_occurrence_by_dataset_key_and_occurrence_id(self, dataset_key, occurrence_id):
        """
        Returns details for a single, interpreted occurrence.
        
        Args:
            dataset_key (str): UUID key for the dataset. Example : e053ff53-c156-4e2e-b9b5-4462e9625424.
            occurrence_id (str): Occurrence ID from the dataset. Example : urn:catalog:MO:Tropicos:100889255.
        
        Returns:
            dict: A dictionary containing details for a single occurrence.
        """
        resource = f"/{dataset_key}/{occurrence_id}"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
             
    def get_occurrence_fragment_by_id(self, gbif_id):
        """
        Returns a single occurrence fragment in its raw form (JSON or XML).
        
        Args:
            gbif_id (int): Integer gbifId for the occurrence. Example : 1258202889.
        
        Returns:
            dict: A dictionary containing details for a single occurrence fragment.
        """
        resource = f"/{gbif_id}/fragment"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
             
    def get_occurrence_fragment_by_dataset_key_and_occurrence_id(self, dataset_key, occurrence_id):
        """
        Returns a single occurrence fragment in its raw form (JSON or XML) by its dataset key and occurrenceId in that dataset. 
        
        Args:
            dataset_key (str): UUID key for the dataset. Example : e053ff53-c156-4e2e-b9b5-4462e9625424.
            occurrence_id (str): Occurrence ID from the dataset. Example : urn:catalog:MO:Tropicos:100889255.
        
        Returns:
            dict: A dictionary containing details for a single occurrence fragment.
        """
        resource = f"/{dataset_key}/{occurrence_id}/fragment"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
             
    def get_verbatim_occurrence_by_id(self, gbif_id):
        """
        Returns a single, verbatim occurrence without any interpretation.
         
        Args:
            gbif_id (int): Integer gbifId for the occurrence. Example : 1258202889.
        
        Returns:
            dict: A dictionary containing details for a single occurrence.
        """
        resource = f"/{gbif_id}/verbatim"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
           
    def get_verbatim_occurrence_by_dataset_key_and_occurrence_id(self, dataset_key, occurrence_id):
        """
        Returns a single, verbatim occurrence without any interpretation by its dataset key and occurrenceId.
        
        Args:
            dataset_key (str): UUID key for the dataset. Example : e053ff53-c156-4e2e-b9b5-4462e9625424.
            occurrence_id (str): Occurrence ID from the dataset. Example : urn:catalog:MO:Tropicos:100889255.
        
        Returns:
            dict: A dictionary containing details for a single occurrence.
        """
        resource = f"/{dataset_key}/{occurrence_id}/verbatim"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
            
    def get_related_occurrences_by_id(self, gbif_id):
        """
       Returns a list of related occurrences. (Experimental)
        
        Args:
            gbif_id (int): Integer gbifId for the occurrence. Example : 1258202889.
        
        Returns:
            dict: A dictionary containing details for occurrences.
        """
        resource = f"/{gbif_id}/experimental/related"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
            
    def get_occurrence_terms(self):
        """
        Returns a list of the definitions of the terms (JSON properties, field names) of occurrences.  
        
        Args:
            None
         
        Returns:
            list: A list containing a list of definitions.
        """
        resource = "/term"
        return hc.try_get_except_json_decode_err(base_url, self.endpoint, resource)
      