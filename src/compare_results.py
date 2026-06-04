import argparse
import glob
import json
import os
import sys
from collections import defaultdict


def normalize_python_version(full_version):
    return ".".join(full_version.split(".")[:2])


def find_metadata_files(search_path):
    metadata_files = glob.glob(search_path, recursive=True)
    if not metadata_files:
        print("No metadata files found to compare!")
        sys.exit(1)

    print(f"Found {len(metadata_files)} environments to compare.\n")
    return metadata_files


def build_grouped_environments(metadata_files, compare_by):
    grouped = defaultdict(list)

    for filepath in metadata_files:
        with open(filepath, 'r') as f:
            data = json.load(f)

        first_key = list(data.keys())[0]
        full_py_version = data[first_key]["python"]
        os_name = data[first_key]["os"]
        py_major_minor = normalize_python_version(full_py_version)

        entry = {
            "file": filepath,
            "python": py_major_minor,
            "full_python": full_py_version,
            "os": os_name,
            "data": data,
        }

        if compare_by == "python":
            grouped[os_name].append(entry)
        else:
            grouped[py_major_minor].append(entry)

    return grouped


def compare_grouped_environments(grouped, compare_by):
    mismatch_found = False

    for group_name, environments in grouped.items():
        if compare_by == "python":
            print(f"\n========================================")
            print(f" Comparing across Python versions for OS: {group_name}")
            print(f"========================================")
            reference_label = "Reference Python"
            compare_label = "Python"
        else:
            print(f"\n========================================")
            print(f" Comparing across OSes for Python: {group_name}")
            print(f"========================================")
            reference_label = "Reference OS"
            compare_label = "OS"

        if len(environments) < 2:
            print(f"  Only 1 entry found for {group_name}. Nothing to compare.")
            continue

        reference_env = environments[0]
        ref_data = reference_env["data"]

        if compare_by == "python":
            reference_value = reference_env["python"]
        else:
            reference_value = reference_env["os"]

        print(f"  {reference_label}: {reference_value} (File: {reference_env['file']})")

        for test_env in environments[1:]:
            test_data = test_env["data"]
            current_label = test_env["python"] if compare_by == "python" else test_env["os"]
            print(f"\n  -> Comparing against {compare_label} {current_label} (File: {test_env['file']})")

            for object_key, ref_info in ref_data.items():
                if object_key not in test_data:
                    print(f"    [MISSING] Key '{object_key}' is missing in {current_label}")
                    mismatch_found = True
                    continue

                test_info = test_data[object_key]
                ref_hash = ref_info["sha256"]
                test_hash = test_info["sha256"]

                if ref_hash != test_hash:
                    print(f"    [MISMATCH] Object '{object_key}' serialized differently!")
                    print(f"      Ref ({reference_value}): {ref_hash}")
                    print(f"      Test ({current_label}): {test_hash}")
                    mismatch_found = True
                else:
                    print(f"    [PASS] '{object_key}' hashes match.")

    return mismatch_found


def run_comparison(compare_by="os"):
    search_path = os.path.join("all_results", "**", "metadata.json")
    metadata_files = find_metadata_files(search_path)
    grouped = build_grouped_environments(metadata_files, compare_by)
    mismatch_found = compare_grouped_environments(grouped, compare_by)

    if mismatch_found:
        print("\n[FAIL] Found serialization mismatches in the selected comparison mode.")
        sys.exit(1)

    if compare_by == "python":
        print("\n[SUCCESS] Pickle serialized bytes are identical across all Python versions within each OS.")
    else:
        print("\n[SUCCESS] Pickle serialized bytes are perfectly identical across all tested OSes for every Python version.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare pickle metadata across CI artifacts")
    parser.add_argument("--compare-by", choices=["os", "python"], default="os",
                        help="Compare across OSes (os) or across Python versions within the same OS (python).")
    args = parser.parse_args()
    run_comparison(compare_by=args.compare_by)