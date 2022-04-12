"""
IOT Library
Author:  Maj Adrian A. de Freitas
Description:  Provides Simple Methods to Upload and Download
              data from the iot backend
"""
import requests, json
from datetime import datetime

# This points to the website where the database and webservices are loaded
# Sorry that the name doesn't make sense . . . it's all temporary stuff for now
upload_url = "https://iot.dfcs-cloud.net/upload_data.php"
get_data_url = "https://iot.dfcs-cloud.net/get_data.php"
update_url = "https://iot.dfcs-cloud.net/update_data.php"

# This is needed so that the website doesn't immediately reject the request
post_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def upload_data(data_dictionary, device_id, api_key=12345):
    """ Uploads Data to the Database
        
        Parameters
        ----------
        data_dictionary : dictionary
            A dictionary that contains the information you want to store.  Must have the 'type' key specified.
        device_id : string
            A string value used to uniquely identify this device
        api_key : string
            A string value that represents the API Key (provided by the server)

        Returns
        -------
        string
            a string containing the response from the server
    
    """

    # Creates the Headers / POST Information
    post_data = {}
    post_data['api_key'] = api_key
    post_data['device_id'] = device_id
    post_data['data'] = json.dumps(data_dictionary)
    
    # This performs an HTTP POST operation
    response = requests.post(upload_url, headers=post_headers, data = post_data)

    # TODO:  For now, just return the response
    # Eventually, we should look at the response code
    return response.text


def get_data(data_type, api_key=12345, device_ids = [],
             time_start = datetime(1900, 1, 1, 0, 0, 0),
             time_end = datetime.now(),
             limit = 10):
    """ Retrieves Data from the Database
        
        Parameters
        ----------
        data_type : string
            A value that represents the type of data to get from the database.
            You can think of it as the name of the table
        api_key : string
            A string value that represents the API Key (provided by the server)
        device_ids : list, optional
            A list of specific devices you want to get data from.  If not specified,
            the function will get values from every device
        time_start & time_end : DateTime, optional
            Specifies the date range to get data from
        limit : integer, optional
            Specifies the max # of records to return.  Default is 10.
            
        Returns
        -------
        string
            a string containing the response from the server 
    """
    
    post_data = {}
    post_data['type'] = data_type
    post_data['api_key'] = api_key
    post_data['time_start'] = time_start
    post_data['time_end'] = time_end
    post_data['limit'] = limit
    post_data['device_ids'] = device_ids
    
    # This performs an HTTP POST operation
    response = requests.post(get_data_url, headers=post_headers, data=post_data)
    
    # TODO:  For now, just return the response
    # Eventually, we should look at the response code
    return response.text



def update_data(data_dictionary, device_id, api_key, table_name, row_id):
    """ Uploads Data to the Database
        
        Parameters
        ----------
        data_dictionary : dictionary
            A dictionary that contains the information you want to store.  Must have the 'type' key specified.
        device_id : string
            A string value used to uniquely identify this device
        api_key : string
            A string value that represents the API Key (provided by the server)

        Returns
        -------
        string
            a string containing the response from the server
    
    """

    # Creates the Headers / POST Information
    post_data = {}
    post_data['device_id'] = device_id
    post_data['table_name'] = table_name
    if row_id.isnumeric():
        post_data['row_id'] = int(row_id)
    else:
        post_data['row_id'] = row_id
    post_data['api_key'] = api_key
    post_data['data'] = json.dumps(data_dictionary)
    
    # This performs an HTTP POST operation
    response = requests.post(update_url, headers=post_headers, data = post_data)

    # TODO:  For now, just return the response
    # Eventually, we should look at the response code
    return response.text