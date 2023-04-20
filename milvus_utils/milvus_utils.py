import requests
import json

class MilvusUtils:
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def create_collection(self, collection_name, schema):
        url = f"{self.endpoint_url}/api/v1/collection"
        data = {
            "collection_name": collection_name,
            "schema": schema
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print('Status code:', response.status_code)
            return True
        else:
            print("Error creating collection:", response.json())
            return False
        
    def check_collection_existence(self, collection_name):
        url = f"{self.endpoint_url}/api/v1/collection/existence"
        data = {
            "collection_name": collection_name
        }
        response = requests.get(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            if result['value']:
                print(f"Collection {collection_name} exists!")
                return True
            else:
                print(f"Collection {collection_name} does not exist.")
                return False
        else:
            print("Error checking collection existence:", response.json())
            return False
        
    def get_collections_list(self):
        url = f"{self.endpoint_url}/api/v1/collections"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error getting collections:", response.json())
            return False
    def get_collection_details(self,collection_name):
        url = f"{self.endpoint_url}/api/v1/collection"
        data = {
            "collection_name": collection_name
        }
        response = requests.get(url, headers=self.headers,data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error getting collection details:", response.json())
            return False
        
    def get_collection_details(self,collection_name):
        url = f"{self.endpoint_url}/api/v1/collection"
        data = {
            "collection_name": collection_name
        }
        response = requests.delete(url, headers=self.headers,data=json.dumps(data))
        
        if response.status_code == 200:
            print(f'Collection {collection_name} successfully deleted!')
            return True
        else:
            print("Error deleting collection details:", response.json())
            return False
        

    def load_collection(self,collection_name):
        url = f'{self.endpoint_url}/api/v1/collection/load'
        data = {'collection_name': collection_name}
        
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.ok:
            print(f'Collection {collection_name} successfully loaded!')
            return True
        else:
            print('Error occurred while loading collection.')
            print(response.status_code)
            return False
        
    def release_collection(self,collection_name):
        url = f'{self.endpoint_url}/api/v1/collection/load'
        data = {'collection_name': collection_name}
        
        response = requests.delete(url, headers=self.headers, data=json.dumps(data))
        
        if response.ok:
            print(f'Collection {collection_name} successfully released!')
            return True
        else:
            print('Error occurred while releasing collection.')
            print(response.status_code)
            return False
        
    def insert_data(self, collection_name, data, num_rows):
        url = f"{self.endpoint_url}/api/v1/entities"
        data = {
            "collection_name": collection_name,
            "fields_data": data,
            "num_rows": num_rows
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print('Status code:', response.status_code)
            print('Data successfully inserted', response.json())
            return True
        else:
            print("Error creating collection:", response.json())
            return False
    def build_index(self, collection_name, field_name, params):
        url = f"{self.endpoint_url}/api/v1/index"
        data = {
            "collection_name": collection_name,
            "field_name": field_name,
            "extra_params": params
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print('Status code:', response.status_code)
            print('Index successfully built!', response.json())
            return True
        else:
            print("Error building index", response.json())
            return False
        
    def similarity_search(self, collection_name, output_fields, params, vectors):
        url = f"{self.endpoint_url}/api/v1/search"
        data = {
            "collection_name": collection_name,
            "output_fields": output_fields,
            "search_params": params,
            "vectors": vectors,
            "dsl_type": 1
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print('Status code:', response.status_code)
            print('search results', response.json())
            return True
        else:
            print('Status code:', response.status_code)
            print("error occured while searching:", response.json())
            return False
