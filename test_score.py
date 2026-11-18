from score_pair import score_pair, PLAN

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

print("Confidence:", result.confidence)
print("Algorithm:", result.algorithm)
print("Field scores:", result.field_scores)
print("\n--- Missing Value Test ---")

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

print("Confidence:", missing_result.confidence)
print("Algorithm:", missing_result.algorithm)
print("Field scores:", missing_result.field_scores)