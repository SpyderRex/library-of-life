from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class GADMRegions:
    """
    A class for interacting with the GADM regions section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="gadm_regions_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "geocode/gadm"
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
            
    def get_subregions(self, gid, query: Optional[str]=None):
        """
        Lists sub-regions or divisions of a region.
        
        Args:
            gid (str): Required. GADM region.
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            
        Returns:
            dict: A dictionary containing listed subregions.
        """
        params: Dict[str, Any] = {}
        params_list = [("q", query)]
        hc.add_params(params, params_list)
        resource = f"/{gid}/subdivisions"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_details_for_gadm_region(self, gid):
        """
        Details for a single GADM region.
         
        Args:
            gid (str): Required. GADM region.
               
        Returns:
            dict: A dictionary containing GADM region details.
        """
        resource = f"/{gid}"
        return hc.get_for_content(base_url+self.endpoint+resource).decode("utf-8")
        
    def search_gadm_regions(self, query: Optional[str]=None,
                            gadm_level: Optional[str]=None,
                            gadm_gid: Optional[str]=None,
                            limit: Optional[int]=None,
                            offset: Optional[int]=None):
        """
        Search for GADM regions. When parameters are used the results are narrowed to results that are subdivisions of gadmGid at level gadmLevel.
        
        Args:
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            gadm_level (str): Optional. Limit to subdivisions at this level. Example : 2
            gadm_gid (str): Optional. Limit to subdivisions of this GADM region. Example : SLV.4_1
            limit (int): Optional. Number of items to return.
            offset (int): Offset parameter.
            
        Returns:
            dict: A dictionary containing listed subregions.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("q", query),
                ("gadmLevel", gadm_level),
                ("gadmGid", gadm_gid),
                ("limit", limit), 
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = "/search"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_3rd_level_gadm_subdivisions(self, level0, level1, level2, query: Optional[str]=None):
        """
        Lists third-level subdivisions of a second-level GADM subdivision.
        
        Args:
            level0 (str): Required. Top-level GADM region. Example : DNK
            level1 (str): Required. Level 1 GADM region. Example : DNK.1_1 
            level2 (str): Required. Level 2 GADM region. Example : DNK.1.1_1  
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            
        Returns:
            dict: A dictionary containing listed GADM regions.
        """
        params: Dict[str, Any] = {}
        params_list = [("q", query)]
        hc.add_params(params, params_list)
        resource = f"/browse/{level0}/{level1}/{level2}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_2nd_level_gadm_subdivisions(self, level0, level1, query: Optional[str]=None):
        """
        Lists second-level subdivisions of a first-level GADM subdivision.  
        
        Args:
            level0 (str): Required. Top-level GADM region. Example : DNK
            level1 (str): Required. Level 1 GADM region. Example : DNK.1_1 
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            
        Returns:
            dict: A dictionary containing listed GADM regions.
        """
        params: Dict[str, Any] = {}
        params_list = [("q", query)]
        hc.add_params(params, params_list)
        resource = f"/browse/{level0}/{level1}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_1st_level_gadm_subdivisions(self, level0, query: Optional[str]=None):
        """
        Lists first-level subdivisions of a top-level GADM region.  
        
        Args:
            level0 (str): Required. Top-level GADM region. Example : DNK
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            
        Returns:
            dict: A dictionary containing listed GADM regions.
        """
        params: Dict[str, Any] = {}
        params_list = [("q", query)]
        hc.add_params(params, params_list)
        resource = f"/browse/{level0}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_top_level_gadm_subdivisions(self, query: Optional[str]=None):
        """
        Lists GADM regions at the highest level.
           
        Args:
            query (str): Optional. Query for (sub)divisions matching a wildcard.
            
        Returns:
            dict: A dictionary containing listed GADM regions.
        """
        params: Dict[str, Any] = {}
        params_list = [("q", query)]
        hc.add_params(params, params_list)
        resource = "/browse"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
 
 
 
 
   
        
   
            
   