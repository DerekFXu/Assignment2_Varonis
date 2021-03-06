import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime
import urllib.parse


#Credientials to access key vault
credential = DefaultAzureCredential(managed_identity_client_id = "efdd8d32-9ad9-427a-ba4d-12ef2517c8f5")
client = SecretClient(
    vault_url="https://varonisassignmentkv1-dfx.vault.azure.net/",
    credential=credential
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #Tries to get secret, returns generic error if secret doesn't exist
        try:
            secret = client.get_secret(name)
        except Exception as e:
            return func.HttpResponse("Generic Error")
        #Parses URL for keyvault name
        vault_url = secret.properties.vault_url
        u = urllib.parse.urlparse(vault_url)
        vault_name = u.netloc.removesuffix('.vault.azure.net')
        #Converts created_on to string
        secret_time = secret.properties.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        return func.HttpResponse(f"Name of the Key Vault: {vault_name}\nName of the Key Vault Secret: {secret.name}\nCreation Date Of Secret: {secret_time}\nValue Of Secret: {secret.value}")