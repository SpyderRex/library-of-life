from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class Metrics:
    """
    A class for interacting with the metrics section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="metrics_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/count"
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
            
    def get_occurrence_counts(self, basis_of_record: Optional[str]=None,
                             country: Optional[str]=None,
                             dataset_key: Optional[str]=None,
                             is_georeferenced: Optional[bool]=None,
                             issue: Optional[str]=None,
                             protocol: Optional[str]=None,
                             publishing_country: Optional[str]=None,
                             taxon_key: Optional[int]=None,
                             type_status: Optional[str]=None,
                             year: Optional[str]=None):
        """
        Returns occurrence counts for a predefined set of dimensions. The supported dimensions are enumerated in the /occurrence/count/schema service. The keys should be supplied as query parameters. An example for the count of georeferenced observations from Canada: /occurrence/count?country=CA&isGeoreferenced=true&basisOfRecord=OBSERVATION
        
        Args:
            basis_of_record (str): Optional. Count records with a particular basisOfRecord.
            country (str): Optional. Count records in the given country.
            dataset_key (str): Optional. Count records in a dataset.
            is_georeferenced (bool): Optional. Count only georeferenced (or not) records.
            issue (str): Optional. Count only records with this issue.
            protocol (str): Optional. Count records retrieved using the chosen protocol.
            publishing_country (str): Optional. Count records published by the given country.
            taxon_key (int): Optional. Count records of a particular taxon.
            type_status (str): Optional. Count records with this type status.
            year (int): Optional. Count records from this year.
            
        Returns:
            int: The number of records.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("basisOfRecord", basis_of_record),
                ("country", country),
                ("datasetKey", dataset_key),
                ("isGeoreferenced", is_georeferenced),
                ("issue", issue),
                ("protocol", protocol),
                ("publishingCountry", publishing_country),
                ("taxonKey", taxon_key),
                ("typeStatus", type_status),
                ("year", year)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)
        
    def get_supported_occurrence_count_metrics(self):
        """
        List the metrics supported by the service.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the supported metrics.
        """
        resource = "/schema"
        return hc.get(base_url+self.endpoint+resource)
   
 
      
           
                     
         
 

            
 
                                    
                                                                                                          
                       
                                             
                  