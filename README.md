# Greyquill Record Matching

## Overview

This project compares two customer records and calculates a matching confidence score based on the similarity of their available fields.

The goal is to identify whether two records may belong to the same person while considering multiple attributes rather than relying on a single field.

## Scoring Approach

Each field is compared separately and assigned a similarity score between 0 and 1.

The final confidence score is calculated using the weighted average of the comparable fields. Missing or blank values are ignored so that they do not negatively affect the result.

The implementation supports:
- Exact matching for fields such as email, city, and PIN code.
- Phone number normalization to handle differences in formatting.
- Date comparison across different date formats.
- Name similarity using string similarity, edit distance, and word-order handling.

The final confidence score ranges from 0 to 1, where a higher score indicates a stronger potential match.

## How to Run

### Requirements
- Python 3.10 or later
- No external packages required

### Compare Two Records

Run the following command from the project folder:

    python compare_records.py <ID1> <ID2>

Replace `<ID1>` and `<ID2>` with the record IDs you want to compare.

Example:

    python compare_records.py R0001 R0002

The program displays:
- Matching confidence percentage
- Matching algorithm used
- Individual field similarity scores

## Missing Values

If a field is empty or missing in either record, it is excluded from the comparison. Only fields with values available on both sides contribute to the final confidence score.

If no comparable fields are available, the confidence score is 0.0.

## Limitations

- Similar names do not necessarily mean the records belong to the same person.
- The name comparison uses similarity heuristics and edit distance, not a dedicated phonetic matching library.
- Matching confidence is an indication of similarity, not proof of identity.