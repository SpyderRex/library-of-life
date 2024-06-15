from typing import Optional, Dict, Any

import requests_cache

from ..gbif_root import GBIF
from ..utils import http_client as hc

base_url = GBIF().base_url


class Vocabularies:
    """
    A class for interacting with the vocabularies section of the Vocabulary API.

    Attributes:
        endpoint: endpoint for this section of the API.
    """

    def __init__(
        self,
        use_caching=False,
        cache_name="vocabularies_cache",
        backend="sqlite",
        expire_after=3600,
        auth_type="basic",
        client_id=None,
        client_secret=None,
        token_url=None,
    ):
        self.endpoint = "vocabularies"
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

    def list_all_vocabularies(
        self,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        deprecated: Optional[bool] = None,
        vocab_key: Optional[int] = None,
        has_unreleased_changes: Optional[bool] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        Lists all current vocabularies.

        Args:
            name (str): Optional. The name of the vocabulary.
            namespace (str): Optional. The namespace of the vocabulary.
            deprecated (bool): Optional. Is the vocabulary deprecated?
            vocab_key (int): Optional. The key of the vocabulary.
            has_unreleased_changes (bool): Optional. Has the vocabulary changes that haven't been released yet?
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.

        Returns:
            dict: A dictionary containing the vocabulary search results.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("name", name),
            ("namespace", namespace),
            ("deprecated", deprecated),
            ("key", vocab_key),
            ("has unreleased changes", has_unreleased_changes),
            ("q", query),
            ("limit", limit),
            ("offset", offset),
        ]
        hc.add_params(params, params_list)
        return hc.get_with_params(base_url + self.endpoint, params=params)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def create_new_vocabulary(self, username, password, payload):
        """
        Creates a new vocabulary. Note definitions and labels must be added in subsequent requests.

        Args:
            username (str): The username.
            password (str): The user's password.
            payload (dict): The request body JSON object.

        Returns:
            dict, str: Dictionary or string containing an error message or returned vocabulary if successful.
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

    def get_details_of_vocabulary(self, name):
        """
        Details of a single vocabulary.

        Args:
            name (str): The name of the vocabulary.

        Returns:
            dict: A dictionary containing the vocabulary details.
        """
        resource = f"/{name}"
        return hc.get(base_url + self.endpoint + resource)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def update_existing_vocabulary(self, name, username, password, payload):
        """
        Updates the existing vocabulary. Note definitions and labels are not changed with this method.

        Args:
            name (str): The name of the vocabulary.
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

    def suggest_vocabularies(self, locale, query: Optional[str] = None):
        """
        Search that returns up to 20 matching vocabularies. Results are ordered by relevance. The response is smaller than a vocabulary search.

        Args:
            locale (str): Required. Locale to filter by. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.

        Returns:
            dict: A dictionary containing the vocabulary suggestions.
        """
        params: Dict[str, Any] = {}
        params_list = [("locale", locale), ("q", query)]
        hc.add_params(params, params_list)
        resource = "/suggest"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def deprecate_existing_vocabulary(self, name, username, password, payload=None):
        """
        Deprecates the existing vocabulary. Optionally, a replacement vocabulary can be specified. Note that if the vocabulary has concepts they will be deprecated too and that has to be specified explicitly in the parameters.

        Args:
            name (str): The name of the vocabulary.
            username (str): The username.
            password (str): The password.
            payload (dict): The json object response body.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{name}/deprecate"
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
            response = hc.put_with_auth_and_json(
                base_url + self.endpoint, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def restore_deprecated_vocabulary(
        self,
        name,
        username,
        password,
        restore_deprecated_concepts: Optional[bool] = None,
    ):
        """
        Restores the deprecated vocabulary. Optionally, its deprecated concepts can be restored too if it is specified in the parameters.

        Args:
            name (str): The name of the vocabulary.
            username (str): The username.
            password (str): The password.
            restore_deprecated_concepts (bool): Set to true to restore deprecated concepts.

        Returns:
            string, dict: A message of success or failure of update.
        """
        params: Dict[str, Any] = {}
        params_list = [("restoreDeprecatedConcepts", restore_deprecated_concepts)]
        hc.add_params(params, params_list)
        resource = f"/{name}/deprecate"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.delete_with_auth(
                base_url + self.endpoint + resource, auth=auth, params=params
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

        else:  # OAuth
            headers = self.auth_headers
            response = hc.delete_with_auth(
                base_url + self.endpoint, headers=headers, params=params
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    def export_vocabulary(self, name):
        """
        Exports a vocabulary in JSON format.

        Args:
            name (str): The name of the vocabulary.

        Returns:
            dict: A dictionary containing the exported vocabulary.
        """
        resource = f"/{name}/export"
        return hc.get(base_url + self.endpoint + resource)

    def list_vocabulary_releases(
        self,
        name,
        version: Optional[str] = None,
        limit: Optional[str] = None,
        offset: Optional[str] = None,
    ):
        """
        Search that returns up to 20 matching vocabularies. Results are ordered by relevance. The response is smaller than a vocabulary search.

        Args:
            name (str): The name of the vocabulary.
            version (str): Optional. The version to filter by. To get the latest one you can specify 'latest'.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.

        Returns:
            dict: A dictionary containing the vocabulary release information.
        """
        params: Dict[str, Any] = {}
        params_list = [("version", version), ("limit", limit), ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{name}/releases"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def get_single_vocabulary_release(self, name, version):
        """
        Details of a single vocabulary release.

        Args:
            name (str): The name of the vocabulary.
            version (str): The version to filter by. To get the latest one you can specify 'latest'.

        Returns:
            dict: A dictionary containing the vocabulary information.
        """
        resource = f"/{name}/releases/{version}"
        return hc.get(base_url + self.endpoint + resource)

    def export_single_vocabulary_release(self, name, version):
        """
        Details of the exported release to see its content.

        Args:
            name (str): The name of the vocabulary.
            version (str): The version to filter by. To get the latest one you can specify 'latest'.

        Returns:
            dict: A dictionary containing the vocabulary information.
        """
        resource = f"/{name}/releases/{version}/export"
        response = hc.get_for_content(base_url + self.endpoint + resource).decode(
            "utf-8"
        )
        if response == "":
            return "Nothing found."
        else:
            return response

    def list_definitions_for_vocabulary(self, name, language):
        """
        Lists all definitions of the vocabulary.

        Arg:
            name (str): The name of the vocabulary.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the vocabulary definitions.
        """
        params = {"lang": language}
        resource = f"/{name}/definition"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_definition_to_vocabulary(self, username, password, name, payload):
        """
        Creates a definition and adds it to an existing vocabulary.

        Args:
            name (str): The name of the vocabulary.
            payload (dict): The json response body containing new definition. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned vocabulary if successful.
        """
        resource = f"/{name}/definition"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.post_with_auth_and_json(
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
                base_url + self.endpoint + resource, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    def get_vocabulary_definition(self, name, key):
        """
        Gets the definition of the vocabulary.

        Args:
            name (str): The name of the vocabulary.
            key (int): The key of the definition.

        Returns:
            dict: A dictionary containing vocabulary definition.
        """
        resource = f"/{name}/definition/{key}"
        return hc.get(base_url + self.endpoint + resource)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def update_vocabulary_definition(self, name, key, username, password, payload):
        """
        Updates a definition that belongs to an existing vocabulary.

        Args:
            name (str): The name of the vocabulary.
            key (int): The key of the definition.
            username (str): The username.
            password (str): The password.
            payload (dict): The json object response body.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{name}/definition/{key}"
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
            response = hc.put_with_auth_and_json(
                base_url + self.endpoint, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def delete_vocabulary_definition(self, name, key, username, password):
        """
        Deletes a definition from an existing vocabulary.

        Args:
            name (str): The name of the vocabulary.
            key (int): The key of the definition.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{name}/definition/{key}"
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

    def list_all_vocabulary_labels(self, name, language):
        """
        Lists all labels of the vocabulary.

        Arg:
            name (str): The name of the vocabulary.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the vocabulary labels.
        """
        params = {"lang": language}
        resource = f"/{name}/label"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_label_to_vocabulary(self, name, username, password, payload):
        """
        Creates a label and adds it to an existing vocabulary.

        Args:
            name (str): The name of the vocabulary.
            username (str): The username.
            password (str): The user's password.
            payload (dict): The json response body containing new label. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned vocabulary if successful.
        """
        resource = f"/{name}/label"
        if self.auth_type == "basic":
            auth = (username, password)
            response = hc.post_with_auth_and_json(
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
                base_url + self.endpoint + resource, headers=headers, json=payload
            )
            if "400" in response["error"]:
                return "Bad request: the JSON is invalid or the request is not well-formed."
            elif "422" in response["error"]:
                return "The request is syntactically correct but the fields are invalid (required fields not set, duplicated keys, inconsistent keys, etc.)"
            else:
                return response

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def delete_label_from_vocabulary(self, name, key, username, password):
        """
        Deletes a label from an existing vocabulary.

        Args:
            name (str): The name of the vocabulary.
            key (int): The key of the label.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{name}/label/{key}"
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
