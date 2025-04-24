import logging
import os
from datetime import datetime

def setup_logging():
    """
    Setup logging configuration
    """
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Configure logging
    log_file = f'results/stego_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )