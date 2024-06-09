from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class Inventories:
    """
    A class for interacting with the inventories section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="inventories_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/counts"
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
            
    def get_inventory_by_basis_of_record(self):
        """
        Lists occurrence counts by basis of record.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the inventory counts.
        """
        resource = "/basisOfRecord"
        return hc.get(base_url+self.endpoint+resource)
        
    def get_inventory_by_year(self, year: Optional[str]=None):
        """
        Lists occurrence counts by year.
        
        Args:
            year (str): Optional. Limit to occurrences from a particular year or range of years. Example : 1981,1991
            
        Returns:
            dict: A dictionary containing the inventory counts.
        """
        params: Dict[str, Any] = {}
        params_list = [("year", year)]
        hc.add_params(params, params_list)
        resource = "/year"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_inventory_by_dataset(self, country: Optional[str]=None,
                                 taxon_key: Optional[int]=None):
        """
        Lists occurrence counts for datasets that cover a given taxon or country.
         
        Args:
            country (str): Optional. Limit to occurrences in an ISO 3166 country or area. 
            taxon_key (int): Optional. Limit to occurrences of a particular taxon. 
                
        Returns:
            dict: A dictionary containing the inventory counts.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("country", country),
                ("taxonKey", taxon_key)]
        hc.add_params(params, params_list)
        resource = "/datasets"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_inventory_by_publishing_country(self, publishing_country: Optional[str]=None):
        """
        Lists occurrence counts by publishing country.
        
        Args:
            publishing_country (str): Optional. Limit to data published by a particular country.
        
        Returns:
            dict: A dictionary containing the inventory counts.
        """
        params: Dict[str, Any] = {}
        params_list = [("publishingCountry", publishing_country)]
        hc.add_params(params, params_list)
        resource = "/publishingCountries"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_inventory_by_country(self, country: Optional[str]=None):
        """
        Lists occurrence counts for all countries that publish data about the given country. 
        
        Args:
            country (str): Optional. Count only occurrences from a country or area.
        
        Returns:
            dict: A dictionary containing the inventory counts.
        """
        params: Dict[str, Any] = {}
        params_list = [("country", country)]
        hc.add_params(params, params_list)
        resource = "/countries"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
   
   
        
        
 
   
        
        
     