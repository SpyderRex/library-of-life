from typing import Optional, Dict, Any

import requests_cache

from ..gbif_root import GBIF
from ..utils import http_client as hc

base_url = GBIF().base_url


class OccurrenceDownload:
    """
    A class for interacting with the download section of the Occurrence API.

    Attributes:
        endpoint: endpoint for this section of the API.
    """

    def __init__(
        self,
        use_caching=False,
        cache_name="occurrence_download_cache",
        backend="sqlite",
        expire_after=3600,
        auth_type="basic",
        client_id=None,
        client_secret=None,
        token_url=None,
    ):
        self.endpoint = "occurrence/download"
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
