#!/bin/bash

# Activate the Conda environment
source activate finance

# Start the Airflow webserver in the background
airflow webserver --port 8080 &

# Start the Airflow scheduler in the background
airflow scheduler &

