from google.oauth2 import service_account
from googleapiclient import discovery
import base64



class DeviceConfig(object):
    service_account_json = "./service.json"

    def __init__(self):
        print("Init")

    def get_client(self):
        """Returns an authorized API client by discovering the IoT API and creating
        a service object using the service account credentials JSON."""
        api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
        api_version = 'v1'
        discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
        service_name = 'cloudiotcore'

        credentials = service_account.Credentials.from_service_account_file(
                self.service_account_json)
        scoped_credentials = credentials.with_scopes(api_scopes)

        discovery_url = '{}?version={}'.format(
                discovery_api, api_version)

        return discovery.build(
                service_name,
                api_version,
                discoveryServiceUrl=discovery_url,
                credentials=scoped_credentials)


    # [START iot_set_device_config]
    def set_config(self,
            project_id, cloud_region, registry_id, device_id,
            version, config):
        print('Set device configuration: {}'.format(config))
        client = self.get_client()
        device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
                project_id, cloud_region, registry_id, device_id)

        config_body = {
            'versionToUpdate': version,
            'binaryData': base64.urlsafe_b64encode(
                    config.encode('utf-8')).decode('ascii')
        }

        return client.projects(
            ).locations().registries(
            ).devices().modifyCloudToDeviceConfig(
            name=device_path, body=config_body).execute()
    # [END iot_set_device_config]
