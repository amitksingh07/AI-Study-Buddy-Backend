import sys
import os

# Add the root directory to the python path so 'app' can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
