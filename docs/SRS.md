# Software Requirements Specification (SRS)

**Project:** Smart City Waste Management System
**Team:** Sasyak Subudhi (PES1UG24AM256), Shriya Vasundhara Singh (PES1UG24AM269), Shreya Yashodhara Singh (PES1UG24AM266), Shruti Choudhary (PES1UG24AM271)
**Course:** Software Engineering, PES University

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements of a Smart City Waste Management System that monitors the fill level of public waste bins, raises alerts for bins that need emptying, plans collection routes for garbage trucks, and produces summary reports for city administrators.

### 1.2 Scope
The system receives fill-level readings (simulated sensor data), classifies each bin, alerts operators, assigns due bins to trucks and summarises city-wide status. It does not control physical hardware.

### 1.3 Definitions
| Term | Meaning |
|---|---|
| Fill level | Percentage (0-100) of a bin's capacity currently used |
| OK | Fill level below 70% |
| NEARLY_FULL | Fill level 70-89% |
| FULL | Fill level 90% or more |
| Threshold | Fill level at or above which a bin is due for collection (default 70%) |

### 1.4 Users
- **City administrator:** registers bins, views reports.
- **Collection supervisor:** reviews alerts, plans truck routes.

## 2. Overall description

- **Product perspective:** standalone Python application (package `waste_mgmt`).
- **Assumptions:** sensor readings are supplied as integers 0-100; every truck can serve `capacity_bins` bins per trip.
- **Constraints:** Python 3.10+, no external runtime dependencies.

## 3. Functional requirements

| ID | Requirement | Module |
|---|---|---|
| FR-1 | The system shall let an administrator add, retrieve, list and remove bins. Duplicate bin IDs shall be rejected. | bins |
| FR-2 | The system shall accept a fill-level reading for a bin and reject values outside 0-100. | bins |
| FR-3 | The system shall classify each bin as OK, NEARLY_FULL or FULL using the boundaries in 1.3. | bins |
| FR-4 | The system shall generate a WARNING alert for NEARLY_FULL bins and a CRITICAL alert for FULL bins, listing CRITICAL first. | alerts |
| FR-5 | The system shall select bins at or above a configurable threshold, fullest first, and assign them to trucks without exceeding truck capacity. | routing |
| FR-6 | The system shall report bins that could not be assigned because the fleet is full. | routing |
| FR-7 | The system shall mark bins as emptied once a truck completes its route. | routing |
| FR-8 | The system shall report total bins, average fill level, a count per status and average fill per waste type. | reports |

## 4. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-1 | Invalid input shall raise a clear error rather than silently corrupt data. |
| NFR-2 | The full automated test suite shall run in under 10 seconds. |
| NFR-3 | Statement and branch coverage shall each be at least 80%. |
| NFR-4 | Code shall be maintained in Git with changes merged only via reviewed pull requests passing CI. |

## 5. Traceability to tests

| Requirement | Test cases |
|---|---|
| FR-1 | TC-BIN-06..10, SYS-01, SYS-04 |
| FR-2 | TC-BIN-03, SYS-02 |
| FR-3 | TC-BIN-04 |
| FR-4 | TC-AL-01..05, SYS-01, SYS-02 |
| FR-5 | TC-RT-01..05, SYS-01 |
| FR-6 | TC-RT-05, SYS-03 |
| FR-7 | TC-RT-08, SYS-01 |
| FR-8 | TC-RP-01..06 |
