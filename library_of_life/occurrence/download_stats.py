from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class DownloadStats:
    """
    A class for interacting with the download statistics section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="download_stats_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/download/statistics"
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
            
    def get_summarized_download_stats(self, from_date: Optional[str]=None,
                                to_date: Optional[str]=None,
                                publishing_country: Optional[str]=None,
                                dataset_key: Optional[str]=None,
                                publishing_org_key: Optional[str]=None,
                                limit: Optional[int]=None,
                                offset: Optional[int]=None):
        """
        Filters for downloads matching the provided criteria, then provide counts by year, month and dataset of the total number of downloads, and the total number of records included in those downloads.
        
        Args:
            from_date (str[datetime]): Optional. The year and month (YYYY-MM) to start from.
            to_date (str[datetime]): Optional. The year and month (YYYY-MM) to end at.
            publishing_country (str): Optional. The ISO 3166-2 code for the publishing organization's country, territory or island. See this endpoint's docs for available values.
            dataset_key (str): Optional. The uuid for a dataset.
            publishing_org_key (str): Optional. The uuid for a publishing organization.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            dict: A dictionary containing download statistics.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("fromDate", from_date),
                ("toDate", to_date),
                ("publishingCountry", publishing_country),
                ("datasetKey", dataset_key),
                ("publishingOrgKey", publishing_org_key),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)
        
    def export_summarized_download_stats(self, from_date,
                                to_date,
                                publishing_country,
                                export_format="TSV",
                                dataset_key: Optional[str]=None,
                                publishing_org_key: Optional[str]=None):
        """
        Filters for downloads matching the provided criteria, then provide counts by year, month and dataset of the total number of downloads, and the total number of records included in those downloads.
        
        Args:
            from_date (str[datetime]): Required. The year and month (YYYY-MM) to start from.
            to_date (str[datetime]): Required. The year and month (YYYY-MM) to end at.
            publishing_country (str): Required. The ISO 3166-2 code for the publishing organization's country, territory or island. See this endpoint's docs for available values.
            dataset_key (str): Optional. The uuid for a dataset.
            publishing_org_key (str): Optional. The uuid for a publishing organization.
                
        Returns:
            dict: A dictionary containing download statistics.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("format", export_format),
                ("fromDate", from_date),
                ("toDate", to_date),
                ("publishingCountry", publishing_country),
                ("datasetKey", dataset_key),
                ("publishingOrgKey", publishing_org_key)]
        hc.add_params(params, params_list)
        resource = "/export"
        try:
            return hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params).decode("utf-8")
        except AttributeError:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
            
    def get_summarized_download_stats_for_user_country(self, from_date: Optional[str]=None,
                                to_date: Optional[str]=None,
                                user_country: Optional[str]=None):
        """
        Provides counts of user downloads by month, grouped by the user's ISO 3166-2 country, territory or island.  
        
        Args:
            from_date (str[datetime]): Optional. The year and month (YYYY-MM) to start from.
            to_date (str[datetime]): Optional. The year and month (YYYY-MM) to end at.
            user_country (str): Optional. The ISO 3166-2 code for the user's country, territory or island. See this endpoint's docs for available values.
               
        Returns:
            dict: A dictionary containing download statistics.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("fromDate", from_date),
                ("toDate", to_date),
                ("userCountry", user_country)]
        resource = "/downloadsByUserCountry"
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_summarized_download_stats_by_dataset(self, from_date: Optional[str]=None,
                                to_date: Optional[str]=None,
                                publishing_country: Optional[str]=None,
                                dataset_key: Optional[str]=None,
                                publishing_org_key: Optional[str]=None):
        """
        Summarizes downloads by month, filtered by a publishing organization's country, territory or island and/or a single dataset.  
        
        Args:
            from_date (str[datetime]): Optional. The year and month (YYYY-MM) to start from.
            to_date (str[datetime]): Optional. The year and month (YYYY-MM) to end at.
            publishing_country (str): Optional. The ISO 3166-2 code for the publishing organization's country, territory or island. See this endpoint's docs for available values.
            dataset_key (str): Optional. The uuid for a dataset.
            publishing_org_key (str): Optional. The uuid for a publishing organization.
              
        Returns:
            dict: A dictionary containing download statistics.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("fromDate", from_date),
                ("toDate", to_date),
                ("publishingCountry", publishing_country),
                ("datasetKey", dataset_key),
                ("publishingOrgKey", publishing_org_key)]
        hc.add_params(params, params_list)
        resource = "/downloadsByDataset"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_summarized_download_stats_by_source(self, from_date: Optional[str]=None,
                                to_date: Optional[str]=None,
                                source: Optional[str]=None):
        """
        Summarizes downloaded record totals by source, e.g. www.gbif.org or APIs. 
        
        Args:
            from_date (str[datetime]): Optional. The year and month (YYYY-MM) to start from.
            to_date (str[datetime]): Optional. The year and month (YYYY-MM) to end at.
            source (str): Optional. Restrict to a particular source.
        
        Returns:
            dict: A dictionary containing download statistics.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("fromDate", from_date),
                ("toDate", to_date),
                ("source", source)]
        resource = "/downloadsBySource"
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
    
        
    
   
  
     
                                    
            