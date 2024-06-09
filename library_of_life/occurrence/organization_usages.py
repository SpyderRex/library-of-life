from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class OrganizationUsage:
    """
    A class for interacting with the organization usage section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="organization_usage_cache", 
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
            
    def list_organizations_in_download(self, download_key,
                            organization_title: Optional[str]=None,
                            sort_by: Optional[str]=None,
                            sort_order: Optional[str]=None,
                            limit: Optional[int]=None,
                            offset: Optional[int]=None):
        """
        Shows the countries with occurrences present in the given occurrence download.
        
        Args:
            download_key (str): Required. The key of the download.
            organization_title (str): Optional. Title of the organization to filter by.
            sort_by (str): Optional. Field to sort the results by. Available values : ORGANIZATION_TITLE, COUNTRY_CODE, RECORD_COUNT
            sort_order (str): Optional. Sort order. Only taken into account when sortBy is used. Available values : ASC, DESC
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            dict: A dictionary containing country usage within an occurrence download information.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("organizationTitle", organization_title),
                ("sortBy", sort_by),
                ("sortOrder", sort_order),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{download_key}/organizations"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
  