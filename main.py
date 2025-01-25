import csv
import random
from faker import Faker


from google.cloud import bigquery
client = bigquery.Client()


faker = Faker()

incident_types = ["Medical", "Fire", "Accident", "Crime"]
severity_levels = [1, 2, 3, 4, 5]

def generate_incident():
    return {
        "incident_id": faker.uuid4(),
        "timestamp": faker.date_time_this_year(),
        "caller_name": faker.name(),
        "incident_type": random.choice(incident_types),
        "severity_level": random.choice(severity_levels),
        "lat": faker.latitude(),
        "lng": faker.longitude(),
    }

def save_incidents_to_csv(num_rows=100, filename="mock_incidents.csv"):
    """Generate mock incidents and save to CSV."""
    fieldnames = [
        "incident_id", "timestamp", "caller_name", 
        "incident_type", "severity_level", "lat", "lng"
    ]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for _ in range(num_rows):
            writer.writerow(generate_incident())
    
    print(f"Saved {num_rows} rows of mock data to {filename}")

save_incidents_to_csv(1000, "mock_incidents.csv")


def insert_mock_data_into_bq(project_id, dataset_id, table_id, num_rows=1000):
    client = bigquery.Client(project=project_id)

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # Make an API request to get table
    
    rows_to_insert = []
    for _ in range(num_rows):
        incident = generate_incident()
        # Convert your dict to a tuple matching the table schema
        # or keep it as a dict if using the 'insert_rows_json' method
        rows_to_insert.append({
            "incident_id": incident["incident_id"],
            "timestamp": incident["timestamp"].isoformat(),  # if it's a datetime
            "caller_name": incident["caller_name"],
            "incident_type": incident["incident_type"],
            "severity_level": incident["severity_level"],
            "lat": incident["lat"],
            "lng": incident["lng"]
        })

    # Use insert_rows_json if you have a dictionary that matches the table schema
    errors = client.insert_rows_json(table, rows_to_insert)
    if errors == []:
        print(f"Successfully inserted {num_rows} rows into {table_id}.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

# Example usage:
insert_mock_data_into_bq(
    project_id="concise-memory-448916-t4",
    dataset_id="concise-memory-448916-t4.real_time_location_data",
    table_id="concise-memory-448916-t4.real_time_location_data.call-id",
    num_rows=1000
)