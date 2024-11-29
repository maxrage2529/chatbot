

def import_documents_from_bigquery(
        project_id, location, data_store_id, bigquery_dataset, bigquery_table
):
    """
    Imports documents from a BigQuery table into a Discovery Engine data store.

    Args:
        project_id (str): The Google Cloud project ID.
        location (str): The location of the data store (e.g., 'global', 'eu', 'us').
        data_store_id (str): The ID of the data store.
        bigquery_dataset (str): The BigQuery dataset ID.
        bigquery_table (str): The BigQuery table ID.

    Returns:
        response: The response from the import operation.
        metadata: Metadata information about the import operation.
    """
    # Configure API endpoint based on location
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # Build the parent branch path
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    # Prepare the request
    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        bigquery_source=discoveryengine.BigQuerySource(
            project_id=project_id,
            dataset_id=bigquery_dataset,
            table_id=bigquery_table,
            data_schema="custom",
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Execute the request
    operation = client.import_documents(request=request)
    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # Extract metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Return the response and metadata
    return response, metadata


# Example usage
if __name__ == "__main__":
    import os
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/gcpServiceAccounts/chatbot-poc-436512-40e4b95f4ae7.json"
    # Replace these variables with your values
    project_id = "chatbot-poc-436512"
    location = "eu"  # or "global", "us", etc.
    data_store_id = "eu-datastore_1732013310429"
    bigquery_dataset = "faq_dataset"
    bigquery_table = "new_table_with_id"

    try:
        response, metadata = import_documents_from_bigquery(
            project_id, location, data_store_id, bigquery_dataset, bigquery_table
        )
        print("Import operation completed successfully.")
        print("Response:", response)
        print("Metadata:", metadata)
    except Exception as e:
        print(f"Error occurred during import: {e}")
