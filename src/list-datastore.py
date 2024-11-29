#
#
# def list_datastores(project_id, location):
#     """
#     Lists all DataStores in the specified project and location.
#
#     Args:
#         project_id (str): The GCP project ID.
#         location (str): The location of the DataStore (e.g., 'global').
#
#     Returns:
#         List of DataStores.
#     """
#     client = discoveryengine_v1.DataStoreServiceClient()
#     parent = f"projects/{project_id}/locations/{location}"
#
#     print(f"Listing DataStores in project {project_id}, location {location}...")
#     response = client.list_data_stores(parent=parent)
#
#     datastores = []
#     for datastore in response:
#         datastores.append(datastore)
#         print(f"- DataStore ID: {datastore.name}")
#
#     return datastores
#
# if __name__ == "__main__":
#
#     import os
#     from google.cloud import discoveryengine_v1
#     # Replace with your project ID and location
#     project_id = "chatbot-poc-436512"
#     location = "global"
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/gcpServiceAccounts/chatbot-poc-436512-d088c910b850.json"
#
#     datastores = list_datastores(project_id, location)
#     if not datastores:
#         print("No DataStores found.")
#
# from google.cloud import discoveryengine_v1
# from google.api_core.client_options import ClientOptions

def list_eu_datastores(project_id, location="eu"):
    """
    Lists all DataStores in the specified project and EU location using the correct endpoint.

    Args:
        project_id (str): The GCP project ID.
        location (str): The location of the DataStore, default is 'eu'.

    Returns:
        List of DataStores.
    """
    # Specify the correct API endpoint for EU
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DataStoreServiceClient(client_options=client_options)

    # The full resource name of the collection
    # e.g. projects/{project}/locations/{location}/collections/default_collection
    parent = client.collection_path(
        project=project_id,
        location=location,
        collection="default_collection",
    )

    print(f"Listing DataStores in project {project_id}, location {location}...")
    response = client.list_data_stores(parent=parent)

    datastores = []
    for datastore in response:
        datastores.append(datastore)
        print(f"- DataStore ID: {datastore.name}")

    return datastores


if __name__ == "__main__":

    import os
    from google.cloud import discoveryengine
    from google.api_core.client_options import ClientOptions
    # Replace with your project ID and location
    project_id = "chatbot-poc-436512"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/gcpServiceAccounts/chatbot-poc-436512-40e4b95f4ae7.json"

    datastores = list_eu_datastores(project_id)
    if not datastores:
        print("No DataStores found.")