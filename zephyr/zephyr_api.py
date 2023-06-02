import json
import requests



class Zephyr:

    def __init__(self, token, project_key):
        self.url = "https://api.zephyrscale.smartbear.com"
        self.token = token
        self. project_key =  project_key

    def get_cycles(self):
        url = f"{self.url}/v2/testcycles?project_key={self.project_key}&startAt=50000&maxResults=4000"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        return requests.request("GET", url, headers=headers, data=payload)

    def get_cycle_by_id_or_key(self, cycle_id):
        url = f"{self.url}/v2/testcycles/{cycle_id}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        return requests.request("GET", url, headers=headers, data=payload)
    

    def create_cycle(self, cycle_name, folder_id):
        url = f"{self.url}/v2/testcycles"

        payload = json.dumps({
            "projectKey": "FIQ",
            "name": cycle_name,
            "folderId": folder_id
        })
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        return requests.request("POST", url, headers=headers, data=payload)

    def update_cycle(self, cycle_id=int, cycle_key=str, cycle_name=str, folder_id=int, release_version=str):
        url = f"{self.url}/v2/testcycles/{cycle_key}"

        payload = json.dumps({
            "id": cycle_id,
            "key": cycle_key,
            "name": cycle_name,
            "project": {
                "id": 113251,
                "self": f"{self.url}/v2/projects/113251"
            },
            "jiraProjectVersion": None,
            "status": {
                "id": 2080807,
                "self": f"{self.url}/v2/statuses/2080807"
            },
            "folder": {
                "id": folder_id,
                "self": f"{self.url}/v2/folders/{str(folder_id)}"
            },
            "description": None,
            "plannedStartDate": None,
            "plannedEndDate": None,
            "owner": None,
            "customFields": {
                "Build NO": None,
                "Deployment Type": None,
                "Release Version": release_version
            },
            "links": {}
        })
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        return requests.request("PUT", url, headers=headers, data=payload)

    def get_test_cycle_folders(self):
        url = f"{self.url}/v2/folders?folderType=TEST_CYCLE&projectKey={self.project_key}&maxResults=1000"
 
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}',
        }

        return requests.request("GET", url, headers=headers, data=payload)

    def create_test_cycle_folder(self, folder_name, parent_folder_name=None):
        url = f"{self.url}/v2/folders"

        payload = json.dumps({
            "parentId": parent_folder_name if parent_folder_name else None,
            "name": folder_name,
            "projectKey": self.project_key,
            "folderType": "TEST_CYCLE"
        })
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        return requests.request("POST", url, headers=headers, data=payload)


    def get_folder(self, folder_name, parent_id):
        q = self.get_test_cycle_folders().json()
        for e in q['values']:
            if e['name'].strip().lower() == folder_name.strip().lower() and e['parentId'] == parent_id:
                return  e
            return False
        

    def post_junit_results(self, file_name, file_data, test_cycle_id=None):
        url = f"{self.url}/v2/automations/executions/junit?projectKey={self.project_key}&autoCreateTestCases=false"

        if test_cycle_id is not None:
            test_cycle = json.loads(self.get_cycle_by_id(test_cycle_id).text)
        payload = {}
        files = [
            ('file', (file_name, file_data, 'text/xml'))
        ]
        headers = {
            'Authorization': f'Bearer {self.token}',
        }

        return requests.request("POST", url, headers=headers, data=payload, files=files)