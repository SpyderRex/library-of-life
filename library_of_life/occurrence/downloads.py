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
        
    def get_occurrence_download_info_by_key(self, download_key, 
                                statistics: Optional[bool]=None):
        """
        Retrieves the status (in-progress, complete, etc), definition and location of an occurrence download. Authorized users see additional details on their own downloads
        
        Args:
            download_key (str): The key for the download.
            statistics (bool): Optional. If true it also shows number of organizations and countries.
            
        Returns:
            dict: A dictionary containing occurrence download information.
        """
        params: Dict[str, Any] = {}
        params_list = [("statistics", statistics)]
        hc.add_params(params, params_list)
        resource = f"/{download_key}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_occurrence_download_info_by_doi(self, doi_prefix, doi_suffix):
        """
        Retrieves the status (in-progress, complete, etc), definition and location of an occurrence download. Authorized users see additional details on their own downloads.
        
        Args:
            doi_prefix (str): The DOI prefix of the download, 10.15468 for GBIF downloads
            doi_suffix (str): The DOI suffix of the download, begins 'dl.' for GBIF downloads
            
        Returns:
            dict: A dictionary containing occurrence download information.
        """
        resource = f"/{doi_prefix}/{doi_suffix}"
        return hc.get(base_url+self.endpoint+resource)
    
    #Requires authentication. User must have an account with GBIF.
    def get_user_download_info(self, user, username, password,
                        status: Optional[str]=None,
                        from_date: Optional[str]=None,
                        statistics: Optional[bool]=None,
                        limit: Optional[int]=None,
                        offset: Optional[int]=None):
        """
        Retrieves the status, definitions and locations of all occurrence download by your own user.
        
        Args:
            user (str): Required. Username (administrator account required to see other users).
            username (str): Your username.
            password (str): Your password.
            status (str): Optional. List of statuses to filter by. Available values : PREPARING, RUNNING, SUCCEEDED, CANCELLED, KILLED, FAILED, SUSPENDED, FILE_ERASED
            from_date (str[datetime]): Optional. Date time in ISO format to filter downloads by its creation date.
            statistics (bool): Optional. If true it returns the counts of datasets, organizations and countries. By default it's true to maintain backwards compatibility. Default value : true
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            dict: A dictionary containing the download information for the user.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("status", status),
                ("from", from_date),
                ("statistics", statistics),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/user/{user}"
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.get_with_auth_and_params(base_url+self.endpoint+resource, auth=auth, params=params)  
        else: #OAuth
            headers = self.auth_headers
            return hc.get_with_auth_and_params(base_url+self.endpoint+resource, headers=headers, params=params)
            
    #Requires authentication. User must have an account with GBIF.
    def get_user_download_count(self, user, username, password,
                        status: Optional[str]=None,
                        from_date: Optional[str]=None,
                        limit: Optional[int]=None,
                        offset: Optional[int]=None):
        """
        Retrieves the counts of occurrence downloads done by the user.  
        
        Args:
            user (str): Required. Username (administrator account required to see other users).
            username (str): Your username.
            password (str): Your password.
            status (str): Optional. List of statuses to filter by. Available values : PREPARING, RUNNING, SUCCEEDED, CANCELLED, KILLED, FAILED, SUSPENDED, FILE_ERASED
            from_date (str[datetime]): Optional. Date time in ISO format to filter downloads by its creation date.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            int: The download count for the user.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("status", status),
                ("from", from_date),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/user/{user}/count"
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.get_with_auth_and_params(base_url+self.endpoint+resource, auth=auth, params=params)  
        else: #OAuth
            headers = self.auth_headers
            return hc.get_with_auth_and_params(base_url+self.endpoint+resource, headers=headers, params=params)
            
    def list_datasets_in_occurrence_download_by_doi(self, doi_prefix, doi_suffix,
                                            limit: Optional[int]=None, 
                                            offset: Optional[int]=None):
        """
        Shows the datasets with occurrences present in the given occurrence download.  
        
        Args:
            doi_prefix (str): The DOI prefix of the download, 10.15468 for GBIF downloads
            doi_suffix (str): The DOI suffix of the download, begins 'dl.' for GBIF downloads
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            dict: A dictionary containing dataset usage within an occurrence download information.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
   
        resource = f"/{doi_prefix}/{doi_suffix}/datasets"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def list_datasets_in_occurrence_download_by_key(self, download_key,
                                            dataset_title: Optional[str]=None,
                                            sort_by: Optional[str]=None,
                                            sort_order: Optional[str]=None,
                                            limit: Optional[int]=None, 
                                            offset: Optional[int]=None):
        """
        Shows the datasets with occurrences present in the given occurrence download.  
        
        Args:
            download_key (str): Required. The download key.
            dataset_title (str): Optional. Title of the dataset to filter by.
            sort_by (str): Optional. Field to sort the results by..Available values : DATASET_TITLE, COUNTRY_CODE, RECORD_COUNT
            sort_order (str): Optional. Sort order. Only taken into account when sortBy is used. Available values : ASC, DESC
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            
        Returns:
            dict: A dictionary containing dataset usage within an occurrence download information.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("datasetTitle", dataset_title),
                ("sortBy", sort_by),
                ("sortOrder", sort_order),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
   
        resource = f"/{download_key}/datasets"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def export_datasets_listed_in_occurrence_download(self, download_key, export_format="TSV"):
        """
        Shows the datasets with occurrences present in the given occurrence download in TSV or CSV format.
        
        Args:
            download_key (str): The key of the download.
            export_format (str): The export format. Available values : CSV, TSV. Default is TSV.
            
        Returns:
            dict: A dictionary containing dataset usage within an occurrence download information.
        """
        resource = f"/{download_key}/datasets/export?format={export_format.upper()}"
        return hc.get_for_content(base_url+self.endpoint+resource)
        
    def get_citation_for_download_by_key(self, download_key):
        """
        Shows the citation for the download.
        
        Args:
            download_key (str): The key for the download.
            
        Returns:
            dict: A dictionary containing the citation.
        """
        resource = f"/{download_key}/citation"
        try:
            return hc.get_for_content(base_url+self.endpoint+resource).decode("utf-8")
        except AttributeError:
            return hc.get(base_url+self.endpoint+resource)
            
    def get_citation_for_download_by_doi(self, doi_prefix, doi_suffix):
        """
        Shows the citation for the download.
        
        Args:
            doi_prefix (str): The DOI prefix of the download, 10.15468 for GBIF downloads
            doi_suffix (str): The DOI suffix of the download, begins 'dl.' for GBIF downloads
          
        Returns:
            dict: A dictionary containing the citation.
        """
        resource = f"/{doi_prefix}/{doi_suffix}/citation"
        try:
            return hc.get_for_content(base_url+self.endpoint+resource).decode("utf-8")
        except AttributeError:
            return hc.get(base_url+self.endpoint+resource)
            
    def list_download_activity_for_dataset(self, dataset_key,
                                show_download_details: Optional[bool]=None,
                                limit: Optional[int]=None,
                                offset: Optional[int]=None):
        """
        Lists the downloads in which data from a dataset has been included. The limit is set to a maximum of 100 results unless you set the showDownloadDetails parameter to false.
        
        Args:
            dataset_key (str): The key of the dataset 
            show_download_details (bool): Flag to indicate if we want the download details in the response. It defaults to true to keep backwards compatibility. Default value : true
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
       
        Returns:
            dict: A dictionary containing the download information.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("showDownloadDetails", show_download_details),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/dataset/{dataset_key}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
 
 
    
        
            
            
            
            
            
            
            
            
            
            