from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
from requests.auth import HTTPBasicAuth
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class DerivedDatasets:
    """
    A class for interacting with the derived datasets section of the Registry API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="derived_datasets_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "derivedDataset"
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
    
    # Requires authentication. User must create an account with GBIF.    
    def create_new_derived_dataset(self, username=None, password=None, derived_dataset=None):
        """
        Creates a new derived dataset with the specified source dataset and records of what subset should be cited.
        
        Args:
            username (str): The username.
            password (str): The user's password.
            derived_dataset (dict): The derived dataset to be created.
            
        Returns:
            None
        """
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint, auth=auth, json=derived_dataset)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint, headers=headers, json=derived_dataset)
   
    def get_derived_dataset_record(self, doi_prefix, doi_suffix):
        """
        Returns a derived dataset record.
        
        Args:
            doi_prefix (str): The DOI prefix.
            doi_suffix (str): The DOI suffix.
        
        Returns:
            dict: A dictionary containing a derived dataset record.
        """
        resource = f"/{doi_prefix}/{doi_suffix}"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
    
    # Requires authentication and is restricted to administrators.     
    def update_derived_dataset(self, doi_prefix, doi_suffix, username=None, password=None, data=None):
        """
        Updates the values of a derived dataset. This is restricted to administrators.
        
        Args:
            doi_prefix (str): The doi prefix.
            doi_suffix (str): The doi suffix.
            username (str): The username.
            password (str): The user's password.
            data (dict): The data with which to update the derived dataset.
                          
        Returns:
            None
        """
        resource = f"/{doi_prefix}/{doi_suffix}"
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=auth, json=data)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, headers=headers, json=data)
         
    def get_derived_datasets_by_key(self, key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a derived datasets of a dataset matching the given key.
        
        Args:
            key (str): Dataset key.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a derived datasets of a dataset.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/dataset/{key}"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_derived_datasets_by_doi(self, doi_prefix, doi_suffix,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a derived datasets of a dataset matching the given DOI.
        
        Args:
            doi_prefix (str): The DOI prefix.
            doi_suffix (str): The DOI suffix.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a derived datasets of a dataset.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/dataset/{doi_prefix}/{doi_suffix}"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_derived_datasets_by_user(self, user,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a derived datasets of a dataset matching the given user.
        
        Args:
            user (str): A user. 
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a derived datasets of a dataset.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/user/{user}"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_derived_dataset_citation(self, doi_prefix, doi_suffix,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a derived dataset citation matching the given doi.
        
        Args:
            doi_prefix (str): The DOI prefix.
            doi_suffix (str): The DOI suffix.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a derived dataset citation.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{doi_prefix}/{doi_suffix}/citation"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_derived_dataset_related_datasets(self, doi_prefix, doi_suffix,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a derived dataset related datasets matching the given doi.
        
        Args:
            doi_prefix (str): The DOI prefix.
            doi_suffix (str): The DOI suffix.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a derived dataset related datasets.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{doi_prefix}/{doi_suffix}/datasets"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
             