import csv
from itertools import combinations
from score_pair import score_pair, PLAN

# Read the customer records locally
with open("customer-records.csv", "r", newline="", encoding="utf-8") as file:
    records = list(csv.DictReader(file))

candidates = []

# Compare every pair of records
for person1, person2 in combinations(records, 2):
    result = score_pair(person1, person2, PLAN)

    name_score = result.field_scores.get("name")

    # Look for similar names but lower overall matching confidence
    if name_score is not None and name_score >= 0.65 and result.confidence < 0.75:
        candidates.append({
            "id1": person1["record_id"],
            "id2": person2["record_id"],
            "name_score": name_score,
            "confidence": result.confidence,
        })

# Sort by name similarity (highest first)
candidates.sort(key=lambda item: (-item["name_score"], item["confidence"]))

print(f"Total records checked: {len(records)}")
print(f"Potential candidate pairs found: {len(candidates)}")
print("\n--- Top Candidate Pairs ---")

for candidate in candidates[:20]:
    print(
        f"{candidate['id1']} vs {candidate['id2']} | "
        f"Name Similarity: {candidate['name_score']:.2%} | "
        f"Overall Confidence: {candidate['confidence']:.2%}"
    )