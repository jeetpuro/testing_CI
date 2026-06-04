import os
import json
import glob
import sys
from collections import defaultdict


def normalize_python_version(full_version):
    return ".".join(full_version.split(".")[:2])


def run_comparison():
    search_path = os.path.join("all_results", "**", "metadata.json")
    metadata_files = glob.glob(search_path, recursive=True)

    if not metadata_files:
        print("No metadata files found to compare!")
        sys.exit(1)

    print(f"Found {len(metadata_files)} environments to compare.\n")

    grouped_by_os = defaultdict(list)

    for filepath in metadata_files:
        with open(filepath, 'r') as f:
            data = json.load(f)

        first_key = list(data.keys())[0]
        full_py_version = data[first_key]["python"]
        os_name = data[first_key]["os"]
        py_major_minor = normalize_python_version(full_py_version)

        grouped_by_os[os_name].append({
            "file": filepath,
            "python": py_major_minor,
            "full_python": full_py_version,
            "os": os_name,
            "data": data,
        })

    mismatch_found = False

    for os_name, environments in grouped_by_os.items():
        print(f"\n========================================")
        print(f" Comparing across Python versions for OS: {os_name}")
        print(f"========================================")

        if len(environments) < 2:
            print(f"  Only 1 Python version found for OS {os_name}. Nothing to compare.")
            continue

        reference_env = environments[0]
        ref_data = reference_env["data"]
        print(f"  Reference Python: {reference_env['python']} (File: {reference_env['file']})")

        for test_env in environments[1:]:
            test_data = test_env["data"]
            print(f"\n  -> Comparing against Python {test_env['python']} (File: {test_env['file']})")

            for object_key, ref_info in ref_data.items():
                if object_key not in test_data:
                    print(f"    [MISSING] Key '{object_key}' is missing in Python {test_env['python']}")
                    mismatch_found = True
                    continue

                test_info = test_data[object_key]
                ref_hash = ref_info["sha256"]
                test_hash = test_info["sha256"]

                if ref_hash != test_hash:
                    print(f"    [MISMATCH] Object '{object_key}' serialized differently!")
                    print(f"      Ref (Python {reference_env['python']}): {ref_hash}")
                    print(f"      Test (Python {test_env['python']}): {test_hash}")
                    mismatch_found = True
                else:
                    print(f"    [PASS] '{object_key}' hashes match.")

    if mismatch_found:
        print("\n[FAIL] Found cross-Python serialization mismatches within the same OS.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] Pickle serialized bytes are identical across all Python versions within each OS.")


if __name__ == '__main__':
    run_comparison()