import datetime
import os
from pathlib import Path
import sys
import os.path

from lib.client import get_lifelogs
from lib.env import load_env
from lib.tz import get_local_timezone

import time

# Add the parent directory to the path so we can import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import .env files
root_dir = Path(__file__).resolve().parent.parent
load_env(root_dir)

def export_data(lifelogs):
    for lifelog in lifelogs:
        print(lifelog.get("markdown"), end="\n\n")

def main():
    timezone = sys.argv[1] if len(sys.argv) > 1 else None
    
    if timezone is None:
        timezone = get_local_timezone()
    
    # NOTE: Increase limit to get more lifelogs
    lifelogs = get_lifelogs(timezone=timezone, limit=1)
    
    # Export data
    export_data(lifelogs)

if __name__ == "__main__":
    main() 
