
from score_pair import score_pair, PLAN, FieldComparison

# Test 1: Similar customer records
person1 = {
    "name": "Rahul Sharma",
    "email": "rahul@gmail.com",
    "phone": "9876543210",
    "date_of_birth": "12-06-2004",
    "pin_code": "560001",
    "city": "Bengaluru",
}

person2 = {
    "name": "Rahul Sharam",
    "email": "rahul@gmail.com",
    "phone": "+91 98765-43210",
    "date_of_birth": "12/06/2004",
    "pin_code": "560001",
    "city": "Bengaluru",
}

result = score_pair(person1, person2, PLAN)

assert 0.0 <= result.confidence <= 1.0
assert result.field_scores["email"] == 1.0
assert result.field_scores["phone"] == 1.0
assert result.field_scores["date_of_birth"] == 1.0
assert result.field_scores["pin_code"] == 1.0
assert result.field_scores["city"] == 1.0

print("Test 1 passed: Similar records")


# Test 2: Missing values
person3 = {
    "name": "Rahul Sharma",
    "email": "",
    "phone": None,
    "date_of_birth": "",
    "pin_code": "560001",
    "city": "Bengaluru",
}

person4 = {
    "name": "Rahul Sharma",
    "email": None,
    "phone": "",
    "date_of_birth": None,
    "pin_code": "560001",
    "city": "Bengaluru",
}

missing_result = score_pair(person3, person4, PLAN)

assert missing_result.confidence == 1.0
assert "email" not in missing_result.field_scores
assert "phone" not in missing_result.field_scores
assert "date_of_birth" not in missing_result.field_scores

print("Test 2 passed: Missing values are skipped")


# Test 3: Nothing to compare
empty_plan = [
    FieldComparison("email", "edit_distance", 0.20),
    FieldComparison("phone", "normalized_phone", 0.20),
]

empty_result = score_pair(person3, person4, empty_plan)

assert empty_result.confidence == 0.0
assert empty_result.field_scores == {}

print("Test 3 passed: No comparable fields")


print("\nAll tests passed successfully!")
