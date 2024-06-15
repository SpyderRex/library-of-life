from typing import Optional, Dict, Any

import requests_cache

from ..gbif_root import GBIF
from ..utils import http_client as hc

base_url = GBIF().base_url


class Literature:
    """
    A class for interacting with the Literuari API.

    Attributes:
        endpoint: endpoint for this section of the API.
    """

    def __init__(
        self,
        use_caching=False,
        cache_name="literature_cache",
        backend="sqlite",
        expire_after=3600,
        auth_type="basic",
        client_id=None,
        client_secret=None,
        token_url=None,
    ):
        self.endpoint = "literature"
        self.auth_type = auth_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

        if auth_type == "OAuth":
            if not all([client_id, client_secret, token_url]):
                raise ValueError(
                    "Client ID, client secret, and token URL must be provided for OAuth authentication."
                )
            self.auth_headers = hc.get_oauth_headers(
                client_id, client_secret, token_url
            )

        if use_caching:
            requests_cache.install_cache(
                cache_name, backend=backend, expire_after=expire_after
            )

    def get_literature_details_by_id(self, uuid):
        """
        Retrieve details for a single literature item.

        Args:
            uuid (str): UUID for the literature item. Example : 83a00190-7038-3970-a7e8-5e5563c40e37

        Returns:
            dict: A dictionary containing the literature details.
        """
        resource = f"/{uuid}"
        return hc.get(base_url + self.endpoint + resource)

    def search_literature(
        self,
        citation_type: Optional[list[str]] = None,
        countries_of_coverage: Optional[list[str]] = None,
        countries_of_researcher: Optional[list[str]] = None,
        doi: Optional[list[str]] = None,
        gbif_dataset_key: Optional[str] = None,
        gbif_download_key: Optional[list[str]] = None,
        gbif_higher_taxon_key: Optional[list[int]] = None,
        gbif_network_key: Optional[str] = None,
        gbif_occurrence_key: Optional[list[int]] = None,
        gbif_project_identifier: Optional[str] = None,
        gbif_programme_acronym: Optional[str] = None,
        gbif_taxon_key: Optional[list[int]] = None,
        literature_type: Optional[list[str]] = None,
        open_access: Optional[bool] = None,
        peer_review: Optional[bool] = None,
        publisher: Optional[list[str]] = None,
        publishing_organization_key: Optional[list[str]] = None,
        relevance: Optional[list[str]] = None,
        source: Optional[list[str]] = None,
        topics: Optional[list[str]] = None,
        year: Optional[int] = None,
        language: Optional[str] = None,
        highlight: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        facet: Optional[str] = None,
        facet_mincount: Optional[int] = None,
        facet_multiselect: Optional[bool] = None,
        facet_limit: Optional[int] = None,
        facet_offset: Optional[int] = None,
        query: Optional[str] = None,
    ):
        """
        Full-text and parameterized search across all literature.

        Args:
            citation_type (list[str]): Optional. The manner in which GBIF is cited in a paper. Make a facet query for available values.
            countries_of_coverage (list[str]): Optional. Country or area of focus of study. Country codes are listed in our Country enum. See this endpoint's docs for available values.
            countries_of_research (list[str]): Optional. Country or area of institution with which author is affiliated. Country codes are listed in our Country enum. See this endpoint's docs for available values.
            doi (list[str]): Optional. Digital Object Identifier (DOI) of the literature item.
            gbif_dataset_key (list[str]): Optional. GBIF dataset referenced in publication.
            gbif_download_key (list[str]): Optional. GBIF download referenced in publication.
            gbif_higher_taxon_key (list[int]): Optional. All parent keys of any taxon that is the focus of the paper (see gbifTaxonKey).
            gbif_network_key (str): Optional. GBIF network referenced in publication.
            gbif_occurence_key (list[int]): Optional. Any GBIF occurrence keys directly mentioned in a paper.
            gbif_project_identifier (str): Optional. GBIF dataset referenced in publication.
            gbif_programme_acronym (str): Optional. GBIF dataset referenced in publication.
            gbif_taxon_key (list[int]): Optional. Key(s) from the GBIF backbone of taxa that are the focus of a paper.
            literature_type (list[str]): Optional. Type of literature, e.g. journal article. Available values : JOURNAL, BOOK, GENERIC, BOOK_SECTION, CONFERENCE_PROCEEDINGS, WORKING_PAPER, REPORT, WEB_PAGE, THESIS, MAGAZINE_ARTICLE, STATUTE, PATENT, NEWSPAPER_ARTICLE, COMPUTER_PROGRAM, HEARING, TELEVISION_BROADCAST, ENCYCLOPEDIA_ARTICLE, CASE, FILM, BILL.
            open_access (bool): Optional. Is the publication Open Access?
            peer_review (bool): Optional. Has the publication undergone peer review?
            publisher (list[str]): Optional. Publisher of journal.
            publishing_organization_key (list[str]): Optional. Publisher whose dataset is referenced in publication.
            relevance (list[str]): Optional. Relevance to GBIF community, see literature relevance..Available values : GBIF_USED, GBIF_CITED, GBIF_DISCUSSED, GBIF_PRIMARY, GBIF_ACKNOWLEDGED, GBIF_PUBLISHED, GBIF_AUTHOR, GBIF_MENTIONED, GBIF_FUNDED.
            source (list[str]): Optional. Journal of publication.
            topics (list[str]): Optional. Topic of publication. Available values : AGRICULTURE, BIODIVERSITY_SCIENCE, BIOGEOGRAPHY, CITIZEN_SCIENCE, CLIMATE_CHANGE, CONSERVATION, DATA_MANAGEMENT, DATA_PAPER, ECOLOGY, ECOSYSTEM_SERVICES, EVOLUTION, FRESHWATER, HUMAN_HEALTH, INVASIVES, MARINE, PHYLOGENETICS, SPECIES_DISTRIBUTIONS, TAXONOMY.
            year (int): Optional. Year of publication. This can be a single range such as 2019,2021, or can be repeated to search multiple years.
            language (str): Optional. Language of publication. Language codes are listed in our Language enum. See this endpoint's docs for available values.
            highlight (bool): Optional. Set highlight=True to highlight terms matching the query when in full-text search fields. The highlight will be an emphasis tag of class gbifH1 e.g. /search?q=plant&hl=true. Full-text search fields include: title, keyword, country, publishing country, publishing organization title, hosting organization title, and description. One additional full text field is searched which includes information from metadata documents, but the text of this field is not returned in the response. Example : true
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the maximum threshold, which is 300 for this service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. This service has a maximum offset of 100,000.
            facet (str): Optional. A facet name used to retrieve the most frequent values for a field. Facets are allowed for all search parameters except geometry and geoDistance. Note terms not available for searching are not available for faceting.
            facet_mincount (int): Optional. Used in combination with the facet parameter. Set facetMincount={#} to exclude facets with a count less than {#}, e.g. [/search?facet=basisOfRecord&limit=0&facetMincount=10000](https://api.gbif.org/v1/occurrence/search?facet=basisOfRecord&limit=0&facetMincount=1000000].
            facet_multiselect (bool): Optional. Used in combination with the facet parameter. Set facetMultiselect=true to still return counts for values that are not currently filtered, e.g. /search?facet=basisOfRecord&limit=0&basisOfRecord=HUMAN_OBSERVATION&facetMultiselect=true still shows Basis of Record values 'PRESERVED_SPECIMEN' and so on, even though Basis of Record is being filtered.
            facet_limit (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            facet_offset (int): Optional. Facet parameters allow paging requests using the parameters facetOffset and facetLimit.
            query (str): Optional. Simple full-text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.

        Returns:
            dict: A dictionary containing the literature items.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("citationType", citation_type),
            ("countriesOfCoverage", countries_of_coverage),
            ("countriesOfResearcher", countries_of_researcher),
            ("doi", doi),
            ("gbifDatasetKey", gbif_dataset_key),
            ("gbifDownloadKey", gbif_download_key),
            ("gbifHigherTaxonKey", gbif_higher_taxon_key),
            ("gbifNetworkKey", gbif_network_key),
            ("gbifOccurrenceKey", gbif_occurrence_key),
            ("gbifProjectIdentifier", gbif_project_identifier),
            ("gbifProgrammeAcronym", gbif_programme_acronym),
            ("gbifTaxonKey", gbif_taxon_key),
            ("literatureType", literature_type),
            ("openAccess", open_access),
            ("peerReview", peer_review),
            ("publisher", publisher),
            ("publishingOrganizationKey", publishing_organization_key),
            ("relevance", relevance),
            ("source", source),
            ("topics", topics),
            ("year", year),
            ("language", language),
            ("hl", highlight),
            ("limit", limit),
            ("offset", offset),
            ("facet", facet),
            ("facetMincount", facet_mincount),
            ("facetMultiselect", facet_multiselect),
            ("facetLimit", facet_limit),
            ("facetOffset", facet_offset),
            ("q", query),
        ]
        hc.add_params(params, params_list)
        resource = "/search"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def export_literature_search(
        self,
        export_format="TSV",
        citation_type: Optional[list[str]] = None,
        countries_of_coverage: Optional[list[str]] = None,
        countries_of_researcher: Optional[list[str]] = None,
        doi: Optional[list[str]] = None,
        gbif_dataset_key: Optional[str] = None,
        gbif_download_key: Optional[list[str]] = None,
        gbif_higher_taxon_key: Optional[list[int]] = None,
        gbif_network_key: Optional[str] = None,
        gbif_occurrence_key: Optional[list[int]] = None,
        gbif_project_identifier: Optional[str] = None,
        gbif_programme_acronym: Optional[str] = None,
        gbif_taxon_key: Optional[list[int]] = None,
        literature_type: Optional[list[str]] = None,
        open_access: Optional[bool] = None,
        peer_review: Optional[bool] = None,
        publisher: Optional[list[str]] = None,
        publishing_organization_key: Optional[list[str]] = None,
        relevance: Optional[list[str]] = None,
        source: Optional[list[str]] = None,
        topics: Optional[list[str]] = None,
        year: Optional[int] = None,
        language: Optional[str] = None,
        query: Optional[str] = None,
    ):
        """
        Exports the result of a literature search.

        Args:
            export_format (str): The format for the search results export. Defaults to TSV. Available values : CSV, TSV.
            citation_type (list[str]): Optional. The manner in which GBIF is cited in a paper. Make a facet query for available values.
            countries_of_coverage (list[str]): Optional. Country or area of focus of study. Country codes are listed in our Country enum. See this endpoint's docs for available values.
            countries_of_research (list[str]): Optional. Country or area of institution with which author is affiliated. Country codes are listed in our Country enum. See this endpoint's docs for available values.
            doi (list[str]): Optional. Digital Object Identifier (DOI) of the literature item.
            gbif_dataset_key (list[str]): Optional. GBIF dataset referenced in publication.
            gbif_download_key (list[str]): Optional. GBIF download referenced in publication.
            gbif_higher_taxon_key (list[int]): Optional. All parent keys of any taxon that is the focus of the paper (see gbifTaxonKey).
            gbif_network_key (str): Optional. GBIF network referenced in publication.
            gbif_occurence_key (list[int]): Optional. Any GBIF occurrence keys directly mentioned in a paper.
            gbif_project_identifier (str): Optional. GBIF dataset referenced in publication.
            gbif_programme_acronym (str): Optional. GBIF dataset referenced in publication.
            gbif_taxon_key (list[int]): Optional. Key(s) from the GBIF backbone of taxa that are the focus of a paper.
            literature_type (list[str]): Optional. Type of literature, e.g. journal article. Available values : JOURNAL, BOOK, GENERIC, BOOK_SECTION, CONFERENCE_PROCEEDINGS, WORKING_PAPER, REPORT, WEB_PAGE, THESIS, MAGAZINE_ARTICLE, STATUTE, PATENT, NEWSPAPER_ARTICLE, COMPUTER_PROGRAM, HEARING, TELEVISION_BROADCAST, ENCYCLOPEDIA_ARTICLE, CASE, FILM, BILL.
            open_access (bool): Optional. Is the publication Open Access?
            peer_review (bool): Optional. Has the publication undergone peer review?
            publisher (list[str]): Optional. Publisher of journal.
            publishing_organization_key (list[str]): Optional. Publisher whose dataset is referenced in publication.
            relevance (list[str]): Optional. Relevance to GBIF community, see literature relevance..Available values : GBIF_USED, GBIF_CITED, GBIF_DISCUSSED, GBIF_PRIMARY, GBIF_ACKNOWLEDGED, GBIF_PUBLISHED, GBIF_AUTHOR, GBIF_MENTIONED, GBIF_FUNDED.
            source (list[str]): Optional. Journal of publication.
            topics (list[str]): Optional. Topic of publication. Available values : AGRICULTURE, BIODIVERSITY_SCIENCE, BIOGEOGRAPHY, CITIZEN_SCIENCE, CLIMATE_CHANGE, CONSERVATION, DATA_MANAGEMENT, DATA_PAPER, ECOLOGY, ECOSYSTEM_SERVICES, EVOLUTION, FRESHWATER, HUMAN_HEALTH, INVASIVES, MARINE, PHYLOGENETICS, SPECIES_DISTRIBUTIONS, TAXONOMY.
            year (int): Optional. Year of publication. This can be a single range such as 2019,2021, or can be repeated to search multiple years.
            language (str): Optional. Language of publication. Language codes are listed in our Language enum. See this endpoint's docs for available values.
            query (str): Optional. Simple full-text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.

        Returns:
            str: The export search results in TSV or CSV format.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("format", export_format),
            ("citationType", citation_type),
            ("countriesOfCoverage", countries_of_coverage),
            ("countriesOfResearcher", countries_of_researcher),
            ("doi", doi),
            ("gbifDatasetKey", gbif_dataset_key),
            ("gbifDownloadKey", gbif_download_key),
            ("gbifHigherTaxonKey", gbif_higher_taxon_key),
            ("gbifNetworkKey", gbif_network_key),
            ("gbifOccurrenceKey", gbif_occurrence_key),
            ("gbifProjectIdentifier", gbif_project_identifier),
            ("gbifProgrammeAcronym", gbif_programme_acronym),
            ("gbifTaxonKey", gbif_taxon_key),
            ("literatureType", literature_type),
            ("openAccess", open_access),
            ("peerReview", peer_review),
            ("publisher", publisher),
            ("publishingOrganizationKey", publishing_organization_key),
            ("relevance", relevance),
            ("source", source),
            ("topics", topics),
            ("year", year),
            ("language", language),
            ("q", query),
        ]
        hc.add_params(params, params_list)
        resource = "/export"
        return hc.get_for_content_with_params(
            base_url + self.endpoint + resource, params=params
        ).decode("utf-8")
