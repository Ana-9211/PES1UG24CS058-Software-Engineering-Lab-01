# Requirements Traceability Matrix

**Smart Lab Equipment & Slot Reservation Portal** – covers SRS-SLP-01, SADS-SLP-01, TP-SLP-01.

Chain: **Requirement → Use Case → Architecture Component → Design element → Test Case**.
ID prefixes: FR / NFR / SEC-OBJ / SEC-REQ (SRS), UC (SRS §5), C-nn (Architecture §4), SD-nn / API-n / DD-nn (Design), TC-nn (Test Plan).
API numbers refer to the endpoint catalogue in Design §9.1.

## 1. Requirement-level matrix

| Requirement | Use case | Components | Design elements | Test cases |
|---|---|---|---|---|
| FR-001 | UC-02, UC-03, UC-10 | C-01, C-02, C-05, C-11, C-12 | SD-01 (parts 1–2); API-2, API-3, API-8; DD-01, DD-02, DD-03 | TC-01, TC-02, TC-03, TC-04, TC-17, TC-21, TC-24 |
| FR-002 | UC-03, UC-09 | C-05, C-06, C-11 | SD-01 (alt A1); API-8 | TC-01, TC-05, TC-13 |
| FR-003 | UC-04 | C-05, C-11 | API-11; DD-05 | TC-06, TC-07, TC-23 |
| FR-004 | UC-06, UC-12 | C-08, C-10, C-11 | SD-02; API-12, API-13; DD-07 | TC-08, TC-09, TC-22 |
| FR-005 | UC-08 | C-07, C-10, C-11 | API-4, API-5, API-6; DD-06, DD-07 | TC-10, TC-21, TC-22, TC-25 |
| FR-006 | UC-01 | C-03, C-11 | API-1 | TC-11, TC-19, TC-20 |
| FR-007 | UC-05 | C-05, C-11 | API-9, API-10; DD-08 | TC-12 |
| FR-008 | UC-07 | C-06, C-10, C-11 | API-7; DD-07 | TC-13, TC-22 |
| FR-009 | UC-11 | C-05, C-09 | SD-01; DD-04 | TC-14 |
| FR-010 | UC-03 | C-05, C-11 | SD-01; DD-02 | TC-15 |
| NFR-001 | UC-03 | C-02, C-05, C-11 | SD-01; DD-02, DD-04 | TC-16 |
| NFR-002 | UC-06, UC-07, UC-08 | C-02, C-03, C-04 | SD-02; DD-08 | TC-18, TC-19 |
| NFR-003 | UC-03 | C-05, C-11, C-12 | SD-01; DD-02 | TC-17 |

## 2. Security traceability

SEC-OBJ → SEC-REQ → component / control → design mechanism → validation test.

| Objective | Requirement | Component(s) | Design mechanism | Test case |
|---|---|---|---|---|
| SEC-OBJ-01 | SEC-REQ-01 | C-04, C-02 | Role table, deny by default, 403 `FORBIDDEN_ROLE`; SD-02 | TC-18 |
| SEC-OBJ-01 | SEC-REQ-02 | C-03 | Idle-time check, 401 `SESSION_EXPIRED`; SD-02 | TC-19 |
| SEC-OBJ-01 | SEC-REQ-04 | C-02, C-03 | Session required on all but API-1; 401 `AUTHENTICATION_REQUIRED` | TC-20 |
| SEC-OBJ-01 | SEC-REQ-07 | C-03 | Generic login error; credentials stored only as a verifier and never logged | TC-11, TC-20 |
| SEC-OBJ-02 | SEC-REQ-01, SEC-REQ-05 | C-04, C-02, C-11 | Validation + parameterised access; DD-02 | TC-18, TC-21 |
| SEC-OBJ-03 | SEC-REQ-03 | C-05, C-04 | Ownership check; history filtered by session user; DD-08 | TC-12, TC-23 |
| SEC-OBJ-04 | SEC-REQ-06 | C-10 | Audit record in the same transaction; DD-07 | TC-22 |

## 3. Use case coverage

