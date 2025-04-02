from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

def get_gmail_tools(google_creds_path="./creds/credentials.json"):
    ''' 
    returns a list of Gmail tools that can be used in Langchain
    '''

    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'

    creds_path_prefix = google_creds_path.replace("credentials.json", "")
    token_file_path = creds_path_prefix + "token.json" 

    credentials = get_gmail_credentials(
        token_file=token_file_path,
        scopes=["https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/gmail.compose",
                "https://www.googleapis.com/auth/gmail.addons.current.action.compose"],
        client_secrets_file=google_creds_path,
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    tools = toolkit.get_tools()
    return tools