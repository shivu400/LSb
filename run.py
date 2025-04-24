import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(__file__))

from src.main import main

if __name__ == "__main__":
    exit(main())