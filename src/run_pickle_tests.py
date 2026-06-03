import hashlib
import pickle
import platform
import sys
import os
import json
from fixtures import TEST_DATA

def pickle_and_hash(obj, protocol):
    data = pickle.dumps(obj, protocol=protocol)
    digest = hashlib.sha256(data).hexdigest()
    return {
        "sha256": digest,
        "bytes_len": len(data),
        "python": platform.python_version(),
        "os": platform.system(),
        "protocol": protocol,
    }

def main():
    protocol = 4
    results_dir = "results" # kanske fel path
    
    # Create the results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    summary = {}

    for key, data in TEST_DATA.items():
        if key == "image_path":
            continue # Skip writing the raw image path
            
        # 1. Get hash and metadata
        info = pickle_and_hash(data, protocol)
        summary[key] = info
        
        # 2. Write the actual pickle file to the results folder
        pickle_path = os.path.join(results_dir, f"{key}.pickle")
        with open(pickle_path, 'wb') as f:
            pickle.dump(data, f, protocol=protocol)
            
    # Write a summary metadata file
    summary_path = os.path.join(results_dir, "metadata.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=4)
        
    print(f"Successfully generated pickle files in '{results_dir}/'")

if __name__ == "__main__":
    main()