| Use case | Requirements | Components | Diagram / design | Test cases |
|---|---|---|---|---|
| UC-01 Login / Authenticate | FR-006, SEC-REQ-02, SEC-REQ-04, SEC-REQ-07 | C-01, C-02, C-03 | API-1 | TC-11, TC-19, TC-20 |
| UC-02 View Equipment Availability | FR-001 | C-01, C-02, C-05 | API-2, API-3 | TC-01, TC-24 |
| UC-03 Reserve Equipment Slot | FR-001, FR-002, FR-009, FR-010, NFR-001, NFR-003 | C-02, C-05, C-06, C-09, C-11 | **SD-01 (parts 1–2)**, API-8 | TC-01…TC-05, TC-14…TC-17 |
| UC-04 Cancel Reservation | FR-003, SEC-REQ-03 | C-05 | API-11 | TC-06, TC-07, TC-23 |
| UC-05 View Reservation History | FR-007, SEC-REQ-03 | C-05 | API-9, API-10 | TC-12 |
| UC-06 Return Equipment | FR-004, NFR-002, SEC-REQ-01, SEC-REQ-06 | C-02, C-04, C-08, C-10 | **SD-02**, API-12, API-13 | TC-08, TC-09, TC-18, TC-22 |
| UC-07 Update Calibration Status | FR-008, SEC-REQ-01, SEC-REQ-06 | C-06, C-10 | API-7 | TC-13, TC-18, TC-22 |
| UC-08 Manage Equipment Inventory | FR-005, SEC-REQ-01, SEC-REQ-05, SEC-REQ-06 | C-07, C-10 | API-4…API-6 | TC-10, TC-18, TC-21, TC-22, TC-25 |
| UC-09 Verify Calibration Status | FR-002 | C-06 | SD-01 | TC-05, TC-13 |
| UC-10 Generate Reservation Token | FR-001 | C-05 | SD-01; DD-01 | TC-01 |
| UC-11 Send Confirmation Notification | FR-009 | C-09 | SD-01; DD-04 | TC-14 |
| UC-12 Apply Late-Return Penalty | FR-004 | C-08 | SD-02 (opt fragment) | TC-08, TC-09 |

## 4. Component coverage (no orphan components)

| Component | Requirements it serves |
|---|---|
| C-01 Web Client | FR-001, FR-003, FR-007, FR-009 (display), EIR-01 |
| C-02 API Layer | SEC-REQ-04, SEC-REQ-05, NFR-001, NFR-002 |
| C-03 Authentication & Session Service | FR-006, NFR-002, SEC-REQ-02, SEC-REQ-04, SEC-REQ-07 |
| C-04 Access Control Guard | NFR-002, SEC-REQ-01, SEC-REQ-03 |
| C-05 Reservation Service | FR-001, FR-003, FR-007, FR-010, NFR-001, NFR-003, SEC-REQ-03 |
| C-06 Calibration Service | FR-002, FR-008 |
| C-07 Inventory Service | FR-005 |
| C-08 Return & Penalty Service | FR-004 |
| C-09 Notification Adapter | FR-009 |
| C-10 Audit Logger | SEC-REQ-06 |
| C-11 Data Access Layer | NFR-001, NFR-003, SEC-REQ-05 |
| C-12 Relational Database | NFR-003 |

## 5. Test case → requirement (reverse)

| Test | Requirement(s) | Type |
|---|---|---|
| TC-01 | FR-001, FR-002 | Functional |
| TC-02 | FR-001 | Functional / boundary |
| TC-03 | FR-001 | Functional / boundary |
| TC-04 | FR-001 | Functional / negative |
| TC-05 | FR-002 | Functional / negative |
| TC-06 | FR-003 | Functional |
| TC-07 | FR-003 | Functional / boundary |
| TC-08 | FR-004 | Functional |
| TC-09 | FR-004 | Functional / boundary |
| TC-10 | FR-005 | Functional |
| TC-11 | FR-006, SEC-REQ-07 | Functional / security |
| TC-12 | FR-007, SEC-REQ-03 | Functional / security |
| TC-13 | FR-008, FR-002 | Functional |
| TC-14 | FR-009 | Functional / fault injection |
| TC-15 | FR-010 | Functional / negative |
| TC-16 | NFR-001 | Performance |
| TC-17 | NFR-003, FR-001 | Concurrency |
| TC-18 | NFR-002, SEC-REQ-01 | Security |
| TC-19 | NFR-002, SEC-REQ-02, FR-006 | Security / boundary |
| TC-20 | SEC-REQ-04, SEC-REQ-07, FR-006 | Security |
| TC-21 | SEC-REQ-05, FR-001, FR-005 | Security / negative |
| TC-22 | SEC-REQ-06, FR-004, FR-005, FR-008 | Security |
| TC-23 | SEC-REQ-03, FR-003 | Security / negative |
| TC-24 | FR-001 | Functional |
| TC-25 | FR-005 | Functional / negative |

All 25 tests currently have status *Not Executed*.
