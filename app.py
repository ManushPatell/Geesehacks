from flask import Flask, jsonify
from google.cloud import bigquery
import random
from flask_cors import CORS  # <-- Import CORS

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

# Initialize BigQuery client
client = bigquery.Client()

# Define your BigQuery table
project_id = "concise-memory-448916-t4"
dataset_id = "real_time_location_data"
table_id = "call_id"

@app.route('/', methods=['GET'])
def get_incident_data():
    try:
        # Query BigQuery table
        query = f"""
        SELECT * 
        FROM `{project_id}.{dataset_id}.{table_id}`
        ORDER BY timestamp DESC
        LIMIT 1
        """
        query_job = client.query(query)
        results = [dict(row) for row in query_job]
        if not results:
            return jsonify({"status": "error", "message": "No data found"}), 404

        incident = results[0]

        # Add random nearby locations for units based on the incident type
        base_lat = random.uniform(43.45, 43.50)  # Waterloo latitude range
        base_lng = random.uniform(-80.55, -80.50)  # Waterloo longitude range

        # Generate random units' locations
        units = []
        for _ in range(3):  # Three units
            units.append({
                "lat": base_lat + random.uniform(-0.005, 0.005),
                "lng": base_lng + random.uniform(-0.005, 0.005),
                "type": random.choice(["police", "ambulance", "firetruck"])
            })

        # Add generated units to the incident data
        incident["units"] = units

        return jsonify(incident), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
