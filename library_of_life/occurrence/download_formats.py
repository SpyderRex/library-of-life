import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class DownloadFormats:
    """
    A class for interacting with the download formats section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="download_formats_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/download/describe"
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
            
    def describe_dwca_fields(self):
        """
        **Experimental.** Describes the fields present in a Darwin Core Archive format download.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/dwca"
        return hc.get(base_url+self.endpoint+resource)
        
    def describe_simple_avro_fields(self):
        """
        **Experimental.** Describes the fields present in a Simple Avro format download.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/simpleAvro"
        return hc.get(base_url+self.endpoint+resource)
        
    def describe_simple_csv_fields(self):
        """
        **Experimental.** Describes the fields present in a Simple CSV format download.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/simpleCsv"
        return hc.get(base_url+self.endpoint+resource)
        
    def describe_simple_parquet_fields(self):
        """
        **Experimental.** Describes the fields present in a Simple Parquet format download.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/simpleParquet"
        return hc.get(base_url+self.endpoint+resource)
        
    def describe_species_list_fields(self):
        """
        **Experimental.** Describes the fields present in a Species List format download.
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/speciesList"
        return hc.get(base_url+self.endpoint+resource)
        
    def describe_sql_fields(self):
        """
        **Very experimental.** Describes the fields available for searching or download when using an SQL query.  
        
        Args:
            None
            
        Returns:
            dict: A dictionary containing the field descriptions.
        """
        resource = "/sql"
        return hc.get(base_url+self.endpoint+resource)
  
  
  
        
        
  
  
  