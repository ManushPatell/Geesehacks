from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)

# Initialize BigQuery client
client = bigquery.Client()

# Define your BigQuery table
project_id = "concise-memory-448916-t4"
dataset_id = "real_time_location_data"
table_id = "call_id"

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        # Query BigQuery table
        query = f"""
        SELECT * 
        FROM `{project_id}.{dataset_id}.{table_id}`
        ORDER BY timestamp DESC
        LIMIT 10
        """
        query_job = client.query(query)
        results = [dict(row) for row in query_job]

        # Return the results as JSON
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
