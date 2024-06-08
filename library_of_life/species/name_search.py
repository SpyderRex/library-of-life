from typing import Optional, Dict, Any

from requests.exceptions import JSONDecodeError
import requests_cache

from .. gbif_root import GBIF
from .. utils import http_client as hc

base_url = GBIF().base_url

class NameSearch:
    """
    A class for interacting with the name search section of the Species API.
    
    Attributes:
        endpoint: The endpoint for this section of the API.
    """
    def __init__(self, use_caching=False, 
                cache_name="name_search_cache", 
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
                   
    def autocomplete_species(self, dataset_key: Optional[str]=None,
                     constituent_key: Optional[str]=None,
                     rank: Optional[str]=None,
                     higher_taxon_key: Optional[str]=None,
                     status: Optional[str]=None,
                     is_extinct: Optional[bool]=None,
                     habitat: Optional[str]=None,
                     threat: Optional[str]=None,
                     name_type: Optional[str]=None,
                     nomenclaturual_status: Optional[str]=None,
                     origin: Optional[str]=None,
                     issue: Optional[str]=None,
                     query: Optional[str]=None):
        """
        Returns up to 20 name usages by doing prefix matching against the scientific name. Results are ordered by relevance.
        
        Args:
            dataset_key (str): Optional. A UUID of a checklist dataset. Example : d7dddbf4-2cf0-4f39-9b2a-bb099caae36c.
            constituent_key (str): Optional. The (sub)dataset constituent key as a UUID. Useful to query larger assembled datasets such as the GBIF Backbone or the Catalogue of Life.
            rank (str): Optional. Filters by taxonomic rank as given in our https://api.gbif.org/v1/enumeration/basic/Rank[Rank enum]. See this endpoint's docs for available values.
            higher_taxon_key (str): Optional. Filters by any of the higher Linnean rank keys. Note this is within the respective checklist and not searching NUB keys across all checklists.
            status (str): Optional. Filters by the taxonomic status as given in our https://api.gbif.org/v1/enumeration/basic/TaxonomicStatus[TaxonomicStatus enum]. Available values : ACCEPTED, DOUBTFUL, SYNONYM, HETEROTYPIC_SYNONYM, HOMOTYPIC_SYNONYM, PROPARTE_SYNONYM, MISAPPLIED.
            is_extinct (bool): Optional. Filters by extinction status.
            habitat (str): Optional. Filters by the habitat. Currently only 3 major biomes are accepted in our https://api.gbif.org/v1/enumeration/basic/Habitat[Habitat enum]. Available values : MARINE, FRESHWATER, TERRESTRIAL.
            threat (str): Optional. Filters by the taxonomic threat status as given in our https://api.gbif.org/v1/enumeration/basic/ThreatStatus[ThreatStatus enum]. Available values : EXTINCT, EXTINCT_IN_THE_WILD, REGIONALLY_EXTINCT, CRITICALLY_ENDANGERED, ENDANGERED, VULNERABLE, NEAR_THREATENED, LEAST_CONCERN, DATA_DEFICIENT, NOT_APPLICABLE, NOT_EVALUATED.
            name_type (str): Optional. Filters by the name type as given in our https://api.gbif.org/v1/enumeration/basic/NameType[NameType enum]. Available values : SCIENTIFIC, VIRUS, HYBRID, INFORMAL, CULTIVAR, CANDIDATUS, OTU, DOUBTFUL, PLACEHOLDER, NO_NAME, BLACKLISTED.
            nomenclatural_status (str): Optional. Filters by the nomenclatural status as given in our https://api.gbif.org/v1/enumeration/basic/NomenclaturalStatus[Nomenclatural Status enum]. See this endpoint's docs for available values.
            origin (str): Optional. Filters for name usages with a specific origin. Available values : SOURCE, DENORMED_CLASSIFICATION, VERBATIM_PARENT, VERBATIM_ACCEPTED, VERBATIM_BASIONYM, PROPARTE, AUTONYM, IMPLICIT_NAME, MISSING_ACCEPTED, BASIONYM_PLACEHOLDER, EX_AUTHOR_SYNONYM, OTHER.
            issue (str): Optional. A specific indexing issue as defined in our https://api.gbif.org/v1/enumeration/basic/NameUsageIssue[NameUsageIssue enum]. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
        
        Returns:
            dict: A dictionary containing up to 20 name usages.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("datasetKey", dataset_key),
                ("constituentKey", constituent_key),
                ("rank", rank),
                ("higherTaxonKey", higher_taxon_key),
                ("status", status),
                ("isExtinct", is_extinct),
                ("habitat", habitat),
                ("threat", threat),
                ("nameType", name_type),
                ("nomenclaturalStatus", nomenclaturual_status),
                ("origin", origin),
                ("issue", issue),
                ("q", query)]
        hc.add_params(params, params_list)
        resource = "/suggest"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def search_species(self, dataset_key: Optional[str]=None,
                     constituent_key: Optional[str]=None,
                     rank: Optional[str]=None,
                     higher_taxon_key: Optional[str]=None,
                     status: Optional[str]=None,
                     is_extinct: Optional[bool]=None,
                     habitat: Optional[str]=None,
                     threat: Optional[str]=None,
                     name_type: Optional[str]=None,
                     nomenclaturual_status: Optional[str]=None,
                     origin: Optional[str]=None,
                     issue: Optional[str]=None,
                     query: Optional[str]=None,
                     highlight: Optional[bool]=None,
                     limit: Optional[int]=None,
                     offset: Optional[int]=None,
                     facet: Optional[list]=None,
                     facet_mincount: Optional[int]=None,
                     facet_multiselect: Optional[bool]=None,
                     facet_limit: Optional[int]=None,
                     facet_offset: Optional[int]=None):
        """
        Returns results of a full-text search of name usages covering the scientific and vernacular names, the species description, distribution and the entire classification across all name usages of all or some checklists. Results are ordered by relevance as this search usually returns a lot of results.
        Args:
            dataset_key (str): Optional. A UUID of a checklist dataset. Example : d7dddbf4-2cf0-4f39-9b2a-bb099caae36c.
            constituent_key (str): Optional. The (sub)dataset constituent key as a UUID. Useful to query larger assembled datasets such as the GBIF Backbone or the Catalogue of Life.
            rank (str): Optional. Filters by taxonomic rank as given in our https://api.gbif.org/v1/enumeration/basic/Rank[Rank enum]. See this endpoint's docs for available values.
            higher_taxon_key (str): Optional. Filters by any of the higher Linnean rank keys. Note this is within the respective checklist and not searching NUB keys across all checklists.
            status (str): Optional. Filters by the taxonomic status as given in our https://api.gbif.org/v1/enumeration/basic/TaxonomicStatus[TaxonomicStatus enum]. Available values : ACCEPTED, DOUBTFUL, SYNONYM, HETEROTYPIC_SYNONYM, HOMOTYPIC_SYNONYM, PROPARTE_SYNONYM, MISAPPLIED.
            is_extinct (bool): Optional. Filters by extinction status.
            habitat (str): Optional. Filters by the habitat. Currently only 3 major biomes are accepted in our https://api.gbif.org/v1/enumeration/basic/Habitat[Habitat enum]. Available values : MARINE, FRESHWATER, TERRESTRIAL.
            threat (str): Optional. Filters by the taxonomic threat status as given in our https://api.gbif.org/v1/enumeration/basic/ThreatStatus[ThreatStatus enum]. Available values : EXTINCT, EXTINCT_IN_THE_WILD, REGIONALLY_EXTINCT, CRITICALLY_ENDANGERED, ENDANGERED, VULNERABLE, NEAR_THREATENED, LEAST_CONCERN, DATA_DEFICIENT, NOT_APPLICABLE, NOT_EVALUATED.
            name_type (str): Optional. Filters by the name type as given in our https://api.gbif.org/v1/enumeration/basic/NameType[NameType enum]. Available values : SCIENTIFIC, VIRUS, HYBRID, INFORMAL, CULTIVAR, CANDIDATUS, OTU, DOUBTFUL, PLACEHOLDER, NO_NAME, BLACKLISTED.
            nomenclatural_status (str): Optional. Filters by the nomenclatural status as given in our https://api.gbif.org/v1/enumeration/basic/NomenclaturalStatus[Nomenclatural Status enum]. See this endpoint's docs for available values.
            origin (str): Optional. Filters for name usages with a specific origin. Available values : SOURCE, DENORMED_CLASSIFICATION, VERBATIM_PARENT, VERBATIM_ACCEPTED, VERBATIM_BASIONYM, PROPARTE, AUTONYM, IMPLICIT_NAME, MISSING_ACCEPTED, BASIONYM_PLACEHOLDER, EX_AUTHOR_SYNONYM, OTHER.
            issue (str): Optional. A specific indexing issue as defined in our https://api.gbif.org/v1/enumeration/basic/NameUsageIssue[NameUsageIssue enum]. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            highlight (bool): Optional. Set hl=true to highlight terms matching the query when in fulltext search fields. The highlight will be an emphasis tag of class gbifHl.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            facet (list): Optional. A facet name used to retrieve the most frequent values for a field. This parameter may be repeated to request multiple facets.
            facet_mincount (int): Optional. Used in combination with the facet parameter. Set facetMincount={#} to exclude facets with a count less than {#}.
            facet_multiselect (bool): Optional. Used in combination with the facet parameter. Set facetMultiselect=true to still return counts for values that are not currently filtered.
            facet_limit (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            facet_offset (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
        
        Returns:
            dict: A dictionary containing species data from search.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("datasetKey", dataset_key),
                ("constituentKey", constituent_key),
                ("rank", rank),
                ("higherTaxonKey", higher_taxon_key),
                ("status", status),
                ("isExtinct", is_extinct),
                ("habitat", habitat),
                ("threat", threat),
                ("nameType", name_type),
                ("nomenclaturalStatus", nomenclaturual_status),
                ("origin", origin),
                ("issue", issue),
                ("q", query),
                ("hl", highlight),
                ("limit", limit),
                ("offset", offset),
                ("facet", facet),
                ("facetMincount", facet_mincount),
                ("facetMultiselect", facet_multiselect),
                ("facetLimit", facet_limit),
                ("facetOffset", facet_offset)]
        hc.add_params(params, params_list)
        resource = "/search"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
        
    def list_all_name_usages(self, limit, offset, language,
                            dataset_key: Optional[list]=None,
                            source_id: Optional[str]=None,
                            name: Optional[str]=None,
                            ):
        """
        Returns a list of all name usages across all checklists.
        
        Args:
            limit (int): Required. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Required. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.
            language (str): Required. Language for vernacular names, given as an ISO 639-1 two-letter code from our vocabulary. See this endpoint's docs for available values.
            dataset_key (list): Optional. A UUID of a checklist dataset.
            source_id (str): Optional. Filters by the source identifier.
            name (str): Optional. A name without authorship, to match exactly.
        
        Returns:
            dict: A dictionary containing a list name usages.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("limit", limit), 
                ("offset", offset),
                ("datasetKey", dataset_key),
                ("sourceId", source_id),
                ("name", name)]
        hc.add_params(params, params_list)
        headers = {"Accept-Language": language}
        return hc.get_with_params(base_url+self.endpoint, headers=headers, params=params)
        
    def fuzzy_name_match(self, usage_key: Optional[str]=None,
                         name: Optional[str]=None,
                         authorship: Optional[str]=None,
                         rank: Optional[str]=None,
                         generic_name: Optional[str]=None,
                         generic_epithet: Optional[str]=None,
                         infraspecific_epithet: Optional[str]=None,
                         strict: Optional[bool]=None,
                         verbose: Optional[bool]=None,
                         kingdom: Optional[str]=None,
                         phylum: Optional[str]=None,
                         order: Optional[str]=None,
                         cls: Optional[str]=None,
                         family: Optional[str]=None,
                         genus: Optional[str]=None):
        """
        Returns fuzzy matches of scientific names against the GBIF Backbone Taxonomy with the optional classification provided. If a classification is provided and strict is not set to true, the default matching will also try to match against these if no direct match is found for the name parameter alone.
        
        Args:
            usage_key (int): Optional. The usage key to look up. When provided, all other fields are ignored.
            name (str): Optional. The scientific name to fuzzy match against. May include the authorship and year.
            authorship (str): Optional. The scientific name authorship to fuzzy match against.
            rank (str): Optional. Filters by taxonomic rank as given in our https://api.gbif.org/v1/enumeration/basic/Rank[Rank enum]. See this endpoint's docs for available values.
            generic_name (str): Optional. Generic part of the name to match when given as atomised parts instead of the full name parameter.
            generic_epithet (str): Optional. Specific epithet to match.
            infraspecific_epithet (str): Optional. Infraspecific epithet to match.
            strict (bool): Optional. If true it fuzzy matches only the given name, but never a taxon in the upper classification.
            verbose (bool): Optional. If true it shows alternative matches which were considered but then rejected.
            kingdom (str): Optional. Kingdom to match.
            phylum (str): Optional. Phylum to match.
            order (str): Optional. Order to match.
            cls (str): Optional. Class to match.
            family (str): Optional. Family to match.
            genus (str): Optional. Genus to match.
        
        Returns:
            dict: A dictionary containing fuzzy matches of scientific names.
        """
        params: Dict[str, Any] = {}
        params_list = [
                ("usageKey", usage_key),
                ("name", name),
                ("authorship", authorship),
                ("rank", rank),
                ("genericName", generic_name),
                ("genericEpithet", generic_epithet),
                ("infraspecificEpithet", infraspecific_epithet),
                ("strict", strict),
                ("verbose", verbose),
                ("kingdom", kingdom),
                ("phylum", phylum),
                ("order", order),
                ("class", cls),
                ("family", family),
                ("genus", genus)]
        hc.add_params(params, params_list)
        resource = "/match"
        return hc.get_with_params(base_url+self.endpoint+resource, params=params)
 