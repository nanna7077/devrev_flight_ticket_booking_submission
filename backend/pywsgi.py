# Run the application through this file to get better performace and concurrent requests

from waitress import serve
from app import app

serve(
    app,
    host="0.0.0.0", 
    port=5000
)