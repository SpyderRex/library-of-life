from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class ParticipantNodes:
    """
    A class for interacting with the participants nodes section of the Registry API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="nodes_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "node"
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
          
    def list_all_nodes(self, identifier_type: Optional[str]=None,
                        identifier: Optional[str]=None,
                        machine_tag_namespace: Optional[str]=None,
                        machine_tag_name: Optional[str]=None,
                        machine_tag_value: Optional[str]=None,
                        modified: Optional[str]=None,
                        query: Optional[str]=None,
                        limit: Optional[int]=None,
                        offset: Optional[int]=None):
        """
        Returns a list of all current publishing organizations (deleted nodes are not listed).
        
        Args:
            identifier_type (str): Optional. An identifier type for the identifier parameter. Available values : URL, LSID, HANDLER, DOI, UUID, FTP, URI, UNKNOWN, GBIF_PORTAL, GBIF_NODE, GBIF_PARTICIPANT, GRSCICOLL_ID, GRSCICOLL_URI, IH_IRN, ROR, GRID, CITES, SYMBIOTA_UUID, WIKIDATA, NCBI_BIOCOLLECTION.
            identifier (str): Optional. An identifier of the type given by the identifierType parameter, for example a DOI or UUID.
            machine_tag_namespace (str): Optional: Filters for entities with a machine tag in the specified namespace.
            machine_tag_name (str): Optional. Filters for entities with a machine tag with the specified name (use in combination with the machineTagNamespace parameter).
            machine_tag_value (str): Optional. Filters for entities with a machine tag with the specified value (use in combination with the machineTagNamespace and machineTagName parameters).
            modified (str): Optional. The modified date of the dataset. Accepts ranges and a '' can be used as a wildcard, e.g.:modified=2023-04-01,
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a list of publishing organizations.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("identifierType", identifier_type),
                ("identifier", identifier),
                ("machineTagNamespace", machine_tag_namespace),
                ("machineTagName", machine_tag_name),
                ("machineTagValue", machine_tag_value),
                ("modified", modified),
                ("q", query),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)
        
    def get_node_by_key(self, key):
        """
        Returns details of a single node matching the given key.
        
        Args:
            key (str): The key of the entity (dataset, organization, network etc.).
        
        Returns:
            dict: Returns details of a single node.
        """
        resource = f"/{key}"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
                 