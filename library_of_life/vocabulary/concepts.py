from typing import Optional, Dict, Any

import requests_cache

from ..gbif_root import GBIF
from ..utils import http_client as hc

base_url = GBIF().base_url


class Concepts:
    """
    A class for interacting with the concepts section of the Vocabulary API.

    Attributes:
        endpoint: endpoint for this section of the API.
    """

    def __init__(
        self,
        use_caching=False,
        cache_name="concepts_cache",
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

    def list_all_vocabulary_concepts(self, vocabulary_name, tags: Optional[str] = None):
        """
        Lists all concepts of the vocabulary.

        Args:
            vocabulary_name (str): Required. The name of the vocabulary.
            tags (str): Optional. The tags of the concept.

        Returns:
            dict: A dictionary containing the listed concepts.
        """
        params: Dict[str, Any] = {}
        params_list = [("tags", tags)]
        hc.add_params(params, params_list)
        resource = f"{vocabulary_name}/concepts"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def create_new_concept(self, vocabulary_name, username, password, payload):
        """
        Creates a new concept. Note definitions, labels, alternative labels, hidden labels and tags must be added in subsequent requests.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            username (str): The username.
            password (str): The user's password.
            payload (dict): The request body JSON object.

        Returns:
            dict, str: Dictionary or string containing an error message or returned concept if successful.
        """
        resource = f"/{vocabulary_name}/concepts"
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

    def get_details_of_concept(
        self,
        vocabulary_name,
        name,
        include_parents: Optional[bool] = None,
        include_children: Optional[bool] = None,
    ):
        """
        Details of a single concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            include_parents (bool): Optional.
            include_children (bool): Optional

        Returns:
            dict: A dictionary containing the concept details.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("includeParents", include_parents),
            ("includeChildren", include_children),
        ]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/{name}"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def update_existing_concept(
        self, vocabulary_name, name, username, password, payload
    ):
        """
        Updates the existing concept. Note definitions, labels, alternative labels, hidden labels and tags are not changed with this method.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The password.
            payload (dict): The JSON object request body containing the updated information.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{vocabulary_name}/concepts/{name}"
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

    def suggest_concepts(self, vocabulary_name, locale, query: Optional[str] = None):
        """
        Search that returns up to 20 matching concepts. Results are ordered by relevance. The response is smaller than a concept search.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            locale (str): Required. Locale to filter by. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported.

        Returns:
            dict: A dictionary containing the concept suggestions.
        """
        params: Dict[str, Any] = {}
        params_list = [("locale", locale), ("q", query)]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/suggest"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def deprecate_existing_concept(
        self, vocabulary_name, name, username, password, payload=None
    ):
        """
        Deprecates the existing concept. Optionally, a replacement concept can be specified and the replacement must belong to the same vocabulary. Note that if the concept has children they have to be either deprecated or reassigned to the replacement if it's specified. If they should be deprecated it has to be specified explicitly in the parameters.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The password.
            payload (dict): The json object response body.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/deprecate"
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
    def restore_deprecated_concept(
        self,
        vocabulary_name,
        name,
        username,
        password,
        restore_deprecated_children: Optional[bool] = None,
    ):
        """
        Restores the deprecated concept. Its vocabulary cannot be deprecated. If the concept used to have a parent and now it's deprecated it will be replaced with its replacement if exists. Optionally, it can also be specified to restore all the deprecated children of the concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The password.
            restore_deprecated_children (bool): Set to true to restore deprecated concepts.

        Returns:
            string, dict: A message of success or failure of update.
        """
        params: Dict[str, Any] = {}
        params_list = [("restoreDeprecatedChildren", restore_deprecated_children)]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/{name}/deprecate"
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

    def list_all_concept_definitions(self, vocabulary_name, name, language):
        """
        Lists all definitions of the concept.

        Arg:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the concept definitions.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/{name}/definition"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_definition_to_concept(
        self, vocabulary_name, name, username, password, payload
    ):
        """
        Creates a definition and adds it to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            payload (dict): The json response body containing new definition. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned definition if successful.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/definition"
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

    def get_concept_definition(self, vocabulary_name, name, key):
        """
        Gets the definition of the concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the definition.

        Returns:
            dict: A dictionary containing concept definition.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/definition/{key}"
        return hc.get(base_url + self.endpoint + resource)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def update_concept_definition(
        self, vocabulary_name, name, key, username, password, payload
    ):
        """
        Updates a definition that belongs to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the definition.
            username (str): The username.
            password (str): The password.
            payload (dict): The json object response body.

        Returns:
            string, dict: A message of success or failure of update.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/definition/{key}"
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
    def delete_concept_definition(self, vocabulary_name, name, key, username, password):
        """
        Deletes a definition from an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the definition.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/definition/{key}"
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

    def list_all_concept_tags(self, vocabulary_name, name):
        """
        Lists all tags of the concept.

        Arg:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.

        Returns:
            list: A list containing the concept tags.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/tags"
        return hc.get(base_url + self.endpoint + resource)

    # Requires authentication. User must have an account with GBIF with the proper credentials.
    def link_tag_to_concepts(self, vocabulary_name, name, username, password, payload):
        """
        Links a tag to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The password.
            payload (dict): The json object response body.

        Returns:
            string, dict: A message of success or failure of link.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/tags"
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
    def unlink_tag_from_concept(
        self, vocabulary_name, name, tag_name, username, password
    ):
        """
        Unlinks a tag from an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            tag_name (str): The name of the tag.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of untag.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/tags/{tag_name}"
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

    def list_all_concept_labels(self, vocabulary_name, name, language):
        """
        Lists all labels of the concept.

        Arg:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the vocabulary.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the concept labels.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/{name}/label"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_label_to_concept(self, vocabulary_name, name, username, password, payload):
        """
        Creates a label and adds it to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The user's password.
            payload (dict): The json response body containing new definition. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned label if successful.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/label"
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
    def delete_label_from_concept(self, vocabulary_name, name, key, username, password):
        """
        Deletes a label from an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the label.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/label/{key}"
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

    def list_all_alternative_concept_labels(self, vocabulary_name, name, language):
        """
        Lists all alternative labels of the concept.

        Arg:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the alternative concept labels.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/{name}/alternativeLabels"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_alternative_label_to_concept(
        self, vocabulary_name, name, username, password, payload
    ):
        """
        Creates an alternative label and adds it to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The user's password.
            payload (dict): The json response body containing new label. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned alternative label if successful.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/alternativeLabels"
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
    def delete_alternative_label_from_concept(
        self, vocabulary_name, name, key, username, password
    ):
        """
        Deletes an alternative label from an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the label.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/alternativeLabels/{key}"
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

    def list_all_concept_hidden_labels(self, vocabulary_name, name, language):
        """
        Lists all hidden labels of the concept.

        Arg:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by.

        Returns:
            list: A list containing the hidden labels.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/{name}/hiddenLabels"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    # Requires authentication. User must have an account with GBIF.
    def add_hidden_label_to_concept(
        self, vocabulary_name, name, username, password, payload
    ):
        """
        Creates a hidden label and adds it to an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            username (str): The username.
            password (str): The user's password.
            payload (dict): The json response body containing new label. See this endpoint's docs for schema.

        Returns:
            dict, str: Dictionary or string containing an error message or returned hidden label if successful.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/hiddenLabels"
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
    def delete_hidden_label_from_concept(
        self, vocabulary_name, name, key, username, password
    ):
        """
        Deletes a hidden label from an existing concept.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            key (int): The key of the label.
            username (str): The username.
            password (str): The password.

        Returns:
            string, dict: A message of success or failure of delete.
        """
        resource = f"/{vocabulary_name}/concepts/{name}/hiddenLabels/{key}"
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

    def list_all_concepts_from_latest_vocabulary_release(self, vocabulary_name, params):
        """
        Lists all concepts from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            params (dict): The parameters to filter by. See this endpoint's docs for schema.

        Returns:
            dict: A dictionary containing a list of concepts.
        """
        resource = f"/{vocabulary_name}/concepts/latestRelease"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def suggest_concepts_from_latest_vocabulary_release(
        self, vocabulary_name, locale, query: Optional[str] = None
    ):
        """
        Search that returns up to 20 matching concepts from the latest release of the vocabulary. Results are ordered by relevance. The response is smaller than a concept search.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            locale (str): The locale. See this endpoint's docs for available values.
            query (str): Optional. Simple full text search parameter. The value for this parameter can be a simple word or a phrase. Wildcards are not supported

        Returns:
            dict: A dictionary containing suggestions.
        """
        params: Dict[str, Any] = {}
        params_list = [("locale", locale), ("q", query)]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/latestRelease/suggest"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def get_details_of_concept_from_vocabulary_latest_release(
        self,
        vocabulary_name,
        name,
        include_parents: Optional[bool] = None,
        include_children: Optional[bool] = None,
    ):
        """
        Details of a single concept from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            include_parents (bool): Optional.
            include_children (bool): Optional.

        Returns:
            dict: A dictionary containing the concept details.
        """
        params: Dict[str, Any] = {}
        params_list = [
            ("includeParents", include_parents),
            ("includeChildren", include_children),
        ]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/latestRelease/{name}"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def list_definition_of_concept_from_latest_release_of_vocabulary(
        self, vocabulary_name, name, language
    ):
        """
        Lists all definitions of the concept from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by. See this endpoint's docs for available values.

        Returns:
            dict: A dictionary containing the concept definitions.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/latestRelease/{name}/definition"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def list_all_labels_of_concept_from_latest_release_of_vocabulary(
        self, vocabulary_name, name, language
    ):
        """
        Lists all labels of the concept from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by. See this endpoint's docs for available values.

        Returns:
            dict: A dictionary containing the concept labels.
        """
        params = {"lang": language}
        resource = f"/{vocabulary_name}/concepts/latestRelease/{name}/label"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def list_all_alternative_labels_of_concept_from_latest_release_of_vocabulary(
        self,
        vocabulary_name,
        name,
        language,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        Lists all alternative labels of the concept from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            language (str): Languages to filter by. See this endpoint's docs for available values.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.

        Returns:
            dict: A dictionary containing the alternative labels.
        """
        params: Dict[str, Any] = {}
        params_list = [("lang", language), ("limit", limit), ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/latestRelease/{name}/alterntiveLabels"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)

    def list_all_hidden_labels_of_concept_from_latest_release_of_vocabulary(
        self,
        vocabulary_name,
        name,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        Lists all hidden labels of the concept from the latest release of the vocabulary.

        Args:
            vocabulary_name (str): The name of the vocabulary.
            name (str): The name of the concept.
            limit (int): Optional. Controls the number of results in the page. Using too high a value will be overwritten with the default maximum threshold, depending on the service. Sensible defaults are used so this may be omitted.
            offset (int): Optional. Determines the offset for the search results. A limit of 20 and offset of 40 will get the third page of 20 results. Some services have a maximum offset.

        Returns:
            dict: A dictionary containing the hidden labels.
        """
        params: Dict[str, Any] = {}
        params_list = [("limit", limit), ("offset", offset)]
        hc.add_params(params, params_list)
        resource = f"/{vocabulary_name}/concepts/latestRelease/{name}/hiddenLabels"
        return hc.get_with_params(base_url + self.endpoint + resource, params=params)
