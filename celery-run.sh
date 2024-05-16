#!/bin/bash
cd sample
echo "Initializing Celery..."
celery -A sample worker -l INFO
echo ====================================