from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class Institutions:
    """
    A class for interacting with the institutions section of the Registry API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="institutions_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "grscicoll/institution"
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
      
    def list_all_institutions(self, institution_type: Optional[str]=None,
                             institutional_governance: Optional[str]=None,
                             disciplines: Optional[str]=None,
                             code: Optional[str]=None,
                             name: Optional[str]=None,
                             alternative_code: Optional[str]=None,
                             contact: Optional[str]=None,
                             machine_tag_namespace: Optional[str]=None,
                             machine_tag_name: Optional[str]=None,
                             machine_tag_value: Optional[str]=None,
                             identifier_type: Optional[str]=None,
                             identifier: Optional[str]=None,
                             country: Optional[str]=None,
                             gbif_region: Optional[str]=None,
                             city: Optional[str]=None,
                             fuzzy_name: Optional[str]=None,
                             active: Optional[bool]=None,
                             master_source_type: Optional[str]=None,
                             number_specimens: Optional[str]=None,
                             display_on_nhc_portal: Optional[bool]=None,
                             replaced_by: Optional[str]=None,
                             occurrence_count: Optional[str]=None,
                             type_specimen_count: Optional[str]=None,
                             institution_key: Optional[str]=None,
                             sort_by: Optional[str]=None,
                             sort_order: Optional[str]=None,
                             query: Optional[str]=None,
                             limit: Optional[int]=None,
                             offset: Optional[int]=None):
        """
        Returns full text form of current collections search results.
        
        Args:
            institution_type (str): Optional. Type of a GrSciColl institution. Available values : BIOMEDICAL_RESEARCH_INSTITUTE, BOTANICAL_GARDEN, HERBARIUM, LIVING_ORGANISM_COLLECTION, MEDICAL_RESEARCH_INSTITUTE, MUSEUM, MUSEUM_HERBARIUM_PRIVATE_NON_PROFIT, OTHER_INSTITUTIONAL_TYPE, OTHER_TYPE_RESEARCH_INSTITUTION_BIOREPOSITORY, UNIVERSITY_COLLEGE, ZOO_AQUARIUM.
            institutional_governance (str): Optional. Instutional governance of a GrSciColl institution. Available values : ACADEMIC_FEDERAL, ACADEMIC_FOR_PROFIT, ACADEMIC_LOCAL, ACADEMIC_NON_PROFIT, ACADEMIC_STATE, FEDERAL, FOR_PROFIT, LOCAL, NON_PROFIT, OTHER, STATE.
            disciplines (str): Optional. Discipline of a GrSciColl institution. Accepts multiple values, for example discipline=ARCHAEOLOGY_PREHISTORIC&discipline=ARCHAEOLOGY_HISTORIC. See this endpoint's docs for available values.
            code (str): Optional. Code of a GrSciColl institution or collection.
            name (str): Optional. Name of a GrSciColl institution or collection.
            alternative_code (str): Optional. Alternative code of a GrSciColl institution or collection.
            contact (str): Optional. Filters collections and institutions whose contacts contain the person key specified.
            machine_tag_namespace (str): Optional: Filters for entities with a machine tag in the specified namespace.
            machine_tag_name (str): Optional. Filters for entities with a machine tag with the specified name (use in combination with the machineTagNamespace parameter).
            machine_tag_value (str): Optional. Filters for entities with a machine tag with the specified value (use in combination with the machineTagNamespace and machineTagName parameters).
            identifier_type (str): Optional. An identifier type for the identifier parameter. Available values : URL, LSID, HANDLER, DOI, UUID, FTP, URI, UNKNOWN, GBIF_PORTAL, GBIF_NODE, GBIF_PARTICIPANT, GRSCICOLL_ID, GRSCICOLL_URI, IH_IRN, ROR, GRID, CITES, SYMBIOTA_UUID, WIKIDATA, NCBI_BIOCOLLECTION.
            identifier (str): Optional. An identifier of the type given by the identifierType parameter, for example a DOI or UUID.
            country (str): Optional. Filters by country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            gbif_region (str): Optional. Filters by a gbif region. Available values : AFRICA, ASIA, EUROPE, NORTH_AMERICA, OCEANIA, LATIN_AMERICA, ANTARCTICA.
            city (str): Optional. Filters by the city of the address. It searches in both the physical and the mailing address.
            fuzzy_name (str): Optional. It searches by name fuzzily so the parameter doesn't have to be the exact name.
            active (bool): Optional. Active status of a GrSciColl institution or collection.
            master_source_type (str): Optional. The master source type of a GRSciColl institution or collection. Available values : GRSCICOLL, GBIF_REGISTRY, IH.
            number_specimens (str): Optional. Number of specimens. It supports ranges and a '*' can be used as a wildcard.
            display_on_nhc_portal (bool): Optional. Flag to show this record in the NHC portal.
            replaced_by (str): Optional. Key of the entity that replaced another entity.
            occurrence_count (str): Optional. Count of occurrences linked. It supports ranges and a '*' can be used as a wildcard.
            type_specimen_count (str): Optional. Count of type specimens linked. It supports ranges and a '*' can be used as a wildcard.
            institution_key (str): Optional. Keys of institutions to filter by.
            sort_by (str): Optional. Field to sort the results by. It only supports the fields contained in the enum. Available values : NUMBER_SPECIMENS.
            sort_order (str): Optional. Sort order to use with the sortBy parameter. Available values : ASC, DESC.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns
            TSV or CSV: The full text results of collections search.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("type", institution_type),
                ("institutionalGovernance", institutional_governance),
                ("disciplines", disciplines),
                ("code", code),
                ("name", name),
                ("alternativeCode", alternative_code),
                ("contact", contact),
                ("machineTagNamespace", machine_tag_namespace),
                ("machineTagName", machine_tag_name),
                ("machineTagValue", machine_tag_value),
                ("identifierType", identifier_type),
                ("identifier", identifier),
                ("country", country),
                ("gbifRegion", gbif_region),
                ("city", city),
                ("fuzzyName", fuzzy_name),
                ("active", active),
                ("masterSourceType", master_source_type),
                ("numberSpecimens", number_specimens),
                ("displayOnNHCPortal", display_on_nhc_portal),
                ("replacedBy", replaced_by),
                ("occurrenceCount", occurrence_count),
                ("typeSpecimenCount", type_specimen_count),
                ("institutionKey", institution_key),
                ("sortBy", sort_by),
                ("sortOrder", sort_order),
                ("q", query),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)
        
    def export_institutions(self, data_format="TSV", institution_type: Optional[str]=None,
                             institutional_governance: Optional[str]=None,
                             disciplines: Optional[str]=None,
                             code: Optional[str]=None,
                             name: Optional[str]=None,
                             alternative_code: Optional[str]=None,
                             contact: Optional[str]=None,
                             machine_tag_namespace: Optional[str]=None,
                             machine_tag_name: Optional[str]=None,
                             machine_tag_value: Optional[str]=None,
                             identifier_type: Optional[str]=None,
                             identifier: Optional[str]=None,
                             country: Optional[str]=None,
                             gbif_region: Optional[str]=None,
                             city: Optional[str]=None,
                             fuzzy_name: Optional[str]=None,
                             active: Optional[bool]=None,
                             master_source_type: Optional[str]=None,
                             number_specimens: Optional[str]=None,
                             display_on_nhc_portal: Optional[bool]=None,
                             replaced_by: Optional[str]=None,
                             occurrence_count: Optional[str]=None,
                             type_specimen_count: Optional[str]=None,
                             institution_key: Optional[str]=None,
                             sort_by: Optional[str]=None,
                             sort_order: Optional[str]=None,
                             query: Optional[str]=None,
                             limit: Optional[int]=None,
                             offset: Optional[int]=None):
        """
        Returns full text results of institutions search.
        
        Args:
            data_format (str): Available values: TSV and CSV. Default is TSV.
            institution_type (str): Optional. Type of a GrSciColl institution. Available values : BIOMEDICAL_RESEARCH_INSTITUTE, BOTANICAL_GARDEN, HERBARIUM, LIVING_ORGANISM_COLLECTION, MEDICAL_RESEARCH_INSTITUTE, MUSEUM, MUSEUM_HERBARIUM_PRIVATE_NON_PROFIT, OTHER_INSTITUTIONAL_TYPE, OTHER_TYPE_RESEARCH_INSTITUTION_BIOREPOSITORY, UNIVERSITY_COLLEGE, ZOO_AQUARIUM.
            institutional_governance (str): Optional. Instutional governance of a GrSciColl institution. Available values : ACADEMIC_FEDERAL, ACADEMIC_FOR_PROFIT, ACADEMIC_LOCAL, ACADEMIC_NON_PROFIT, ACADEMIC_STATE, FEDERAL, FOR_PROFIT, LOCAL, NON_PROFIT, OTHER, STATE.
            disciplines (str): Optional. Discipline of a GrSciColl institution. Accepts multiple values, for example discipline=ARCHAEOLOGY_PREHISTORIC&discipline=ARCHAEOLOGY_HISTORIC. See this endpoint's docs for available values.
            code (str): Optional. Code of a GrSciColl institution or collection.
            name (str): Optional. Name of a GrSciColl institution or collection.
            alternative_code (str): Optional. Alternative code of a GrSciColl institution or collection.
            contact (str): Optional. Filters collections and institutions whose contacts contain the person key specified.
            machine_tag_namespace (str): Optional: Filters for entities with a machine tag in the specified namespace.
            machine_tag_name (str): Optional. Filters for entities with a machine tag with the specified name (use in combination with the machineTagNamespace parameter).
            machine_tag_value (str): Optional. Filters for entities with a machine tag with the specified value (use in combination with the machineTagNamespace and machineTagName parameters).
            identifier_type (str): Optional. An identifier type for the identifier parameter. Available values : URL, LSID, HANDLER, DOI, UUID, FTP, URI, UNKNOWN, GBIF_PORTAL, GBIF_NODE, GBIF_PARTICIPANT, GRSCICOLL_ID, GRSCICOLL_URI, IH_IRN, ROR, GRID, CITES, SYMBIOTA_UUID, WIKIDATA, NCBI_BIOCOLLECTION.
            identifier (str): Optional. An identifier of the type given by the identifierType parameter, for example a DOI or UUID.
            country (str): Optional. Filters by country given as a ISO 639-1 (2 letter) country code. See this endpoint's docs for available values.
            gbif_region (str): Optional. Filters by a gbif region. Available values : AFRICA, ASIA, EUROPE, NORTH_AMERICA, OCEANIA, LATIN_AMERICA, ANTARCTICA.
            city (str): Optional. Filters by the city of the address. It searches in both the physical and the mailing address.
            fuzzy_name (str): Optional. It searches by name fuzzily so the parameter doesn't have to be the exact name.
            active (bool): Optional. Active status of a GrSciColl institution or collection.
            master_source_type (str): Optional. The master source type of a GRSciColl institution or collection. Available values : GRSCICOLL, GBIF_REGISTRY, IH.
            number_specimens (str): Optional. Number of specimens. It supports ranges and a '*' can be used as a wildcard.
            display_on_nhc_portal (bool): Optional. Flag to show this record in the NHC portal.
            replaced_by (str): Optional. Key of the entity that replaced another entity.
            occurrence_count (str): Optional. Count of occurrences linked. It supports ranges and a '*' can be used as a wildcard.
            type_specimen_count (str): Optional. Count of type specimens linked. It supports ranges and a '*' can be used as a wildcard.
            institution_key (str): Optional. Keys of institutions to filter by.
            sort_by (str): Optional. Field to sort the results by. It only supports the fields contained in the enum. Available values : NUMBER_SPECIMENS.
            sort_order (str): Optional. Sort order to use with the sortBy parameter. Available values : ASC, DESC.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
        
        Returns:
            TSV or CSV: The full text results of the institutions search.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("format", data_format),
                ("type", institution_type),
                ("institutionalGovernance", institutional_governance),
                ("disciplines", disciplines),
                ("code", code),
                ("name", name),
                ("alternativeCode", alternative_code),
                ("contact", contact),
                ("machineTagNamespace", machine_tag_namespace),
                ("machineTagName", machine_tag_name),
                ("machineTagValue", machine_tag_value),
                ("identifierType", identifier_type),
                ("identifier", identifier),
                ("country", country),
                ("gbifRegion", gbif_region),
                ("city", city),
                ("fuzzyName", fuzzy_name),
                ("active", active),
                ("masterSourceType", master_source_type),
                ("numberSpecimens", number_specimens),
                ("displayOnNHCPortal", display_on_nhc_portal),
                ("replacedBy", replaced_by),
                ("occurrenceCount", occurrence_count),
                ("typeSpecimenCount", type_specimen_count),
                ("institutionKey", institution_key),
                ("sortBy", sort_by),
                ("sortOrder", sort_order),
                ("q", query),
                ("limit", limit),
                ("offset", offset)]
        hc.add_params(params, params_list)
        resource = "/export"
        response = hc.get_for_content_with_params(base_url+self.endpoint+resource, params=params)
        return response.decode("utf-8")
        
    def get_institution_by_key(self, key):
        """
        Returns details of a single institution matching the given key.
        
        Args:
            key (str): The key of the entity (dataset, organization, network etc.).
        
        Returns:
            dict: Returns details of a single institution.
        """
        resource = f"/{key}"
        try:
            return hc.get(base_url+self.endpoint+resource)
        except JSONDecodeError:
            response = hc.get_for_content(base_url+self.endpoint+resource)
            decoded_response = response.decode("utf-8")
            return {"Error": f"{decoded_response}"}
                     