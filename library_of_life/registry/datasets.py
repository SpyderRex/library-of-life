from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class Datasets:
    """
    A class for interacting with the datasets section of the Registry API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="datasets_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "dataset"
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

    def list_datasets(self, country: Optional[str]=None, 
                        dataset_type: Optional[str]=None,
                        identifier_type: Optional[str]=None,
                        identifier: Optional[str]=None,
                        machine_tag_namespace: Optional[str]=None,
                        machine_tag_name: Optional[str]=None,
                        machine_tag_value: Optional[str]=None,
                        modified: Optional[dict]=None,
                        query: Optional[str]=None,
                        limit: Optional[int]=None,
                        offset: Optional[int]=None,
                        ):
        """
        Returns a list of all current datasets.
        
        Args:
            country (str): Optional. The 2-letter country code (as per ISO-3166-1) of the country publishing the dataset. See this endpoint's docs for available values.
            dataset_type (str): Optional. The primary type of the dataset. Available values : OCCURRENCE, CHECKLIST, METADATA, SAMPLING_EVENT, MATERIAL_ENTITY.
            identifier_type (str): Optional. An identifier type for the identifier parameter. Available values : URL, LSID, HANDLER, DOI, UUID, FTP, URI, UNKNOWN, GBIF_PORTAL, GBIF_NODE, GBIF_PARTICIPANT, GRSCICOLL_ID, GRSCICOLL_URI, IH_IRN, ROR, GRID, CITES, SYMBIOTA_UUID, WIKIDATA, NCBI_BIOCOLLECTION
            identifier (str): Optional. An identifier of the type given by the identifierType parameter, for example a DOI or UUID.
            machine_tag_namespace (str): Optional. Filters for entities with a machine tag in the specified namespace.
            machine_tag_name (str): Optional. Filters for entities with a machine tag with the specified name (use in combination with the machineTagNamespace parameter).
            machine_tag_value (str): Optional. Filters for entities with a machine tag with the specified value (use in combination with the machineTagNamespace and machineTagName parameters).
            modified (dict): Optional. The modified date of the dataset. Accepts ranges and a '' can be used as a wildcard, e.g.:modified=2023-04-01,
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing list of current datasets.
        """ 
        params: Dict[str, Any] = {}
        params_list = [("country", country),
                       ("type", dataset_type),
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

    # Requires authentication. User must have an account with GBIF.
    def create_new_dataset(self, username=None, password=None, dataset=None):
        """
        Creates a new dataset. Note contacts, endpoints, identifiers, tags, machine tags, comments and metadata descriptions must be added in subsequent requests.
    
        Args:
            username (str): The username.
            password (str): The user's password.
            dataset (dict): The dataset to be created. See this endpoint's docs for the proper format.
        
        Returns:
            None
        """
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint, auth=auth, json=dataset)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint, headers=headers, json=dataset)
             
    def search_datasets(self, dataset_type: Optional[str]=None,
                        subtype: Optional[str]=None,
                        publishing_org: Optional[str]=None,
                        hosting_org: Optional[str]=None,
                        keyword: Optional[str]=None,
                        decade: Optional[int]=None,
                        publishing_country: Optional[str]=None,
                        hosting_country: Optional[str]=None,
                        license: Optional[str]=None,
                        project_id: Optional[str]=None,
                        taxon_key: Optional[int]=None,
                        record_count: Optional[str]=None,
                        modified_date: Optional[str]=None,
                        doi: Optional[str]=None,
                        network_key: Optional[str]=None,
                        endorsing_node_key: Optional[str]=None,
                        installation_key: Optional[str]=None,
                        endpoint_type: Optional[str]=None,
                        query: Optional[str]=None,
                        highlight: Optional[bool]=None,
                        facet: Optional[list]=None,
                        facet_min_count: Optional[int]=None,
                        facet_multiselect: Optional[bool]=None,
                        facet_limit: Optional[int]=None,
                        facet_offset: Optional[int]=None,
                        limit: Optional[int]=None,
                        offset: Optional[int]=None):
        """
        Returns datasets matching the search parameters. Full-text search across all datasets. Results are ordered by relevance.
        
        Args:
            dataset_type (str): The primary type of the dataset. Available values : OCCURRENCE, CHECKLIST, METADATA, SAMPLING_EVENT, MATERIAL_ENTITY.
            subtype (str): The sub-type of the dataset. Available values : TAXONOMIC_AUTHORITY, NOMENCLATOR_AUTHORITY, INVENTORY_THEMATIC, INVENTORY_REGIONAL, GLOBAL_SPECIES_DATASET, DERIVED_FROM_OCCURRENCE, SPECIMEN, OBSERVATION.
            publishing_org (str): Filters datasets by their publishing organization UUID key.
            hosting_org (str): Filters datasets by their hosting organization UUID key.
            keyword (str): Filters datasets by a case insensitive plain text keyword. The search is done on the merged collection of tags, the dataset keywordCollections and temporalCoverages.
            decade (int): Filters datasets by their temporal coverage broken down to decades. Decades are given as a full year, e.g. 1880, 1960, 2000, etc, and will return datasets wholly contained in the decade as well as those that cover the entire decade or more. Facet by decade to get the break down, i.e. facet=DECADE&limit=0.
            publishing_country (str): Filters datasets by their owning organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            hosting_countrg (str): Filters datasets by their hosting organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            license (str): The dataset's licence. Available values : CC0_1_0, CC_BY_4_0, CC_BY_NC_4_0, UNSPECIFIED, UNSUPPORTED.
            project_id (str): Filter or facet based on the project ID of a given dataset. A dataset can have a project id if it is the result of a project. multiple datasets can have the same project id. Example : AA003-AA003311F.
            taxon_key (int): A taxon key from the GBIF backbone.
            record_count (int): Number of records of the dataset. Accepts ranges and a '*' can be used as a wildcard. Example : 100,*.
            modified_date (str): Date when the dataset was modified the last time. Accepts ranges and a '*' can be used as a wildcard. Example : 2022-05-01,*.
            doi (str): A DOI identifier.
            network_key (str): Network associated to a dataset.
            endorsing_node_key (str): Node key that endorsed this dataset's publisher.
            installation_key (str): Key (uuid) of the installation that hosts the dataset. 
            endpoint_type (str): Type of the endpoint of the dataset. Available values : EML, FEED, WFS, WMS, TCS_RDF, TCS_XML, DWC_ARCHIVE, DIGIR, DIGIR_MANIS, TAPIR, BIOCASE, BIOCASE_XML_ARCHIVE, OAI_PMH, COLDP, CAMTRAP_DP, OTHER. 
            query (str): Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            highlight (bool): Set highlight=True to highlight terms matching the query when in fulltext search fields. The highlight will be an emphasis tag of class gbifHl. 
            facet (list): A facet name used to retrieve the most frequent values for a field. This parameter may be repeated to request multiple facets.
            facet_min_count (int): Used in combination with the facet parameter. Set facet_min_count={#} to exclude facets with a count less than {#}.
            facet_multiselect (bool): Used in combination with the facet parameter. Set facet_multiselect=True to still return counts for values that are not currently filtered.
            facet_limt (int): Facet parameters allow paging requests using the parameters facet_offset and facet_limit.
            facet_offset (int): Facet parameters allow paging requests using the parameters facet_offset and facet_limit.
            limit (int): Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing the datasets matching search criteria.
        """
        params: Dict[str, Any] = {}
        params_list = [("type", dataset_type),
                ("subtype", subtype),
                ("publishingOrg", publishing_org),
                ("hostingOrg", hosting_org),
                ("keyword", keyword),
                ("decade", decade),
                ("publishingCountry", publishing_country),
                ("hostingCountry", hosting_country),
                ("license", license),
                ("projectId", project_id),
                ("taxonKey", taxon_key),
                ("recordCount", record_count),
                ("modifiedDate", modified_date),
                ("doi", doi),
                ("networkKey", network_key),
                ("endorsingNodeKey", endorsing_node_key),
                ("installationKey", installation_key),
                ("endpointType", endpoint_type),
                ("q", query),
                ("hl", highlight),
                ("facet", facet),
                ("facetMincount", facet_min_count),
                ("facetMultiselect", facet_multiselect),
                ("facetLimit", facet_limit),
                ("facetOffset", facet_offset),
                ("limit", limit),
                ("offset", offset)]
        
        hc.add_params(params, params_list)
        resource = "/search"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def export_dataset_search(self, data_format="TSV",
                        dataset_type: Optional[str]=None,
                        subtype: Optional[str]=None,
                        publishing_org: Optional[str]=None,
                        hosting_org: Optional[str]=None,
                        keyword: Optional[str]=None,
                        decade: Optional[int]=None,
                        publishing_country: Optional[str]=None,
                        hosting_country: Optional[str]=None,
                        license: Optional[str]=None,
                        project_id: Optional[str]=None,
                        taxon_key: Optional[int]=None,
                        record_count: Optional[str]=None,
                        modified_date: Optional[str]=None,
                        doi: Optional[str]=None,
                        network_key: Optional[str]=None,
                        endorsing_node_key: Optional[str]=None,
                        installation_key: Optional[str]=None,
                        endpoint_type: Optional[str]=None,
                        query: Optional[str]=None):
        """
        Returns contents of datasets matching the search parameters, in TSV or CSV format. Full-text search across all datasets. Results are ordered by relevance.
        
        Args:
            data_format (str): Format of the exported file. Default is TSV and other supported value is CSV.
            dataset_type (str): The primary type of the dataset. Available values : OCCURRENCE, CHECKLIST, METADATA, SAMPLING_EVENT, MATERIAL_ENTITY.
            subtype (str): The sub-type of the dataset. Available values : TAXONOMIC_AUTHORITY, NOMENCLATOR_AUTHORITY, INVENTORY_THEMATIC, INVENTORY_REGIONAL, GLOBAL_SPECIES_DATASET, DERIVED_FROM_OCCURRENCE, SPECIMEN, OBSERVATION.
            publishing_org (str): Filters datasets by their publishing organization UUID key.
            hosting_org (str): Filters datasets by their hosting organization UUID key.
            keyword (str): Filters datasets by a case insensitive plain text keyword. The search is done on the merged collection of tags, the dataset keywordCollections and temporalCoverages.
            decade (int): Filters datasets by their temporal coverage broken down to decades. Decades are given as a full year, e.g. 1880, 1960, 2000, etc, and will return datasets wholly contained in the decade as well as those that cover the entire decade or more. Facet by decade to get the break down, i.e. facet=DECADE&limit=0.
            publishing_country (str): Filters datasets by their owning organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            hosting_countrg (str): Filters datasets by their hosting organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            license (str): The dataset's licence. Available values : CC0_1_0, CC_BY_4_0, CC_BY_NC_4_0, UNSPECIFIED, UNSUPPORTED.
            project_id (str): Filter or facet based on the project ID of a given dataset. A dataset can have a project id if it is the result of a project. multiple datasets can have the same project id. Example : AA003-AA003311F.
            taxon_key (int): A taxon key from the GBIF backbone.
            record_count (int): Number of records of the dataset. Accepts ranges and a '*' can be used as a wildcard. Example : 100,*.
            modified_date (str): Date when the dataset was modified the last time. Accepts ranges and a '*' can be used as a wildcard. Example : 2022-05-01,*.
            doi (str): A DOI identifier.
            network_key (str): Network associated to a dataset.
            endorsing_node_key (str): Node key that endorsed this dataset's publisher.
            installation_key (str): Key (uuid) of the installation that hosts the dataset. 
            endpoint_type (str): Type of the endpoint of the dataset. Available values : EML, FEED, WFS, WMS, TCS_RDF, TCS_XML, DWC_ARCHIVE, DIGIR, DIGIR_MANIS, TAPIR, BIOCASE, BIOCASE_XML_ARCHIVE, OAI_PMH, COLDP, CAMTRAP_DP, OTHER. 
            query (str): Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            
        Returns:
            string: A TSV or CSV format text content containing the datasets matching search criteria.
        """
        params: Dict[str, Any] = {}
        params["format"] = data_format
        params_list = [
                ("type", dataset_type),
                ("subtype", subtype),
                ("publishingOrg", publishing_org),
                ("hostingOrg", hosting_org),
                ("keyword", keyword),
                ("decade", decade),
                ("publishingCountry", publishing_country),
                ("hostingCountry", hosting_country),
                ("license", license),
                ("projectId", project_id),
                ("taxonKey", taxon_key),
                ("recordCount", record_count),
                ("modifiedDate", modified_date),
                ("doi", doi),
                ("networkKey", network_key),
                ("endorsingNodeKey", endorsing_node_key),
                ("installationKey", installation_key),
                ("endpointType", endpoint_type),
                ("q", query)] 
        
        hc.add_params(params, params_list)           
        resource = "/search/export"
        return hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params).decode("utf-8")
    
    def suggest_datasets(self, dataset_type: Optional[str]=None,
                        subtype: Optional[str]=None,
                        publishing_org: Optional[str]=None,
                        hosting_org: Optional[str]=None,
                        keyword: Optional[str]=None,
                        decade: Optional[int]=None,
                        publishing_country: Optional[str]=None,
                        hosting_country: Optional[str]=None,
                        license: Optional[str]=None,
                        project_id: Optional[str]=None,
                        taxon_key: Optional[int]=None,
                        record_count: Optional[str]=None,
                        modified_date: Optional[str]=None,
                        doi: Optional[str]=None,
                        network_key: Optional[str]=None,
                        endorsing_node_key: Optional[str]=None,
                        installation_key: Optional[str]=None,
                        endpoint_type: Optional[str]=None,
                        query: Optional[str]=None):
        """
        Search that returns up to 20 matching datasets. Results are ordered by relevance. The response is smaller than a dataset search. 
        
        Args:
            dataset_type (str): The primary type of the dataset. Available values : OCCURRENCE, CHECKLIST, METADATA, SAMPLING_EVENT, MATERIAL_ENTITY.
            subtype (str): The sub-type of the dataset. Available values : TAXONOMIC_AUTHORITY, NOMENCLATOR_AUTHORITY, INVENTORY_THEMATIC, INVENTORY_REGIONAL, GLOBAL_SPECIES_DATASET, DERIVED_FROM_OCCURRENCE, SPECIMEN, OBSERVATION.
            publishing_org (str): Filters datasets by their publishing organization UUID key.
            hosting_org (str): Filters datasets by their hosting organization UUID key.
            keyword (str): Filters datasets by a case insensitive plain text keyword. The search is done on the merged collection of tags, the dataset keywordCollections and temporalCoverages.
            decade (int): Filters datasets by their temporal coverage broken down to decades. Decades are given as a full year, e.g. 1880, 1960, 2000, etc, and will return datasets wholly contained in the decade as well as those that cover the entire decade or more. Facet by decade to get the break down, i.e. facet=DECADE&limit=0.
            publishing_country (str): Filters datasets by their owning organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            hosting_countrg (str): Filters datasets by their hosting organization's country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            license (str): The dataset's licence. Available values : CC0_1_0, CC_BY_4_0, CC_BY_NC_4_0, UNSPECIFIED, UNSUPPORTED.
            project_id (str): Filter or facet based on the project ID of a given dataset. A dataset can have a project id if it is the result of a project. multiple datasets can have the same project id. Example : AA003-AA003311F.
            taxon_key (int): A taxon key from the GBIF backbone.
            record_count (int): Number of records of the dataset. Accepts ranges and a '*' can be used as a wildcard. Example : 100,*.
            modified_date (str): Date when the dataset was modified the last time. Accepts ranges and a '*' can be used as a wildcard. Example : 2022-05-01,*.
            doi (str): A DOI identifier.
            network_key (str): Network associated to a dataset.
            endorsing_node_key (str): Node key that endorsed this dataset's publisher.
            installation_key (str): Key (uuid) of the installation that hosts the dataset. 
            endpoint_type (str): Type of the endpoint of the dataset. Available values : EML, FEED, WFS, WMS, TCS_RDF, TCS_XML, DWC_ARCHIVE, DIGIR, DIGIR_MANIS, TAPIR, BIOCASE, BIOCASE_XML_ARCHIVE, OAI_PMH, COLDP, CAMTRAP_DP, OTHER. 
            query (str): Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            
            Returns:
                dict: A dictionary containing dataset suggestions.
            """
        params: Dict[str, Any] = {}
        params_list = [
                ("type", dataset_type),
                ("subtype", subtype),
                ("publishingOrg", publishing_org),
                ("hostingOrg", hosting_org),
                ("keyword", keyword),
                ("decade", decade),
                ("publishingCountry", publishing_country),
                ("hostingCountry", hosting_country),
                ("license", license),
                ("projectId", project_id),
                ("taxonKey", taxon_key),
                ("recordCount", record_count),
                ("modifiedDate", modified_date),
                ("doi", doi),
                ("networkKey", network_key),
                ("endorsingNodeKey", endorsing_node_key),
                ("installationKey", installation_key),
                ("endpointType", endpoint_type),
                ("q", query)] 
        
        hc.add_params(params, params_list)           
        resource = "/suggest"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
                                                                                                                                  
    def get_dataset_by_doi(self, prefix, suffix,
                            limit: Optional[int]=None,
                            offset: Optional[int]=None):
        """
        Returns a dataset matching the given doi.
        
        Arg:
            prefix (str): Plain DOI prefix (before the slash). Example : 10.15468.
            suffix (str): Plain DOI suffix (after the slash). Example : igasai.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            dict: A dictionary containing a dataset.
        """
        params: Dict[str, Any] = {}
        params_list= [("limit", limit), ("offset", offset)]
        
        hc.add_params(params, params_list)
        resource = f"/doi/{prefix}/{suffix}"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def get_dataset_by_key(self, key):
        """
        Returns a dataset matching the given key.
        
        Arg:
            key (str): The key (uuid) of the entity (dataset, organization, network etc.).
          
        Returns:
            dict: A dictionary containing a dataset.
        """       
        resource = f"dataset/{key}"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
            
    def update_dataset(self):
        pass
       
              
                     

                                   
                                                                                                         