import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime
from requests.exceptions import RequestException

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
        try:
            secret = client.get_secret(name)
            vault_name_first = secret.properties.vault_url.replace("https://", "")
            vault_name = vault_name_first.replace(".vault.azure.net/", "")
            secret_time = secret.properties.created_on.strftime("%m/%d/%Y, %H:%M:%S")
            return func.HttpResponse(f"Name of the Key Vault: {vault_name}\nName of the Key Vault Secret: {secret.name}\nCreation Date Of Secret: {secret_time}\nValue Of Secret: {secret.value}\n{vault_name_first}\n{secret.properties.vault_url}")
        except RequestException as e:
            return func.HttpResponse(f"Sorry this is not a valid secret name, error: {e}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
