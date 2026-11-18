# Greyquill Record Matching

## Overview

This project compares two customer records and calculates a matching confidence score based on the similarity of their available fields.

The goal is to identify whether two records may belong to the same person by considering multiple attributes rather than relying on a single field.

## Scoring Approach

Each field is compared separately and assigned a similarity score between 0 and 1.

The final confidence score is calculated using a weighted average of the fields that can be compared. Missing or blank values are skipped and do not contribute to the score.

The implementation supports:

- Name similarity using string similarity, word-order handling, and initials.
- Email similarity using edit distance.
- Phone number normalization to handle formatting differences.
- Date comparison across supported date formats.
- Exact matching for city and PIN code.

The final confidence score ranges from 0 to 1. A higher score indicates greater similarity between the two records, but it does not guarantee that they belong to the same person.

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
- Name comparison uses similarity heuristics and edit distance, not a dedicated phonetic matching library.
- Date formats that are ambiguous may be interpreted according to the first matching format in the supported list.
- Matching confidence indicates similarity, not proof of identity.

## AI Usage

ChatGPT was used to help understand the assignment, plan the implementation, review code, troubleshoot issues, and improve documentation. The code was tested locally using the provided dataset and test scripts.