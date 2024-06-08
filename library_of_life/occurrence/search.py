from typing import Optional, Dict, Any

import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class OccurrenceSearch:
    """
    A class for interacting with the search section of the Occurrence API.
    
    Attributes:
        endpoint: endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="search_occurrence_cache", 
                backend="sqlite", 
                expire_after=3600,
                auth_type="basic",
                client_id=None,
                client_secret=None,
                token_url=None):
        self.endpoint = "occurrence/search"
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
                    
    def search_occurrences(self, accepted_taxon_key: Optional[list[int]]=None,
                           associated_sequences: Optional[list[str]]=None,
                           basis_of_record: Optional[list[str]]=None,
                           bed: Optional[list[str]]=None,
                           catalog_number: Optional[list[str]]=None,
                           class_key: Optional[list[int]]=None,
                           collection_code: Optional[list[str]]=None,
                           collection_key: Optional[list[str]]=None,
                           continent: Optional[list[str]]=None,
                           coordinate_uncertainty_in_meters: Optional[tuple]=None,
                           country: Optional[list[str]]=None,
                           crawl_id: Optional[list[int]]=None,
                           dataset_id: Optional[list[str]]=None,
                           dataset_key: Optional[list[str]]=None,
                           dataset_name: Optional[list[str]]=None,
                           decimal_latitide: Optional[tuple]=None,
                           degree_of_establishment: Optional[list[str]]=None,
                           decimal_longitude: Optional[tuple]=None,
                           depth: Optional[tuple]=None,
                           distance_from_centroid_in_meters: Optional[tuple]=None,
                           dwca_extension: Optional[list[str]]=None,
                           earliest_eon_or_lowest_eonothem: Optional[list[str]]=None,
                           earliest_era_or_lowest_erathem: Optional[list[str]]=None,
                           earliest_period_or_lowest_system: Optional[list[str]]=None,
                           earliest_epoch_or_lowest_series: Optional[list[str]]=None,
                           earliest_age_or_lowest_stage: Optional[list[str]]=None,
                           elevation: Optional[tuple]=None,
                           end_day_of_year: Optional[list[int]]=None,
                           establishment_means: Optional[list[str]]=None,
                           event_date: Optional[list[str]]=None,
                           event_id: Optional[list[str]]=None,
                           family_key: Optional[list[str]]=None,
                           field_number: Optional[list[str]]=None,
                           formation: Optional[list[str]]=None,
                           gadm_gid: Optional[list[str]]=None,
                           gadm_level_0_gid: Optional[list[str]]=None,
                           gadm_level_1_gid: Optional[list[str]]=None,
                           gadm_level_2_gid: Optional[list[str]]=None,
                           gadm_level_3_gid: Optional[list[str]]=None,
                           gbif_id: Optional[int]=None,
                           gbif_region: Optional[list[str]]=None,
                           genus_key: Optional[list[int]]=None,
                           geo_distance: Optional[str]=None,
                           georeferenced_by: Optional[list[str]]=None,
                           geometry: Optional[list[str]]=None,
                           group: Optional[list[str]]=None,
                           has_coordinate: Optional[bool]=None,
                           higher_geography: Optional[list[str]]=None,
                           highest_biostratigraphic_zone: Optional[list[str]]=None,
                           has_geospatial_issue: Optional[bool]=None,
                           hosting_organization_key: Optional[list[str]]=None,
                           identified_by: Optional[list[str]]=None,
                           identified_by_id: Optional[list[str]]=None,
                           installation_key: Optional[list[str]]=None,
                           institution_code: Optional[list[str]]=None,
                           institution_key: Optional[list[str]]=None,
                           issue: Optional[list[str]]=None,
                           is_in_cluster: Optional[bool]=None,
                           island: Optional[list[str]]=None,
                           island_group: Optional[list[str]]=None,
                           is_sequenced: Optional[bool]=None,
                           iucn_red_list_category: Optional[list[str]]=None,
                           kingdom_key: Optional[list[int]]=None,
                           last_interpreted: Optional[list[str]]=None,
                           latest_eon_or_highest_eonothem: Optional[list[str]]=None,
                           latest_era_or_highest_erathem: Optional[list[str]]=None,
                           latest_period_or_highest_system: Optional[list[str]]=None,
                           latest_epoch_or_highest_series: Optional[list[str]]=None,
                           latest_age_or_highest_stage: Optional[list[str]]=None,
                           license: Optional[list[str]]=None,
                           life_stage: Optional[list[str]]=None,
                           locality: Optional[list[str]]=None,
                           lowest_biostratigraphic_zone: Optional[list[str]]=None,
                           media_type: Optional[list[tuple]]=None,
                           member: Optional[list[str]]=None,
                           modified: Optional[list[str]]=None,
                           month: Optional[list[int]]=None,
                           network_key: Optional[list[str]]=None,
                           occurrence_id: Optional[list[str]]=None,
                           occurrence_status: Optional[str]=None,
                           order_key: Optional[list[int]]=None,
                           organism_id: Optional[list[str]]=None,
                           organism_quantity: Optional[list[str]]=None,
                           organism_quantity_type: Optional[list[str]]=None,
                           other_catalog_numbers: Optional[list[str]]=None,
                           parent_event_id: Optional[list[str]]=None,
                           pathway: Optional[list[str]]=None,
                           phylum_key: Optional[list[int]]=None,
                           preparations: Optional[list[str]]=None,
                           previous_identifications: Optional[list[str]]=None,
                           programme: Optional[list[str]]=None,
                           project_id: Optional[list[str]]=None,
                           protocol: Optional[list[str]]=None,
                           published_by_gbif_region: Optional[list[str]]=None,
                           publising_org: Optional[list[str]]=None,
                           recorded_by: Optional[list[str]]=None,
                           recorded_by_id: Optional[list[str]]=None,
                           record_number: Optional[list[str]]=None,
                           relative_organism_quantity: Optional[list[str]]=None,
                           repatriated: Optional[bool]=None,
                           sample_size_unit: Optional[list[str]]=None,
                           sample_size_value: Optional[list[int]]=None,
                           sampling_protocol: Optional[list[str]]=None,
                           sex: Optional[list[str]]=None,
                           scientific_name: Optional[list[str]]=None,
                           species_key: Optional[list[int]]=None,
                           start_day_of_year: Optional[list[int]]=None,
                           state_province: Optional[list[str]]=None,
                           taxon_concept_id: Optional[list[str]]=None,
                           taxon_key: Optional[list[int]]=None,
                           taxon_id: Optional[list[str]]=None,
                           taxonomic_status: Optional[list[str]]=None,
                           type_status: Optional[list[str]]=None,
                           verbatim_scientific_name: Optional[list[str]]=None,
                           water_body: Optional[list[str]]=None,
                           year: Optional[list[int]]=None,
                           highlight: Optional[bool]=None,
                           query: Optional[str]=None,
                           limit: Optional[int]=None,
                           offset: Optional[int]=None,
                           facet: Optional[str]=None,
                           facet_mincount: Optional[int]=None,
                           facet_multiselect: Optional[bool]=None,
                           facet_limit: Optional[int]=None,
                           facet_offset: Optional[int]=None,
                           publishing_country: Optional[list[str]]=None
                           ):
        """
        Returns results of full search across all occurrences.
        
        Args:
            accepted_taxon_key (list[int]): Optional. A taxon key from the GBIF backbone. Only synonym taxa are included in the search, so a search for Aves with acceptedTaxonKey=212 (i.e. /occurrence/search?taxonKey=212) will match occurrences identified as birds, but not any known family, genus or species of bird.Example : 2476674 
            associated_sequences (list[str]): Optional. Identifier (publication, global unique identifier, URI) of genetic sequence information associated with the material entity. Example : http://www.ncbi.nlm.nih.gov/nuccore/U34853.1
            basis_of_record (list[str]): Optional. Basis of record, as defined in our BasisOfRecord vocabulary. Available values : PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN, OBSERVATION, HUMAN_OBSERVATION, MACHINE_OBSERVATION, MATERIAL_SAMPLE, LITERATURE, MATERIAL_CITATION, OCCURRENCE, UNKNOWN. Example : PRESERVED_SPECIMEN
            bed (list[str]): Optional. The full name of the lithostratigraphic bed from which the material entity was collected. Example : Harlem coal
            catalog_number (list[str]): Optional. An identifier of any form assigned by the source within a physical collection or digital dataset for the record which may not be unique, but should be fairly unique in combination with the institution and collection code. Example : K001275042
            class_key (list[int]): Optional. Class classification key. Parameter may be repeated. Example : 212
            collection_code (list[str]): Optional. An identifier of any form assigned by the source to identify the physical collection or digital dataset uniquely within the context of an institution. Example : F  
            collection_key (list[str]): Optional. A key (UUID) for a collection registered in the Global Registry of Scientific Collections. Example : dceb8d52-094c-4c2c-8960-75e0097c6861
            continent (list[str]): Optional. Continent, as defined in our Continent vocabulary. Available values : AFRICA, ANTARCTICA, ASIA, OCEANIA, EUROPE, NORTH_AMERICA, SOUTH_AMERICA. Example : EUROPE 
            coordinate_uncertainty_in_meters (tuple): Optional. The horizontal distance (in metres) from the given decimalLatitude and decimalLongitude describing the smallest circle containing the whole of the Location. Supports range queries. Example : 0,500
            country (list[str]): Optional. The 2-letter country code (as per ISO-3166-1) of the country in which the occurrence was recorded. See this endpoint's docs for available values.
            crawl_id (list[int]): Optional. Crawl attempt that harvested this record. Example : 1
            dataset_id (list[str]): Optional. The ID of the dataset. Example : https://doi.org/10.1594/PANGAEA.315492
            dataset_key (list[str]): Optional. The occurrence dataset key (a UUID). Example : 13b70480-bd69-11dd-b15f-b8a03c50a862
            dataset_name (list[str]): Optional. The exact name of the dataset.
            decimal_latitude (tuple): Optional. Latitude in decimal degrees between -90° and 90° based on WGS 84. Supports range queries. Example : 40.5,45
            degree_of_establishment (list[str]): Optional. The degree to which an organism survives, reproduces and expands its range at the given place and time, as defined in the GBIF DegreeOfEstablishment vocabulary. Example : Invasive
            decimal_longitude (tuple): Optional. Longitude in decimals between -180 and 180 based on WGS 84. Supports range queries. Example : -120,-95.5
            depth (tuple): Optional. Depth in metres relative to altitude. For example 10 metres below a lake surface with given altitude. Example : 10,20
            distance_from_centroid_in_meters (tuple): Optional. The horizontal distance (in metres) of the occurrence from the nearest centroid known to be used in automated georeferencing procedures, if that distance is 5000m or less. Occurrences (especially specimens) near a country centroid may have a poor-quality georeference, especially if coordinateUncertaintyInMeters is blank or large. Supports range queries. Example : 0,500
            dwca_extension (list[str]): Optional. A known Darwin Core Archive extension RowType. Limits the search to occurrences which have this extension, although they will not necessarily have any useful data recorded using the extension. Example : http://rs.tdwg.org/ac/terms/Multimedia
            earliest_eon_or_lowest_eonothem (list[str]): Optional. The full name of the earliest possible geochronologic era or lowest chronostratigraphic erathem attributable to the stratigraphic horizon from which the material entity was collected. Example : Mesozoic
            earliest_era_or_lowest_erathem (list[str]): Optional. The full name of the latest possible geochronologic eon or highest chrono-stratigraphic eonothem or the informal name ("Precambrian") attributable to the stratigraphic horizon from which the material entity was collected. Example : Proterozoic
            earliest_period_or_lowest_system (list[str]): Optional. The full name of the earliest possible geochronologic period or lowest chronostratigraphic system attributable to the stratigraphic horizon from which the material entity was collected. Example : Neogene
            earliest_epoch_or_lowest_series (list[str]): Optional. The full name of the earliest possible geochronologic epoch or lowest chronostratigraphic series attributable to the stratigraphic horizon from which the material entity was collected. Example : Holocene 
            earliest_age_or_lowest_stage (list[str]): Optional. The full name of the earliest possible geochronologic age or lowest chronostratigraphic stage attributable to the stratigraphic horizon from which the material entity was collected. Example : Skullrockian 
            elevation (tuple): Optional. Elevation (altitude) in metres above sea level. Example : 1000,1250 
            end_day_of_year (list[int]): Optional. The latest integer day of the year on which the event occurred. Parameter may be repeated. Example : 6
            establishment_means (list[int]): Optional. Whether an organism or organisms have been introduced to a given place and time through the direct or indirect activity of modern humans, as defined in the GBIF EstablishmentMeans vocabulary. Example : Native
            event_date (list[str]): Optional. Occurrence date in ISO 8601 format: yyyy, yyyy-MM or yyyy-MM-dd. Example : 2000,2001-06-30   
            event_id (list[str]): Optional. An identifier for the information associated with a sampling event. Example : A 123   
            family_key (list[int]): Optional. Family classification key. Example : 2405    
            field_number (list[str]): Optional. An identifier given to the event in the field. Often serves as a link between field notes and the event. Example : RV Sol 87-03-08    
            formation (list[str]): Optional. The full name of the lithostratigraphic formation from which the material entity was collected. Example : Notch Peak Formation 
            gadm_gid (list[str]): Optional. A GADM geographic identifier at any level, for example AGO, AGO.1_1, AGO.1.1_1 or AGO.1.1.1_1. Example : AGO.1_1
            gadm_level_0_gid (list[str]): Optional. A GADM geographic identifier at the zero level, for example AGO. Example : AGO
            gadm_level_1_gid (list[str]): Optional. A GADM geographic identifier at the first level, for example AGO.1_1. Example : AGO.1_1     
            gadm_level_2_gid (list[str]): Optional. A GADM geographic identifier at the second level, for example AFG.1.1_1. Example : AFG.1.1_1  
            gadm_level_3_gid (list[str]): Optional. A GADM geographic identifier at the third level, for example AFG.1.1.1_1. Example : AFG.1.1.1_1       
            gbif_id (int): Optional. The unique GBIF key for a single occurrence. Example : 2005380410             
            gbif_region (list[str]): Optional. Gbif region based on country code. Available values : AFRICA, ASIA, EUROPE, NORTH_AMERICA, OCEANIA, LATIN_AMERICA, ANTARCTICA. Example : AFRICA                 
            genus_key (list[int]): Optional. Genus classification key. Example : 2877951                           
            geo_distance (str): Optional. Filters to match occurrence records with coordinate values within a specified distance of a coordinate. Distance may be specified in kilometres (km) or metres (m). Example : 90,100,5km        
            georeferenced_by (list[str]): Optional. Name of a person, group, or organization who determined the georeference (spatial representation) for the location. Example : Brad Millen         
            geometry (list[str]): Optional. Searches for occurrences inside a polygon described in Well Known Text (WKT) format. Only POLYGON and MULTIPOLYGON are accepted WKT types. For example, a shape written as POLYGON ((30.1 10.1, 40 40, 20 40, 10 20, 30.1 10.1)) would be queried as is. Polygons must have anticlockwise ordering of points. (A clockwise polygon represents the opposite area: the Earth's surface with a 'hole' in it. Such queries are not supported.). Example : POLYGON ((30.1 10.1, 40 40, 20 40, 10 20, 30.1 10.1))        
            group (list[str]): Optional. The full name of the lithostratigraphic group from which the material entity was collected. Example : Bathurst
            has_coordinate (bool): Optional. Limits searches to occurrence records which contain a value in both latitude and longitude (i.e. hasCoordinate=true limits to occurrence records with coordinate values and hasCoordinate=false limits to occurrence records without coordinate values). Example : True            
            higher_geography (list[str]): Optional. Geographic name less specific than the information captured in the locality term. Example : Argentina
            highest_biostratigraphic_zone (list[str]): Optional. The full name of the highest possible geological biostratigraphic zone of the stratigraphic horizon from which the material entity was collected. Example : Blancan                                
            has_geospatial_issue (bool): Optional. Includes/excludes occurrence records which contain spatial issues (as determined in our record interpretation), i.e. hasGeospatialIssue=true returns only those records with spatial issues while hasGeospatialIssue=false includes only records without spatial issues. The absence of this parameter returns any record with or without spatial issues. Example: True                                                               
            hosting_organization_key (list[str]): Optional. The key (UUID) of the publishing organization whose installation (server) hosts the original dataset. (This is of little interest to most data user). Example : fbca90e3-8aed-48b1-84e3-369afbd000ce                                                                                                   
            identified_by (list[str]): Optional. The person who provided the taxonomic identification of the occurrence. Example : Allison                                                                                                                                   
            identified_by_id (list[str]): Optional. Identifier (e.g. ORCID) for the person who provided the taxonomic identification of the occurrence. Example : https://orcid.org/0000-0001-6492-4016                                                                                                                                                                  
            installation_key (list[str]): Optional. The occurrence installation key (a UUID). (This is of little interest to most data users. It is the identifier for the server that provided the data to GBIF.) Example : 17a83780-3060-4851-9d6f-029d5fcb81c9                                                                                                                                                                                                      
            institution_code (list[str]): Optional. An identifier of any form assigned by the source to identify the institution the record belongs to. Not guaranteed to be unique. Example : K                                                                                                                                                                                                                                     
            institution_key (list[str]): Optional. A key (UUID) for an institution registered in the Global Registry of Scientific Collections. Example : fa252605-26f6-426c-9892-94d071c2c77f
            issue (list[str]): Optional. A specific interpretation issue as defined in our OccurrenceIssue enumeration. See this endpoint's docs for available values.
            is_in_cluster (bool): Optional. Experimental. Searches for records which are part of a cluster. See the documentation on clustering. Example : True                                                                                                                                                                                                                                                                 
            island (list[str]): Optional. The name of the island on or near which the location occurs. Example : Zanzibar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            island_group (list[str]): Optional. The name of the island group in which the location occurs. Example : Seychelles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            is_sequenced (bool): Optional. Flag occurrence when associated sequences exists. Example : true
            iucn_red_list_category (list[str]): Optional. A threat status category from the IUCN Red List. The two-letter code for the status should be used. Available values : EXTINCT, EXTINCT_IN_THE_WILD, REGIONALLY_EXTINCT, CRITICALLY_ENDANGERED, ENDANGERED, VULNERABLE, NEAR_THREATENED, LEAST_CONCERN, DATA_DEFICIENT, NOT_APPLICABLE, NOT_EVALUATED. Example : EX                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            kingdom_key (list[int]): Optional. Kingdom classification key. Parameter may be repeated. Example : 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            last_interpreted (list[str]): Optional. This date the record was last modified in GBIF, in ISO 8601 format: yyyy, yyyy-MM, yyyy-MM-dd, or MM-dd. Note that this is the date the record was last changed in GBIF, not necessarily the date the record was first/last changed by the publisher. Data is re-interpreted when we change the taxonomic backbone, geographic data sources, or interpretation processes. Parameter may be repeated or a range. Example : 2023-02 
            latest_eon_or_highest_eonothem (list[str]): Optional.The full name of the latest possible geochronologic eon or highest chrono-stratigraphic eonothem or the informal name ("Precambrian") attributable to the stratigraphic horizon from which the material entity was collected. Example : Proterozoic  
            latest_era_or_highest_erathem (list[str]): Optional. The full name of the latest possible geochronologic era or highest chronostratigraphic erathem attributable to the stratigraphic horizon from which the material entity was collected. Example : Cenozoic
            latest_period_or_highest_system (list[str]): Optional. The full name of the latest possible geochronologic period or highest chronostratigraphic system attributable to the stratigraphic horizon from which the material entity was collected. Example : Neogene
            latest_epoch_or_highest_series (list[str]): Optional. The full name of the latest possible geochronologic epoch or highest chronostratigraphic series attributable to the stratigraphic horizon from which the material entity was collected. Example : Pleistocene                                          
            latest_age_or_highest_stage (list[str]): Optional. The full name of the latest possible geochronologic age or highest chronostratigraphic stage attributable to the stratigraphic horizon from which the material entity was collected. Example : Boreal
            license (list[str]): Optional. The licence applied to the dataset or record by the publisher. Parameter may be repeated or a range. Available values : CC0_1_0, CC_BY_4_0, CC_BY_NC_4_0, UNSPECIFIED, UNSUPPORTED. Example : CC0_1_0 
            life_stage (list[str]): Optional. The age class or life stage of an organism at the time the occurrence was recorded, as defined in the GBIF LifeStage vocabulary](https://registry.gbif.org/vocabulary/LifeStage/concepts). Example : Juvenile
            locality (list[str]): Optional. The specific description of the place. Parameter may be repeated.
            lowest_biostratigraphic_zone (list[str]): Optional. The full name of the lowest possible geological biostratigraphic zone of the stratigraphic horizon from which the material entity was collected. Example : Maastrichtian      
            media_type (list[object]): Optional. The kind of multimedia associated with an occurrence as defined in our MediaType enumeration.
            member (list[str]): Optional. The full name of the lithostratigraphic member from which the material entity was collected. Example : Lava Dam Member        
            modified (list[str]): Optional. The most recent date-time on which the occurrnce was changed, according to the publisher. Example : 2023-02-20
            month (list[int]): Optional. The month of the year, starting with 1 for January. Example : 5 
            network_key (list[str]): Optional. The network's GBIF key (a UUID). Example : 2b7c7b4f-4d4f-40d3-94de-c28b6fa054a6
            occurrence_id (list[str]): Optional. A globally unique identifier for the occurrence record as provided by the publisher. Example : URN:catalog:UWBM:Bird:126493
            occurrence_status (list[str]): Optional. Either ABSENT or PRESENT; the presence or absence of the occurrence. Available values : PRESENT, ABSENT. Example : PRESENT
            order_key (list[int]): Optional. Order classification key. Example : 1448
            organism_id (list[str]): Optional. An identifier for the organism instance (as opposed to a particular digital record of the organism). May be a globally unique identifier or an identifier specific to the data set.
            organism_quantity (list[str]): Optional. A number or enumeration value for the quantity of organisms. Parameter may be repeated. Example : 1
            organism_quantity_type (list[str]): Optional. The type of quantification system used for the quantity of organisms. Note this term is not aligned to a vocabulary. Example : individuals
            other_catalog_numbers (list[str]): Optional. Previous or alternate fully qualified catalog numbers.        
            parent_event_id (list[str]): Optional. An identifier for the information associated with a sampling event. Example : A 123
            pathway (list[str]): Optional. The process by which an organism came to be in a given place at a given time, as defined in the GBIF Pathway vocabulary. Example : Agriculture
            phylum_key (list[int]): Optional. Phylum classification key. Example : 44
            preparations (list[str]): Optional. Preparation or preservation method for a specimen. Example : pinned
            previous_identifications (list[str]): Optional. Previous assignment of name to the organism. Example : Chalepidae
            programme (list[str]): Optional. A group of activities, often associated with a specific funding stream, such as the GBIF BID programme. Example : BID
            project_id (list[str]): Optional. The identifier for a project, which is often assigned by a funded programme. Example : bid-af2020-039-reg
            protocol (list[str]): Optional. Protocol or mechanism used to provide the occurrence record. Available values : EML, FEED, WFS, WMS, TCS_RDF, TCS_XML, DWC_ARCHIVE, DIGIR, DIGIR_MANIS, TAPIR, BIOCASE, BIOCASE_XML_ARCHIVE, OAI_PMH, COLDP, CAMTRAP_DP, OTHER. Example : DWC_ARCHIVE
            published_by_gbif_region (list[str]): Optional. GBIF region based on the owning organization's country. Available values : AFRICA, ASIA, EUROPE, NORTH_AMERICA, OCEANIA, LATIN_AMERICA, ANTARCTICA.Example : AFRICA
            publishing_org (list[str]): Optional. The publishing organization's GBIF key (a UUID). Example : e2e717bf-551a-4917-bdc9-4fa0f342c530
            recorded_by (list[str]): Optional. The person who recorded the occurrence. Example : MiljoStyrelsen
            recorded_by_id (list[str]): Optional. Identifier (e.g. ORCID) for the person who recorded the occurrence. Example : https://orcid.org/0000-0003-0623-6682
            record_number (list[int]): Optional. An identifier given to the record at the time it was recorded in the field. Example : 1
            relative_organism_quantity (list[str]): Optional. The relative measurement of the quantity of the organism (i.e. without absolute units).
            repatriated (bool): Optional. Searches for records whose publishing country is different to the country in which the record was recorded. Example : true
            sample_size_unit (list[str]):  Optional. The unit of measurement of the size (time duration, length, area, or volume) of a sample in a sampling event..Example : hectares    
            sample_size_value (list[float]): Optional. numeric value for a measurement of the size (time duration, length, area, or volume) of a sample in a sampling event. Example : 50.5
            sampling_protocol (list[str]): Optional. The name of, reference to, or description of the method or protocol used during a sampling event. Example : malaise trap
            sex (list[str]): Optional. The sex of the biological individual(s) represented in the occurrence. Available values : NONE, MALE, FEMALE, HERMAPHRODITE. Example : MALE
            scientific_name (list[str]): Optional. A scientific name from the GBIF backbone. All included and synonym taxa are included in the search. Under the hood a call to the species match service is done first to retrieve a taxonKey. Only unique scientific names will return results, homonyms (many monomials) return nothing! Consider to use the taxonKey parameter instead and the species match service directly. Example : Quercus robur
            species_key (list[int]): Optional. Species classification key. Example : 2476674
            start_day_of_year (list[int]): Optional. The earliest integer day of the year on which the event occurred. Example : 5
            state_province (list[str]): Optional. The name of the next smaller administrative region than country (state, province, canton, department, region, etc.) in which the Location occurs. This term does not have any data quality checks; see also the GADM parameters. Example : Leicestershire
            taxon_concept_id (list[str]): Optional. An identifier for the taxonomic concept to which the record refers - not for the nomenclatural details of a taxon. Example : 8fa58e08-08de-4ac1-b69c-1235340b7001 
            taxon_key (list[int]): Optional. A taxon key from the GBIF backbone. All included (child) and synonym taxa are included in the search, so a search for Aves with taxonKey=212 (i.e. /occurrence/search?taxonKey=212) will match all birds, no matter which species. Example : 2476674  
            taxon_id (list[str]): Optional. The taxon identifier provided to GBIF by the data publisher. Example : urn:lsid:dyntaxa.se:Taxon:103026
            taxonomic_status (list[str]): Optional. A taxonomic status from our TaxonomicStatus enumeration. Available values : ACCEPTED, DOUBTFUL, SYNONYM, HETEROTYPIC_SYNONYM, HOMOTYPIC_SYNONYM, PROPARTE_SYNONYM, MISAPPLIED. Example : SYNONYM
            type_status (list[str]): Optional. Nomenclatural type (type status, typified scientific name, publication) applied to the subject. See this endpoint's docs for available values.
            verbatim_scientific_name (list[str]): Optional. The scientific name provided to GBIF by the data publisher, before interpretation and processing by GBIF. Example : Quercus robur L.
            water_body (list[str]): Optional. The name of the water body in which the Locations occurs. Example : Lake Michigan
            year (list[int]): Optional. The 4 digit year. A year of 98 will be interpreted as AD 98. Example : 1998
            highlight (bool): Optional. Set highlight=True to highlight terms matching the query when in full-text search fields. The highlight will be an emphasis tag of class gbifH1 e.g. /search?q=plant&hl=true. Full-text search fields include: title, keyword, country, publishing country, publishing organization title, hosting organization title, and description. One additional full text field is searched which includes information from metadata documents, but the text of this field is not returned in the response. Example : true
            query (str): Optional. Simple full-text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the maximum threshold, which is 300 for this service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. This service has a maximum offset of 100,000.
            facet (str): Optional. A facet name used to retrieve the most frequent values for a field. Facets are allowed for all search parameters except geometry and geoDistance. Note terms not available for searching are not available for faceting.     
            facet_mincount (int): Optional. Used in combination with the facet parameter. Set facetMincount={#} to exclude facets with a count less than {#}, e.g. [/search?facet=basisOfRecord&limit=0&facetMincount=10000](https://api.gbif.org/v1/occurrence/search?facet=basisOfRecord&limit=0&facetMincount=1000000].
            facet_multiselect (bool): Optional. Used in combination with the facet parameter. Set facetMultiselect=true to still return counts for values that are not currently filtered, e.g. /search?facet=basisOfRecord&limit=0&basisOfRecord=HUMAN_OBSERVATION&facetMultiselect=true still shows Basis of Record values 'PRESERVED_SPECIMEN' and so on, even though Basis of Record is being filtered.
            facet_limit (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            facet_offset (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            publishing_country (list[str]): Optional. The 2-letter country code (as per ISO-3166-1) of the owning organization's country. See this endpoint's docs for available values.
        
        Returns:
            dict: A dictionary containing the data.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("acceptedTaxonKey", accepted_taxon_key),
            ("associatedSequences", associated_sequences),
            ("basisOfRecord", basis_of_record),
            ("bed", bed),
            ("catalogNumber", catalog_number),
            ("classKey", class_key),
            ("collectionCode", collection_code),
            ("collectionKey", collection_key),
            ("continent", continent),
            ("coordinateUncertaintyInMeters", coordinate_uncertainty_in_meters),
            ("country", country),
            ("crawlId", crawl_id),
            ("datasetId", dataset_id),
            ("datasetKey", dataset_key),
            ("datasetName", dataset_name),
            ("decimalLatitide", decimal_latitide),
            ("degreeOfEstablishment", degree_of_establishment),
            ("decimalLongitude", decimal_longitude),
            ("depth", depth),
            ("distanceFromCentroidInMeters", distance_from_centroid_in_meters),
            ("dwcaExtension", dwca_extension),
            ("earliestEonOrLowestEonothem", earliest_eon_or_lowest_eonothem),
            ("earliestEraOrLowestErathem", earliest_era_or_lowest_erathem),
            ("earliestPeriodOrLowestSystem", earliest_period_or_lowest_system),
            ("earliestEpochOrLowestSeries", earliest_epoch_or_lowest_series),
            ("earliestAgeOrLowestStage", earliest_age_or_lowest_stage),
            ("elevation", elevation),
            ("endDayOfYear", end_day_of_year),
            ("establishmentMeans", establishment_means),
            ("eventDate", event_date),
            ("eventId", event_id),
            ("familyKey", family_key),
            ("fieldNumber", field_number),
            ("formation", formation),
            ("gadmGid", gadm_gid),
            ("gadmLevel0Gid", gadm_level_0_gid),
            ("gadmLevel1Gid", gadm_level_1_gid),
            ("gadmLevel2Gid", gadm_level_2_gid),
            ("gadmLevel3Gid", gadm_level_3_gid),
            ("gbifId", gbif_id),
            ("gbifRegion", gbif_region),
            ("genusKey", genus_key),
            ("geoDistance", geo_distance),
            ("georeferencedBy", georeferenced_by),
            ("geometry", geometry),
            ("group", group),
            ("hasCoordinate", has_coordinate),
            ("higherGeography", higher_geography),
            ("highestBiostratigraphicZone", highest_biostratigraphic_zone),
            ("hasGeospatialIssue", has_geospatial_issue),
            ("hostingOrganizationKey", hosting_organization_key),
            ("identifiedBy", identified_by),
            ("identifiedById", identified_by_id),
            ("installationKey", installation_key),
            ("institutionCode", institution_code),
            ("institutionKey", institution_key),
            ("issue", issue),
            ("isInCluster", is_in_cluster),
            ("island", island),
            ("islandGroup", island_group),
            ("isSequenced", is_sequenced),
            ("iucnRedListCategory", iucn_red_list_category),
            ("kingdomKey", kingdom_key),
            ("lastInterpreted", last_interpreted),
            ("latestEonOrHighestEonothem", latest_eon_or_highest_eonothem),
            ("latestEraOrHighestErathem", latest_era_or_highest_erathem),
            ("latestPeriodOrHighestSystem", latest_period_or_highest_system),
            ("latestEpochOrHighestSeries", latest_epoch_or_highest_series),
            ("latestAgeOrHighestStage", latest_age_or_highest_stage),
            ("license", license),
            ("lifeStage", life_stage),
            ("locality", locality),
            ("lowestBiostratigraphicZone", lowest_biostratigraphic_zone),
            ("mediaType", media_type),
            ("member", member),
            ("modified", modified),
            ("month", month),
            ("networkKey", network_key),
            ("occurrenceId", occurrence_id),
            ("occurrenceStatus", occurrence_status),
            ("orderKey", order_key),
            ("organismId", organism_id),
            ("organismQuantity", organism_quantity),
            ("organismQuantityType", organism_quantity_type),
            ("otherCatalogNumbers", other_catalog_numbers),
            ("parentEventId", parent_event_id),
            ("pathway", pathway),
            ("phylumKey", phylum_key),
            ("preparations", preparations),
            ("previousIdentifications", previous_identifications),
            ("programme", programme),
            ("projectId", project_id),
            ("protocol", protocol),
            ("publishedByGbifRegion", published_by_gbif_region),
            ("publishingOrg", publising_org),
            ("recordedBy", recorded_by),
            ("recordedById", recorded_by_id),
            ("recordNumber", record_number),
            ("relativeOrganismQuantity", relative_organism_quantity),
            ("repatriated", repatriated),
            ("sampleSizeUnit", sample_size_unit),
            ("sampleSizeValue", sample_size_value),
            ("samplingProtocol", sampling_protocol),
            ("sex", sex),
            ("scientificName", scientific_name),
            ("speciesKey", species_key),
            ("startDayOfYear", start_day_of_year),
            ("stateProvince", state_province),
            ("taxonConceptId", taxon_concept_id),
            ("taxonKey", taxon_key),
            ("taxonId", taxon_id),
            ("taxonomicStatus", taxonomic_status),
            ("typeStatus", type_status),
            ("verbatimScientificName", verbatim_scientific_name),
            ("waterBody", water_body),
            ("year", year),
            ("hl", highlight),
            ("q", query),
            ("limit", limit),
            ("offset", offset),
            ("facet", facet),
            ("facetMincount", facet_mincount),
            ("facetMultiselect", facet_multiselect),
            ("facetLimit", facet_limit),
            ("facetOffset", facet_offset),
            ("publishingCountry", publishing_country),
        ]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url+self.endpoint, params=params)

    # Requires authentication. User must have an account with GBIF.  
    def search_occurrences_using_predicates(self, username=None, password=None,
                                            limit: Optional[int]=None,
                                            offset: Optional[int]=None,
                                            facet: Optional[str]=None,
                                            facet_mincount: Optional[int]=None,
                                            facet_multiselect: Optional[bool]=None,
                                            facet_limit: Optional[int]=None,
                                            facet_offset: Optional[int]=None):
        """
        Full search across all occurrences specified using predicates (as used for the download API).
        
        Args:
            username (str): Required. One's GBIF username.
            password (str): Required. One's GBIF password.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the maximum threshold, which is 300 for this service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. This service has a maximum offset of 100,000.
            facet (str): Optional. A facet name used to retrieve the most frequent values for a field. Facets are allowed for all search parameters except geometry and geoDistance. This parameter may by repeated to request multiple facets, as in this example. Note terms not available for searching are not available for faceting.
            facet_mincount (int): Optional. Used in combination with the facet parameter. Set facetMincount={#} to exclude facets with a count less than {#}, e.g. [/search?facet=basisOfRecord&limit=0&facetMincount=10000](https://api.gbif.org/v1/occurrence/search?facet=basisOfRecord&limit=0&facetMincount=1000000].
            facet_multiselect (bool): Optional. Used in combination with the facet parameter. Set facetMultiselect=true to still return counts for values that are not currently filtered, e.g. /search?facet=basisOfRecord&limit=0&basisOfRecord=HUMAN_OBSERVATION&facetMultiselect=true still shows Basis of Record values 'PRESERVED_SPECIMEN' and so on, even though Basis of Record is being filtered.
            facet_limit (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            facet_offset (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
                
        Returns:
            dict: Dictionary containing the search results.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("limit", limit),
            ("offset", offset),
            ("facet", facet),
            ("facetMincount", facet_mincount),
            ("facetMultiselect", facet_multiselect),
            ("facetLimit", facet_limit),
            ("facetOffset", facet_offset),
        ]
        hc.add_params(params, params_list)
        resource = "/predicate"
        if self.auth_type == "basic":
            auth = (username, password)
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, auth=auth, json=params)  
        else: #OAuth
            headers = self.auth_headers
            return hc.post_with_auth_and_json(base_url+self.endpoint+resource, headers=headers, json=params)
         
    def suggest_catalogue_numbers(self, query, limit):
        """
        Search that returns matching catalogue numbers. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested catalogue numbers.
        """
        resource = f"/catalogNumber?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)
        
    def suggest_collection_codes(self, query, limit):
        """
        Search that returns matching collection codes. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested collection codes.
        """
        resource = f"/collectionCode?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_dataset_names(self, query, limit):
        """
        Search that returns matching dataset names. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested dataset names.
        """
        resource = f"/datasetName?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_event_ids(self, query, limit):
        """
        Search that returns matching event ids. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested event ids.
        """
        resource = f"/eventId?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_identified_by_values(self, query, limit):
        """
        Search that returns matching identified by values. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested identified by values.
        """
        resource = f"/identifiedBy?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_institution_codes(self, query, limit):
        """
        Search that returns matching institution codes. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested institution codes.
        """
        resource = f"/institutionCode?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_localities(self, query, limit):
        """
        Search that returns matching localities. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested localities.
        """
        resource = f"/locality?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)
        
    def suggest_occurrence_ids(self, query, limit):
        """
        Search that returns matching occurrence ids. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested occurrence ids.
        """
        resource = f"/occurrenceId?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)
        
    def suggest_organism_ids(self, query, limit):
        """
        Search that returns matching organism ids. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested organism ids.
        """
        resource = f"/organismId?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)
        
    def suggest_other_catalogue_numbers(self, query, limit):
        """
        Search that returns matching other catalogue numbers. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested other catalogue numbers.
        """
        resource = f"/otherCatalogNumbers?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_parent_event_ids(self, query, limit):
        """
        Search that returns matching parent event ids. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested parent event ids.
        """
        resource = f"/parentEventId?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_record_numbers(self, query, limit):
        """
        Search that returns matching record numbers. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested record numbers.
        """
        resource = f"/recordNumber?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_recorded_by_values(self, query, limit):
        """
        Search that returns matching recorded by values. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested recorded by values.
        """
        resource = f"/recordedBy?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_sampling_protocols(self, query, limit):
        """
        Search that returns matching sampling protocols. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested sampling protocols.
        """
        resource = f"/samplingProtocol?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_state_provinces(self, query, limit):
        """
        Search that returns matching state provinces. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested state provinces.
        """
        resource = f"/stateProvince?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)

    def suggest_water_bodies(self, query, limit):
        """
        Search that returns matching water bodies. Results are ordered by relevance.
        
        Args:
            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
            limit (int): Required. Controls the number of suggestions. Example : 5

        Returns:
            list: A list containing suggested water bodies.
        """
        resource = f"/waterBody?q={query}&limit={limit}"
        return hc.get(base_url+self.endpoint+resource)
                    
### NOT WORKING 
#        def suggest_supported_terms_values(self, term, query, limit):
#        """
#        Search that returns values for supported terms. Results are ordered by relevance.
#        
#        Args:
#            term (str): Required. A supported term. Available values : PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN, OBSERVATION, HUMAN_OBSERVATION, MACHINE_OBSERVATION, MATERIAL_SAMPLE, LITERATURE, MATERIAL_CITATION, OCCURRENCE, UNKNOWN
#            query (str): Required. Simple search suggestion parameter. Wildcards are not supported. Example : A
#            limit (int): Required. Controls the number of suggestions. Example : 5
#
#        Returns:
#            list: A list containing suggested values for supported terms.
#        """
#        endpoint = f"occurrence/search/experimental/term/{{term}}?term={term}&q={query}&limit={limit}"
#        print(endpoint)
#        return mr.make_request(self.base_url+endpoint)
  
 
 
 
 
 
     
 
         

                 
                                                   
                                 

                 
                                  
                                                                    
                                             
 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           