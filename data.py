from google.cloud import bigquery
import json
from decimal import Decimal

# Initialize BigQuery client
client = bigquery.Client()

# Define dataset and table
project_id = "concise-memory-448916"
dataset_id = "real_time_location_data"
table_id = "call_id"  # Use proper BigQuery naming conventions
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# Function to convert data for JSON serialization
def convert_for_json_serialization(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# Function to upload fake data into BigQuery
def upload_data_to_bigquery(data):
    try:
        # Convert JSON data to Python dictionary
        rows_to_insert = json.loads(data, parse_float=Decimal)  # Parse numbers as Decimal
        # Serialize the rows to handle any non-serializable objects
        rows_to_insert = json.loads(json.dumps(rows_to_insert, default=convert_for_json_serialization))
        
        # Insert the data into BigQuery
        errors = client.insert_rows_json(table_ref, rows_to_insert)
        if not errors:
            print("Data successfully uploaded.")
        else:
            print(f"Error uploading data: {errors}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example of fake data in JSON format
fake_data = json.dumps([
    {
        "call_id": "R1",
        "timestamp": "2025-01-25T08:00:00Z",
        "location": "Location 1",
        "incident_type": "Fire",
        "responding_units": ["Unit A"],  # Use an array for repeated fields
        "status": "In Progress"
    }
])

# Call the function to upload the fake data
upload_data_to_bigquery(fake_data)
