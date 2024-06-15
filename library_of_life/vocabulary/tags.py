from typing import Optional, Dict, Any

import requests_cache

from ..gbif_root import GBIF
from ..utils import http_client as hc

base_url = GBIF().base_url


class Tags:
    """
    A class for interacting with the tags section of the Vocabulary API.

    Attributes:
        endpoint: endpoint for this section of the API.
    """

    def __init__(
        self,
        use_caching=False,
        cache_name="tags_cache",
        backend="sqlite",
        expire_after=3600,
        auth_type="basic",
        client_id=None,
        client_secret=None,
        token_url=None,
    ):
        self.endpoint = "vocabularyTags"
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

    def list_all_tags(self, limit: Optional[int] = None, offset: Optional[int] = None):
        """
        Lists all current tags.

        Args:
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.

        Returns:
            dict: A dictionary containing a list of tags.
        """
        params: Dict[str, Any] = {}
        params_list = [("limit", limit), ("offset", offset)]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url + self.endpoint, params=params)

    # Requires authentication. User must have an account with GBIF.
    def create_new_tag(self, username, password, payload):
        """
        Creates a new tag. The default color is white.

        Args:
            username (str): The username.
            password (str): The user's password.
            payload (dict): The json response body. See this endpoint's docs for schema.

        Returns:
            str, dict: A message of success or failure and returned tag if successful.
        """
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.post_with_auth_and_json(
                base_url + self.endpoint, auth=auth, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

        else:  # OAuth
            headers = self.auth_headers
            response = hc.post_with_auth_and_json(
                base_url + self.endpoint, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    def get_details_of_single_tag(self, name):
        """
        Details of a single tag.

        Args:
            name (str): The name of the tag.

        Returns:
            dict: A dictionary containing the tag details.
        """
        resource = f"/{name}"
        return hc.get(base_url + self.endpoint + resource)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def update_existing_tag(self, name, username, password, payload):
        """
        Updates the existing tag.

        Args:
            name (str): The name of the tag.
            username (str): The username.
            password (str): The password.
            payload (dict): The JSON object request body containing the updated information.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{name}"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.put_with_auth_and_json(
                base_url + self.endpoint + resource, auth=auth, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

        else:  # OAuth
            headers = self.auth_headers
            response = hc.post_with_auth_and_json(
                base_url + self.endpoint, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def delete_existing_tag(self, name, username, password):
        """
        Deletes a definition from an existing concept.

        Args:
            name (str): The name of the concept.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{name}"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.delete_with_auth(
                base_url + self.endpoint + resource, auth=auth
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

        else:  # OAuth
            headers = self.auth_headers
            response = hc.delete_with_auth(base_url + self.endpoint, headers=headers)
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response
