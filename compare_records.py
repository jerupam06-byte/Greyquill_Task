import csv
import sys
from score_pair import score_pair, PLAN

# Read customer records from the CSV file
with open("customer-records.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    records = list(reader)

# Check whether two record IDs were provided
if len(sys.argv) != 3:
    print("Usage: python compare_records.py <ID1> <ID2>")
    sys.exit(1)

id1 = sys.argv[1]
id2 = sys.argv[2]

# Find the records using their IDs
person1 = next((r for r in records if r["record_id"] == id1), None)
person2 = next((r for r in records if r["record_id"] == id2), None)

# Check whether both IDs exist
if person1 is None or person2 is None:
    print("Record ID not found. Please check the IDs.")
    sys.exit(1)

# Compare the records
result = score_pair(person1, person2, PLAN)

print("\n--- Comparison Result ---")
print("Confidence:", round(result.confidence * 100, 2), "%")
print("Algorithm:", result.algorithm)
print("Field scores:", result.field_scores)