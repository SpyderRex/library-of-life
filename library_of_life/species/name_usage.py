from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class NameUsage:
    """
    A class for interacting with the name usages section of the Species API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="name_usage_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "species"
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
            
    def get_usage_vernacular_names_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all vernacular names for a name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing all vernacular names for a name usage.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/vernacularNames"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_verbatim_name_usage_by_usage_key(self, usage_key):
        """
        Returns a verbatim name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            dict: A dictionary containing a verbatim name usage.
        """
        resource = f"/{usage_key}/verbatim"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
           
    def get_usage_descriptions_tocs(self, usage_key):
        """
        Returns a table of contents for all descriptions of a name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            dict: A dictionary containing a table of contents.
        """
        resource = f"/{usage_key}/toc"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_synonyms_by_usage_key(self, usage_key, language,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all vernacular names for a name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing all vernacular names for a name usage.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        headers = {"Accept-Language": language}
        resource = f"/{usage_key}/synonyms"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_species_profiles_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all species profiles for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing species profiles.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/speciesProfiles"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_related_name_usages_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all related name usages for a name usage.  
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing related name usages.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/related"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_references_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all references for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing references.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/references"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_parent_name_usages_by_usage_key(self, usage_key, language):
        """
        Returns all parent name usages for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
          
        Returns:
            dict: A dictionary containing parent name usages.
        """
        headers = {"Accept-Language": language}
        resource = f"/{usage_key}/parents"
        try:
            return hc.get(base_url+self.endpoint+resource, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
      
    def get_parsed_name_usage_by_usage_key(self, usage_key):
        """
        Returns the parsed name for a single name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            dict: A dictionary containing parsed name usage.
        """
        resource = f"/{usage_key}/name"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_metrics_by_usage_key(self, usage_key):
        """
        Returns metrics for a single name usage.  
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            dict: A dictionary containing metrics.
        """
        resource = f"/{usage_key}/metrics"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_media_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all media for a name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing media.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/media"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_iucn_red_list_category_for_usage_key(self, usage_key):
        """
        Returns the IUCN Red List Category for a name usage. If the matching IUCN usage does not contain a category, Not Evaluated (NE) is returned. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            dict: A dictionary an IUCN Red List Category.
        """
        resource = f"/{usage_key}/iucnRedListCategory"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_identifiers_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all identifiers for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing identifiers.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/identifier"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_distributions_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all distributions for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing distributions.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/distributions"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_descriptions_by_usage_key(self, usage_key,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns all descriptions for a name usage. 
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing descriptions.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{usage_key}/descriptions"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_recombinations_by_usage_key(self, usage_key, language):
        """
        Returns a list of all (re)combinations of a given basionym, excluding the basionym itself.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
          
        Returns:
            list: A list containing name usage recombinations.
        """
        headers = {"Accept-Language": language}
        resource = f"/{usage_key}/combinations"
        try:
            return hc.get(base_url+self.endpoint+resource, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_all_name_usage_children_by_usage_key(self, usage_key):
        """
        Returns a brief list of all child Name Usages for a parent Name Usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
        
        Returns:
            list: A list of child name usagea
        """
        resource = f"/{usage_key}/childrenAll"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_name_usage_children_by_usage_key(self, usage_key, language,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns a list of child Name Usages for a parent Name Usage.  
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing child name usages for a name usage.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        headers = {"Accept-Language": language}
        resource = f"/{usage_key}/children"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
     
    def get_single_name_usage_by_usage_key(self, usage_key, language):
        """
        Retrieves a single name usage.
        
        Args:
            usage_key (int): Name usage key. Example : 5231190.
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
          
        Returns:
            dict: A dictionary containing a single name usage.
        """
        headers = {"Accept-Language": language}
        resource = f"/{usage_key}"
        try:
            return hc.get(base_url+self.endpoint+resource, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def get_root_name_usage_for_dataset(self, dataset_key, language,
                                   limit: Optional[int]=None,
                                   offset: Optional[int]=None):
        """
        Returns root name usages for a checklist dataset. 
        
        Args:
            dataset_key (int): A UUID of a checklist dataset. Example : d7dddbf4-2cf0-4f39-9b2a-bb099caae36c   
            language (str): Language for vernacular names, given as an ISO 639-1 two-letter code from api's vocabulary. See this endpoint's docs for available values.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing root name usages.
        """
        params: Dict[str, Any] = {}
        params_list = [
                    ("limit", limit),
                    ("offset", offset)]
        hc.add_params(params, params_list)
        headers = {"Accept-Language": language}
        resource = f"/root/{dataset_key}"
        try:
            return hc.get_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
        except JSONDecodeError:
            response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params, headers=headers)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            