import csv
import random
from faker import Faker
from google.cloud import bigquery
from decimal import Decimal
from google.cloud.exceptions import NotFound  # To handle table not found

faker = Faker()

incident_types = ["Medical", "Fire", "Accident", "Crime"]
severity_levels = [1, 2, 3, 4, 5]

def generate_incident():
    return {
        "call_id": faker.basic_phone_number(),
        "timestamp": faker.date_time_this_year(),
        "caller_name": faker.name(),
        "incident_type": random.choice(incident_types),
        "severity_level": random.choice(severity_levels),
        "lat": float(faker.latitude()),  # Convert Decimal to float
        "lng": float(faker.longitude())  # Convert Decimal to float
    }

def make_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    else:
        return obj


def save_incidents_to_csv(num_rows=100, filename="mock_incidents.csv"):
    """Generate mock incidents and save to CSV."""
    fieldnames = [
        "call_id", "timestamp", "caller_name", 
        "incident_type", "severity_level", "lat", "lng"
    ]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for _ in range(num_rows):
            writer.writerow(generate_incident())
    
    print(f"Saved {num_rows} rows of mock data to {filename}")


def create_bq_table(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)

    # Define the schema based on your data
    schema = [
        bigquery.SchemaField("call_id", "STRING"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("caller_name", "STRING"),
        bigquery.SchemaField("incident_type", "STRING"),
        bigquery.SchemaField("severity_level", "INTEGER"),
        bigquery.SchemaField("lat", "FLOAT"),
        bigquery.SchemaField("lng", "FLOAT")
    ]
    
    # Reference to the dataset and table
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    try:
        # Attempt to get the table, if it exists, delete it first
        client.get_table(table_ref)  # Check if the table exists
        print(f"Table {table_id} already exists. Deleting and recreating.")
        client.delete_table(table_ref)  # Delete the table
    except NotFound:
        print(f"Table {table_id} does not exist. Creating a new one.")

    # Create the table (or re-create it after deletion)
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)  # API request to create the table
    print(f"Table {table_id} created in dataset {dataset_id}.")


def insert_mock_data_into_bq(project_id, dataset_id, table_id, num_rows=100):
    client = bigquery.Client(project=project_id)

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Create the table (or re-create it after deletion)
    create_bq_table(project_id, dataset_id, table_id)

    rows_to_insert = []
    for _ in range(num_rows):
        incident = generate_incident()
        # Convert values to serializable format before inserting
        rows_to_insert.append(make_serializable({
            "call_id": incident["call_id"],
            "timestamp": incident["timestamp"].isoformat(),  # Ensure it's a valid datetime format
            "caller_name": incident["caller_name"],
            "incident_type": incident["incident_type"],
            "severity_level": incident["severity_level"],
            "lat": incident["lat"],
            "lng": incident["lng"]
        }))

    # Use insert_rows_json if you have a dictionary that matches the table schema
    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors == []:
        print(f"Successfully inserted {num_rows} rows into {table_id}.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")


# Example usage:
insert_mock_data_into_bq(
    project_id="concise-memory-448916-t4",
    dataset_id="real_time_location_data",
    table_id="call_id",  # Specify the table name here
    num_rows=100
)
