import requests
from requests.exceptions import HTTPError, Timeout, RequestException, JSONDecodeError
from requests.auth import HTTPBasicAuth
from typing import Dict
from time import sleep
from functools import wraps

def retry(retries=3, delay=1, backoff=2):
    """
    Retry decorator with exponential backoff.
    
    Args:
        retries (int): Number of retries before giving up.
        delay (int): Initial delay between retries in seconds.
        backoff (int): Multiplier by which the delay is increased after each retry.
        
    Returns:
        function: A decorator to retry the wrapped function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts, current_delay = 0, delay
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except (HTTPError, Timeout, RequestException) as e:
                    print(f"Error: {e}. Retrying in {current_delay} seconds...")
                    sleep(current_delay)
                    attempts += 1
                    current_delay *= backoff
            return {"error": "Max retries exceeded"}
        return wrapper
    return decorator

def handle_error(response, error_message):
    """
    Helper function to handle HTTP errors and exceptions.
    
    Args:
        response (requests.Response): The HTTP response object.
        error_message (str): The error message to include.
        
    Returns:
        dict: A dictionary containing error information.
    """
    try:
        error_info = response.json().get("message", None)
    except Exception:
        error_info = None
    return {"error": error_message, "message": error_info}

@retry()
def get(url, headers=None, payload=None):
    """
    Make an HTTP request to the specified URL with optional headers and payload.
    
    Args:
        url (str): The URL of the API endpoint.
        headers (dict, optional): Headers to be included in the request.
        payload (dict, optional): The payload to be sent in the request body.
        
    Returns:
        dict: A dictionary containing the response data or error information.
    """
    try:
        if payload is not None:
            response = requests.post(url, headers=headers, json=payload)
        else:
            response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def get_with_params(url, params, headers=None):
    """
    Make a request to an API if the API call requires params.
    
    Args:
        url (str): The url of the API.
        params (dict): The params to be included in the request.
    
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def get_for_content(url, headers=None):
    """
    Make a request to an API if the API call returns content other than in JSON format.
    
    Args:
        url (str): The url of the API.
    
    Returns:
        string: Text in any format containing either the response data or an error message.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def get_for_content_with_params(url, params, headers=None):
    """
    Make a request to an API if the API call returns content other than in JSON format.
    
    Args:
        url (str): The url of the API.
    
    Returns:
        string: Text in any format containing either the response data or an error message.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.content
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def post_with_data(url, data):
    """
    Make a request to an API using the POST method.
    
    Args:
        url (str): The url of the API.
        data (dict): The data to be included in the request.
    
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def post_with_json(url, json):
    """
    Make a request to an API using the POST method.
    
    Args:
        url (str): The url of the API.
        json (dict): The data to be included in the request.
    
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        response = requests.post(url, json=json)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def post_with_auth_and_json(url, headers=None, auth=None, json=None):
    """
    Make a request to an API using the POST method that requires authentication and passes data with the json parameter.
    
    Args:
        url (str): The URL of the API.
        headers (dict): The headers.
        auth (tuple): A tuple containing the username and password for APIs with endpoints that require authentication.
        json (dict): The data to be included in the request.
    
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        if auth is not None:
            response = requests.post(url, auth=auth, json=json)
            response.raise_for_status()
            return response.json()
        else:
            response = requests.post(url, headers=headers, json=json)
            response.raise_for_status()
            return response.json()
    except HTTPError as http_err:
        if response.status_code == 401:
            return {"error": "Unauthorized: Check your API credentials."}
        elif response.status_code == 403:
            return {"error": "Forbidden: You do not have permission to access this resource."}
        else:
            return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@retry()
def put_with_auth_and_json(url, headers=None, auth=None, json=None):
    """
    Make a request to an API using the POST method that requires authentication and passes data with the json parameter.
    
    Args:
        url (str): The URL of the API.
        headers (dict): The headers.
        auth (tuple): A tuple containing the username and password for APIs with endpoints that require authentication.
        json (dict): The data to be included in the request.
    
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        if auth is not None:
            response = requests.put(url, auth=auth, json=json)
            response.raise_for_status()
            return response.json()
        else:
            response = requests.put(url, headers=headers, json=json)
            response.raise_for_status()
            return response.json()
    except HTTPError as http_err:
        if response.status_code == 401:
            return {"error": "Unauthorized: Check your API credentials."}
        elif response.status_code == 403:
            return {"error": "Forbidden: You do not have permission to access this resource."}
        else:
            return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

def try_get_except_json_decode_err(base_url, endpoint, resource):
    """
    Simplifies certain API calls in the package that use a try/except block dealing with JSON Decoding error.
    
    Args:
        base_url (str): The base URL of the API.
        endpoint (str): The endpoint of the API.
        resource (str): The specific resource being fetched.
        
    Returns:
        dict: A dictionary containing the requested data.
    """
    try:
        return get(base_url+endpoint+resource)
    except JSONDecodeError:
        response = get_for_content(base_url+endpoint+resource)
        decoded_response = response.decode("utf-8")
        return {"Error": f"{decoded_response}"}

@retry()
def delete_with_auth(url, headers=None, auth=None):
    """
    Make a request to an API using the DELETE method that requires authentication.
    
    Args:
        url (str): The URL of the API.
        auth (tuple): A tuple containing the username and password for APIs with endpoints that require authentication.
         
    Returns:
        dict: A dictionary containing either the response data or an error message.
    """
    try:
        if auth is not None:
            response = requests.delete(url, auth=auth)
            status = response.status_code
            return status
            
        else:
            response = requests.delete(url, headers=headers)
            status = response.status_code
            return status
            
    except HTTPError as http_err:
        if response.status_code == 401:
            return {"error": "Unauthorized: Check your API credentials."}
        elif response.status_code == 403:
            return {"error": "Forbidden: You do not have permission to access this resource."}
        else:
            return handle_error(response, f"HTTP error occurred: {http_err}")
    except Timeout:
        return {"error": "Request timed out."}
    except RequestException as req_err:
        return {"error": f"Request exception occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}
        
def get_oauth_headers(client_id: str, client_secret: str, token_url: str) -> Dict[str, str]:
    """
    Retrieves OAuth 2.0 access token and returns headers for authenticated requests.
    
    Args:
        client_id (str): The client ID provided by the OAuth provider.
        client_secret (str): The client secret provided by the OAuth provider.
        token_url (str): The URL to obtain the OAuth token.
    
    Returns:
        Dict[str, str]: Headers including the OAuth 2.0 access token.
    """
    try:
        # Request for the access token
        response = requests.post(
            token_url,
            auth=HTTPBasicAuth(client_id, client_secret),
            data={'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens.get('access_token')
        
        if not access_token:
            raise Exception("Failed to obtain access token.")
        
        # Return the headers with the access token
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")

  
def add_params(params, params_list):
    """
    Adds parameters to the params dictionary if their values are not None.

    Args:
        params (dict): The dictionary to add parameters to.
        params_list (list of tuples): Each tuple contains (original_param_name, new_param_name).
    """
    for original_param_name, new_param_name in params_list:
        if new_param_name is not None:
            params[original_param_name] = new_param_name