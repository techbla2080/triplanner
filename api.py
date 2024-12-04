# Standard library imports
from datetime import datetime
import json
from threading import Thread, Lock
from uuid import uuid4
import logging
import os
import traceback
from clean_result import clean_result

# Third-party imports
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dateutil.parser import parse

# Local imports
from main import TripCrew

app = Flask(__name__)

# Configure CORS properly for all routes
CORS(app, 
     resources={
         r"/*": {
             "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }
     })

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

import random

# In-memory dictionary to store job statuses and results
jobs = {}
jobs_lock = Lock()

def kickoff_trip_planning(job_id, location, cities, date_range, interests):
    """Run the trip planning process in a separate thread."""
    try:
        logging.info(f"Starting trip planning for job {job_id}")
        logging.debug(f"Input parameters: location={location}, cities={cities}, "
                     f"date_range={date_range}, interests={interests}")

        trip_crew = TripCrew(location, cities, date_range, interests)
        result = trip_crew.run()
        
        # Log the raw result for debugging
        logging.debug(f"Raw result from TripCrew.run(): {result}")

        # Ensure result is JSON serializable
        if result is None:
            result = {"message": "No result generated"}
        
        # Try to convert result to string if it's not already
        if not isinstance(result, (str, dict)):
            result = str(result)

        # Clean the result before storing
        cleaned_result = clean_result(result)

        with jobs_lock:
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = cleaned_result
            jobs[job_id]["events"].append({
                "timestamp": datetime.now().isoformat(),
                "data": "Trip planning completed successfully"
            })

        logging.info(f"Successfully completed trip planning for job {job_id}")

    except Exception as e:
        error_msg = f"Error in trip planning: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        
        with jobs_lock:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["result"] = {"error": str(e)}
            jobs[job_id]["events"].append({
                "timestamp": datetime.now().isoformat(),
                "data": f"Error occurred: {str(e)}"
            })

@app.route('/api/crew', methods=['POST'])
def plan_trip():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json
        logging.info(f"Received trip planning request: {data}")

        # Validate required fields
        required_fields = ['location', 'cities', 'date_range', 'interests']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
            if not isinstance(data[field], str):
                return jsonify({"error": f"{field} must be a string"}), 400

        # Validate date range format
        try:
            start_date, end_date = data['date_range'].split(" to ")
            parse(start_date)
            parse(end_date)
        except (ValueError, AttributeError) as e:
            return jsonify({
                "error": "Invalid date range format. Expected 'DD/MM/YYYY to DD/MM/YYYY'"
            }), 400

        job_id = str(uuid4())
        
        with jobs_lock:
            jobs[job_id] = {
                "status": "in_progress",
                "result": None,
                "events": [{
                    "timestamp": datetime.now().isoformat(),
                    "data": "Job started"
                }]
            }

        thread = Thread(
            target=kickoff_trip_planning,
            args=(job_id, data['location'], data['cities'], 
                  data['date_range'], data['interests'])
        )
        thread.start()

        return jsonify({
            "job_id": job_id,
            "status": "Trip planning started",
            "message": "Successfully initiated trip planning"
        }), 202

    except Exception as e:
        error_msg = f"Error in plan_trip: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        return jsonify({"error": str(e)}), 500

@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    if request.method == 'OPTIONS':
        return '', 204

    try:
        with jobs_lock:
            job = jobs.get(job_id)

            if job is None:
                logging.warning(f"Job {job_id} not found")
                return jsonify({"error": "Job not found"}), 404

            logging.debug(f"Current job state for {job_id}: {job}")

            response_data = {
                "job_id": job_id,
                "status": job["status"],
                "result": job["result"],  # Result is already cleaned when stored
                "events": job["events"]
            }

            logging.debug(f"Sending response for job {job_id}: {response_data}")
            return jsonify(response_data)

    except Exception as e:
        error_msg = f"Error in get_status: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host='0.0.0.0', port=port)