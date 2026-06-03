import os
import json
import glob
import sys
from collections import defaultdict

def run_comparison():
    # Find all downloaded metadata.json files from the CI artifacts
    search_path = os.path.join("all_results", "**", "metadata.json")
    metadata_files = glob.glob(search_path, recursive=True)
    
    if not metadata_files:
        print("No metadata files found to compare!")
        sys.exit(1)
        
    print(f"Found {len(metadata_files)} environments to compare.\n")
    
    # Dictionary to group environments by Python version (e.g., "3.10", "3.11")
    # Format: {"3.10": [{"os": "Windows...", "data": {...}}, ...]}
    grouped_by_py_version = defaultdict(list)

    for filepath in metadata_files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Get OS info and Python version from the first item recorded
        first_key = list(data.keys())[0]
        full_py_version = data[first_key]["python"] # e.g. "3.10.12"
        os_name = data[first_key]["os"]             # e.g. "Linux-5.15..."
        
        # We only care about major.minor grouping (e.g., "3.10", "3.11")
        py_major_minor = ".".join(full_py_version.split(".")[:2])
        
        grouped_by_py_version[py_major_minor].append({
            "file": filepath,
            "os": os_name,
            "data": data
        })
            
    mismatch_found = False

    # Now, compare OSes ONLY within the same Python version
    for py_ver, environments in grouped_by_py_version.items():
        print(f"\n========================================")
        print(f" Comparing across OSes for Python {py_ver}")
        print(f"========================================")

        if len(environments) < 2:
            print(f"  Only 1 OS found for Python {py_ver}. Nothing to compare.")
            continue

        # Use the first OS in the group as our "Reference/Baseline"
        reference_env = environments[0]
        ref_data = reference_env["data"]
        print(f"  Reference OS: {reference_env['os']} (File: {reference_env['file']})")

        # Compare every other OS against the reference
        for test_env in environments[1:]:
            test_data = test_env["data"]
            print(f"\n  -> Comparing against: {test_env['os']} (File: {test_env['file']})")
            
            for object_key, ref_info in ref_data.items():
                if object_key not in test_data:
                    print(f"    [MISSING] Key '{object_key}' is missing in {test_env['os']}")
                    mismatch_found = True
                    continue
                    
                test_info = test_data[object_key]
                
                ref_hash = ref_info["sha256"]
                test_hash = test_info["sha256"]
                
                # The Critical Check: Does the hash match across the OSes for this Python version?
                if ref_hash != test_hash:
                    print(f"    [MISMATCH] Object '{object_key}' serialized differently!")
                    print(f"      Ref ({reference_env['os']}): {ref_hash}")
                    print(f"      Test ({test_env['os']}): {test_hash}")
                    mismatch_found = True
                else:
                    print(f"    [PASS] '{object_key}' hashes match.")

    if mismatch_found:
        print("\n[FAIL] Found cross-OS serialization mismatches within the same Python version.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] Pickle serialized bytes are perfectly identical across all tested OSes for every Python version.")

if __name__ == '__main__':
    run_comparison()