---
title: Test Plan
subtitle: Smart Lab Equipment & Slot Reservation Portal
---

# Test Plan

**Smart Lab Equipment & Slot Reservation Portal**

| | |
|---|---|
| Document ID | TP-SLP-01 |
| Version | 1.0 (Mini-Project Part-1) |
| Author | Anagha N (PES1UG24CS058) |
| Format | Organised in an IEEE 829-style test-plan structure as requested by the assignment (sections 1–5, §5.1 Security Validation); no formal standards-compliance is claimed |
| Inputs | `SRS.md` (SRS-SLP-01), `Software_Architecture_and_Design.md`, `traceability/Requirements_Traceability.md` |

> **Execution status.** The repository contains requirements and design documents only; the portal is not implemented yet. **No test case has been executed.** Every test case below has status *Not Executed* and an empty *Actual Result*. Results are to be filled in when an implementation exists.

## 1. Introduction

### 1.1 Purpose
This plan defines how the requirements of SRS-SLP-01 (FR-001…FR-010, NFR-001…NFR-003, SEC-REQ-01…SEC-REQ-07) will be verified, and contains the test cases that cover them.

### 1.2 Scope
Verification of the Smart Lab Equipment & Slot Reservation Portal at the system level through its HTTP API and web UI. Component-level (unit) testing is planned by the implementer once the technology stack is chosen and is not enumerated here.

### 1.3 Definitions
Terms and ID prefixes are those of the SRS §1.3. Additional: **Test clock** – a controllable time source used to create boundary situations (A-T2); **Stub** – a simulated Notification System.

### 1.4 References
SRS (`SRS.md`); Architecture & Design (`Software_Architecture_and_Design.md`); IEEE Std 829; assignment `SE_Mini_Project_Delivereables_Part-1.pdf`.

### 1.5 Overview
§2–§4 define what is tested; §5 the approach (including §5.1 Security Validation); §6–§11 environment, data, tools, roles, criteria and risks; §12 the test cases; §13 the traceability matrix.

## 2. Test Items

| Item | Description | Source |
|---|---|---|
| TI-1 | Smart Lab Equipment & Slot Reservation Portal – web UI and HTTP/JSON API (all components C-01…C-12) | SRS, Design §9 |
| TI-2 | Interface to the Notification System (verified against a stub) | SRS EIR-02 |
| TI-3 | Persistent store behaviour relevant to locking and audit records | SRS EIR-03 |

Version under test: *to be recorded at execution time* (no build exists yet).

## 3. Features to be Tested

| Feature | Requirement | Use case | Test cases |
|---|---|---|---|
| View availability and reserve a slot (clauses a–e: availability, duration, horizon, overlap, token) | FR-001 | UC-02, UC-03, UC-10 | TC-01, TC-02, TC-03, TC-04, TC-17, TC-21, TC-24 |
| Calibration check before confirmation | FR-002 | UC-03, UC-09 | TC-01, TC-05, TC-13 |
| Cancellation and 5-second slot release | FR-003 | UC-04 | TC-06, TC-07, TC-23 |
| Return recording and late-return flag | FR-004 | UC-06, UC-12 | TC-08, TC-09, TC-22 |
| Equipment inventory add / update / remove | FR-005 | UC-08 | TC-10, TC-21, TC-22, TC-25 |
| Login and role assignment | FR-006 | UC-01 | TC-11, TC-19, TC-20 |
| Own reservation history | FR-007 | UC-05 | TC-12 |
| Calibration status update | FR-008 | UC-07 | TC-13, TC-22 |
| Confirmation display and notification | FR-009 | UC-11 | TC-14 |
| Student self-overlap rejection | FR-010 | UC-03 | TC-15 |
| Reservation latency ≤ 200 ms | NFR-001 | UC-03 | TC-16 |
| RBAC and 30-minute session expiry | NFR-002 | UC-06/07/08 | TC-18, TC-19 |
| No double booking under concurrency | NFR-003 | UC-03 | TC-17 |
| Security requirements | SEC-REQ-01…07 | – | see §5.1 |

## 4. Features Not to be Tested

| Item | Reason |
|---|---|
| User registration, password reset | Out of scope of the SRS (A-11). |
| Actual email / push delivery by the real Notification System | External system; only the request made by the portal is verified (stub, A-12). |
| Browser/device compatibility, visual layout, accessibility | No requirement specifies them (SRS §3.3 EIR-01). |
| Capacity beyond the A-03 test load, availability %, long-term endurance | No such requirement exists; none are invented. |
| Transport encryption (HTTPS) and password-hash algorithm | Deployment / implementation choices (A-10); to be reviewed as configuration, not by a functional test. |
| Penalties other than the late-return flag | Not defined in Lab 1. |
| Technician-initiated cancellation | Out of scope (A-09). |

## 5. Approach

Testing is black-box and requirement-driven. Each test case traces to at least one SRS requirement. Test design techniques: equivalence partitioning (valid / invalid roles, calibration states), boundary-value analysis (120 / 121 min, 7 days, 60 / 59 min before start, 29 / 31 min idle, return at slot end), negative testing and fault injection (notification stub failure), concurrency testing, and security testing as in §5.1.

Test levels: system test through the HTTP API (preferred for repeatability) with a small set of UI-level checks for the confirmation screen and role-specific menus (TC-01, TC-11, TC-14).

| Area | Approach | Test cases |
|---|---|---|
| Functional | Scripted request/response checks with state verification in the data store; success and alternate flows A1–A4 of UC-03. | TC-01 … TC-15, TC-24, TC-25 |
| Non-functional – performance | Fire the A-03 load at the reservation endpoint and record per-request duration; verify against 200 ms. | TC-16 |
| Non-functional – concurrency / integrity | Submit N identical-slot requests simultaneously; verify exactly one confirmation and one stored record. | TC-17 |
| Non-functional – access control, session | See §5.1. | TC-18, TC-19 |
| Security | See §5.1. | TC-11, 12, 18 – 23 |

### 5.1 Security Validation

Objective: demonstrate that each security requirement of SRS §4.2 is enforced, and therefore that each security objective of §4.1 is preserved.

| Security objective | Security requirement | Control (Architecture §7) | Validation method | Test case | Pass criterion |
|---|---|---|---|---|---|
| SEC-OBJ-01 Authenticated & authorized access, SEC-OBJ-02 Integrity | SEC-REQ-01 | C-04 Access Control Guard | Call every technician-only endpoint with a Student session | TC-18 | HTTP 403 each time; data unchanged |
| SEC-OBJ-01 | SEC-REQ-02 | C-03 Authentication & Session Service | Use a session idle for 29 and 31 minutes (test clock) | TC-19 | 29 min → success; 31 min → HTTP 401 |
| SEC-OBJ-01 | SEC-REQ-04 | C-02 security filter, C-03 | Call every protected endpoint with no token and with a malformed token | TC-20 | HTTP 401 for every endpoint; no data returned |
| SEC-OBJ-01 | SEC-REQ-07 | C-03 Authentication & Session Service; C-10 / §11.4 logging rules | Compare login error text for unknown user vs. wrong password; inspect logs, responses and stored credentials | TC-11, TC-20 | Identical error text; no plaintext credential in log, response or store |
| SEC-OBJ-03 Confidentiality of own data | SEC-REQ-03 | C-04 + C-05 ownership check | Student B reads / cancels Student A's reservation | TC-12, TC-23 | HTTP 403; no content leaked; reservation unchanged |
| SEC-OBJ-02 Integrity | SEC-REQ-05 | C-02 input validation, C-11 parameterised access | Boundary, malformed and injection-style inputs | TC-21 | HTTP 400/422; no data change; tables intact |
| SEC-OBJ-04 Accountability | SEC-REQ-06 | C-10 Audit Logger | Perform privileged actions, then read audit records | TC-22 | One record per action with user, role, action, target, timestamp |

Security test notes: tests use only the system under test in the lab environment; no third-party service is attacked. Injection inputs are limited to a short set of standard strings (e.g. `' OR '1'='1`, `'; DROP TABLE equipment;--`).

### 5.2 Entry, Exit and Suspension Criteria
- **Entry:** build deployed to the test environment; test data loaded (§7); Notification stub and test clock available.
- **Exit:** all test cases executed; all High-priority requirements' tests passed; no open defect that violates a requirement acceptance criterion.
- **Suspension:** environment unavailable, or a blocking defect in login / reservation prevents further testing; resume after fix and re-run of TC-01 and TC-11.

### 5.3 Pass / Fail Criteria
A test case *passes* when every expected result in its table is observed. It *fails* if any is not. Statuses: *Not Executed*, *Pass*, *Fail*, *Blocked*. Performance (TC-16) passes only if **every** measured request is ≤ 200 ms (the SRS gives no percentile).

## 6. Test Environment
| Item | Specification |
|---|---|
| Server | Instance of the portal with a relational database supporting transactions and locking (SRS EIR-03); stack not yet chosen. |
| Client | Any current web browser for UI checks; HTTP client for API checks. |
| Time | A test clock that can set "now" (needed for TC-03, 07, 08, 09, 19). **A-T2** |
| Notification System | Stub that records requests and can be switched to *fail*. |
| Network | Single machine or LAN; latency not part of NFR-001 (server-side processing time is measured). |

## 7. Test Data
| Data | Content |
|---|---|
| Users | `studentA`, `studentB`, `student01`…`student20` (role Student); `tech1` (role Lab Technician). Passwords set by the tester; not recorded in this document. |
| Equipment | EQ-01 *Oscilloscope* – Valid; EQ-02 *Oscilloscope* – Valid (alternative); EQ-03 *Logic Analyzer* – Expired; EQ-04 *FPGA Board* – Pending; EQ-05 *Logic Analyzer* – Valid (only loaded for TC-05 and TC-24). |
| Reservations | Created by the tests themselves; the store is reset to the baseline before each test case. |
| Time values | Defined relative to "now" (e.g. *now + 1 day 10:00*). |

## 8. Test Tools
No tooling has been selected because the stack is not chosen. Required capabilities: an HTTP client able to send scripted requests, a facility to send concurrent requests and record timings (for TC-16, TC-17), direct read access to the data store for verification, and a stub for the Notification System. The tools will be named in the execution report; none are asserted here.

## 9. Responsibilities
| Role | Person |
|---|---|
| Test designer, executor, reporter | Anagha N (PES1UG24CS058) – individual project |
| Reviewer / approver | Course instructor |

## 10. Risks, Assumptions and Dependencies
| ID | Item |
|---|---|
| R-1 | NFR-001 "peak load" undefined → 20 concurrent requests used (A-03); result may need re-baselining. |
| R-2 | Boundary tests need a controllable clock (A-T2); without it TC-03, 07, 08, 09, 19 cannot be executed precisely. |
| R-3 | Assumptions A-04…A-09 (SRS §2.6) affect expected results; if the instructor decides otherwise, TC-02, 07, 09, 14 must be revised. |
| R-4 | No implementation exists; all schedule and effort depends on it. No dates are promised here. |
| D-1 | Notification stub available (A-12). D-2 Test data reset mechanism. |

## 11. Test Deliverables
This plan; executed test-case table with actual results; defect log; a requirements-to-test traceability report (§13).

## 12. Test Cases

Fields: Test Case ID, Requirement ID(s), Objective, Preconditions, Test Data, Steps, Expected Result, Actual Result, Pass/Fail (status), Test Type. Times use the test clock; "now" is the clock's current value.

**Summary**

| ID | Requirement(s) | Objective (short) | Type | Status |
|---|---|---|---|---|
| TC-01 | FR-001, FR-002 | Successful reservation | Functional | Not Executed |
| TC-02 | FR-001 | Duration boundary 120 / 121 min | Functional, Boundary | Not Executed |
| TC-03 | FR-001 | 7-day horizon boundary | Functional, Boundary | Not Executed |
| TC-04 | FR-001 | Overlapping slot on same equipment | Functional, Negative | Not Executed |
| TC-05 | FR-002 | Expired / Pending calibration blocked | Functional, Negative | Not Executed |
| TC-06 | FR-003 | Cancellation before cut-off | Functional | Not Executed |
| TC-07 | FR-003 | Cancellation cut-off boundary | Functional, Boundary | Not Executed |
| TC-08 | FR-004 | Late return sets penalty flag | Functional | Not Executed |
| TC-09 | FR-004 | On-time / at-end return has no flag | Functional, Boundary | Not Executed |
| TC-10 | FR-005 | Inventory add / update / remove | Functional | Not Executed |
| TC-11 | FR-006, SEC-REQ-07 | Valid and invalid login | Functional, Security | Not Executed |
| TC-12 | FR-007, SEC-REQ-03 | Own history only | Functional, Security | Not Executed |
| TC-13 | FR-008, FR-002 | Calibration status update takes effect | Functional | Not Executed |
| TC-14 | FR-009 | Confirmation + notification, notification failure | Functional, Fault injection | Not Executed |
| TC-15 | FR-010 | Student self-overlap rejected | Functional, Negative | Not Executed |
| TC-16 | NFR-001 | Reservation latency ≤ 200 ms | Non-functional (Performance) | Not Executed |
| TC-17 | NFR-003, FR-001 | Concurrent requests, one winner | Non-functional (Concurrency) | Not Executed |
| TC-18 | NFR-002, SEC-REQ-01 | Student blocked from technician functions | Security | Not Executed |
| TC-19 | NFR-002, SEC-REQ-02, FR-006 | 30-minute session expiry | Security, Boundary | Not Executed |
| TC-20 | SEC-REQ-04, SEC-REQ-07, FR-006 | Unauthenticated access, credential handling | Security | Not Executed |
| TC-21 | SEC-REQ-05, FR-001, FR-005 | Invalid input and injection strings | Security, Negative | Not Executed |
| TC-22 | SEC-REQ-06, FR-004, FR-005, FR-008 | Audit records for privileged actions | Security | Not Executed |
| TC-23 | SEC-REQ-03, FR-003 | Cancel another student's reservation | Security, Negative | Not Executed |
| TC-24 | FR-001 | Availability display and filters | Functional | Not Executed |
| TC-25 | FR-005 | Remove equipment that has a future reservation | Functional, Negative | Not Executed |

**Detailed test cases**

**TC-01 – Successful reservation** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-001(e), FR-002(a) (UC-03 main flow) |
| Objective | A student reserves a slot on Valid equipment and receives a token. |
| Preconditions | `studentA` logged in; EQ-01 Valid; no reservations exist. |
| Test Data | EQ-01; start = now + 1 day 10:00; duration 90 min. |
| Steps | 1. Open availability list (UC-02) and select EQ-01. 2. Submit reservation. 3. Open the availability list again. |
| Expected Result | Reservation created (HTTP 201) with status Confirmed and a non-empty token; confirmation screen shows token and slot; availability shows 10:00–11:30 as reserved; one reservation record stored. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-02 – Duration boundary** (Functional, Boundary)

| Field | Content |
|---|---|
| Requirement ID | FR-001(b) |
| Objective | Slot of exactly 120 minutes is accepted; 121 minutes is rejected. |
| Preconditions | `studentA` logged in; EQ-01 Valid, free. |
| Test Data | start = now + 1 day 10:00; durations 120 and 121 min (separate requests, store reset between). |
| Steps | 1. Reserve with 120 min. 2. Reset. 3. Reserve with 121 min. |
| Expected Result | 120 min → HTTP 201 Confirmed. 121 min → HTTP 422 `DURATION_EXCEEDS_LIMIT`; no reservation record created. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-03 – Booking horizon boundary** (Functional, Boundary)

| Field | Content |
|---|---|
| Requirement ID | FR-001(c) |
| Objective | A start time exactly 7 days after the request is accepted; later is rejected. |
| Preconditions | `studentA` logged in; EQ-01 Valid, free; test clock fixed at T. |
| Test Data | start = T + 7 days; start = T + 7 days + 1 min; duration 60 min. |
| Steps | 1. Reserve with start = T + 7 d. 2. Reset. 3. Reserve with start = T + 7 d + 1 min. |
| Expected Result | First → HTTP 201. Second → HTTP 422 `START_OUT_OF_RANGE`; no record created. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-04 – Overlapping slot on the same equipment** (Functional, Negative; UC-03 alternate flow A2)

| Field | Content |
|---|---|
| Requirement ID | FR-001(d) |
| Objective | A second student cannot reserve a slot that overlaps a Confirmed reservation of the same equipment. |
| Preconditions | `studentA` has Confirmed EQ-01 10:00–11:00 (day D). `studentB` logged in. |
| Test Data | `studentB` requests EQ-01, D 10:30, 60 min. Also D 11:00, 60 min (adjacent). |
| Steps | 1. `studentB` submits the overlapping request. 2. `studentB` submits the adjacent request 11:00–12:00. |
| Expected Result | Step 1 → HTTP 409 `SLOT_CONFLICT` with next available slots listed; no new record. Step 2 → accepted (adjacent, not overlapping). |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-05 – Expired / Pending calibration blocks reservation** (Functional, Negative; UC-03 alternate flow A1)

| Field | Content |
|---|---|
| Requirement ID | FR-002(b), FR-002(c) |
| Objective | Equipment whose calibration is not Valid cannot be reserved; an alternative is suggested. |
| Preconditions | `studentA` logged in; EQ-03 Expired; EQ-04 Pending; EQ-05 (*Logic Analyzer*, Valid) exists as the alternative for the suggestion check. |
| Test Data | Request for EQ-03 and for EQ-04, tomorrow 10:00, 60 min. |
| Steps | 1. Reserve EQ-03. 2. Reserve EQ-04. |
| Expected Result | Both → HTTP 409 `CALIBRATION_INVALID` with message "This equipment is currently unavailable for booking — calibration required."; the EQ-03 response suggests EQ-05 and the EQ-04 response suggests none (no other FPGA board); no reservation record created. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-06 – Cancellation before the cut-off** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-003 |
| Objective | A student cancels an own reservation; the slot is released within 5 s with no penalty. |
| Preconditions | `studentA` has Confirmed EQ-01 reservation starting in 3 hours. |
| Test Data | The reservation id. |
| Steps | 1. Cancel the reservation. 2. Poll availability of EQ-01 for that slot until Available or 5 s elapse. 3. Check the reservation record. |
| Expected Result | HTTP 200; status Cancelled; slot shows Available within 5 s; penalty flag false. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-07 – Cancellation cut-off boundary** (Functional, Boundary)

| Field | Content |
|---|---|
| Requirement ID | FR-003 |
| Objective | Cancellation exactly 60 min before start is accepted (A-04); at 59 min it is rejected. |
| Preconditions | Two Confirmed reservations R1, R2 of `studentA`, both starting at S. |
| Test Data | Test clock set to S − 60 min for R1; to S − 59 min for R2 (separate runs). |
| Steps | 1. Set clock S − 60 min, cancel R1. 2. Set clock S − 59 min, cancel R2. |
| Expected Result | R1 → HTTP 200 Cancelled. R2 → HTTP 409 `CANCELLATION_WINDOW_CLOSED`; R2 remains Confirmed and its slot stays reserved. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-08 – Late return sets the penalty flag** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-004 |
| Objective | Returning after the slot end records the timestamp and sets the penalty flag. |
| Preconditions | `tech1` logged in; Confirmed reservation with slot end E. |
| Test Data | Test clock = E + 1 min. |
| Steps | 1. `tech1` marks the reservation Returned. 2. Read the reservation. |
| Expected Result | HTTP 200; status Returned; return timestamp = E + 1 min; penalty flag = true. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-09 – On-time return has no penalty** (Functional, Boundary)

| Field | Content |
|---|---|
| Requirement ID | FR-004 |
| Objective | A return before, or exactly at, the slot end is not flagged (A-08). |
| Preconditions | `tech1` logged in; two Confirmed reservations RA, RB with slot end E. |
| Test Data | Clock = E − 10 min for RA; clock = E for RB. |
| Steps | 1. Return RA at E − 10 min. 2. Return RB at E. |
| Expected Result | Both: HTTP 200, status Returned, correct timestamps, penalty flag = false. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-10 – Inventory add / update / remove** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-005 |
| Objective | Technician changes to the inventory are persisted and visible immediately after saving. |
| Preconditions | `tech1` logged in; `studentA` has a second session open. |
| Test Data | New item: name "Spectrum Analyzer", category "RF", calibration due date = a future date. Update: category → "Instruments". |
| Steps | 1. Start the add form but do not save; `studentA` lists equipment. 2. Save the new item; list again. 3. Update the item; list again. 4. Remove the item; list again. |
| Expected Result | Step 1: item not visible. Step 2: HTTP 201, item listed. Step 3: HTTP 200, new category listed. Step 4: HTTP 200, item no longer listed. Changes persist after re-reading from the store. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-11 – Valid and invalid login** (Functional, Security)

| Field | Content |
|---|---|
| Requirement ID | FR-006, SEC-REQ-07 |
| Objective | Valid credentials give a session with the correct role; invalid credentials give no session and a generic error. |
| Preconditions | Accounts `studentA`, `tech1` exist. |
| Test Data | Valid pairs for both users; unknown user `nobody`/any password; `studentA` with a wrong password. |
| Steps | 1. Log in as `studentA`. 2. Log in as `tech1`. 3. Log in as `nobody`. 4. Log in as `studentA` with wrong password. |
| Expected Result | 1–2: HTTP 200, session issued, role Student / Lab Technician, role-appropriate menu. 3–4: HTTP 401 `INVALID_CREDENTIALS`, **identical** message and no session in both cases. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-12 – Own reservation history only** (Functional, Security)

| Field | Content |
|---|---|
| Requirement ID | FR-007, SEC-REQ-03 |
| Objective | A student sees all and only their own reservations with the required fields. |
| Preconditions | `studentA` has 2 reservations (one Confirmed, one Cancelled); `studentB` has 1. |
| Test Data | – |
| Steps | 1. `studentA` opens "My reservations". 2. `studentA` requests the detail of `studentB`'s reservation id directly. |
| Expected Result | 1: exactly 2 entries, each with equipment, start/end, status, token, penalty flag. 2: HTTP 403 `FORBIDDEN_RESOURCE`; no data of `studentB`'s reservation in the response. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-13 – Calibration status update takes effect** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-008, FR-002 |
| Objective | A status change by the technician governs subsequent reservation requests. |
| Preconditions | `tech1` and `studentA` logged in; EQ-01 Valid. |
| Test Data | EQ-01 → Expired → Valid; request tomorrow 10:00, 60 min. |
| Steps | 1. `tech1` sets EQ-01 Expired. 2. `studentA` reserves EQ-01. 3. `tech1` sets EQ-01 Valid. 4. `studentA` reserves EQ-01 again. 5. `tech1` sends status "Unknown". |
| Expected Result | 1: HTTP 200. 2: HTTP 409 `CALIBRATION_INVALID`. 3: HTTP 200. 4: HTTP 201 Confirmed. 5: HTTP 422 `INVALID_CALIBRATION_STATUS`, status unchanged. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-14 – Confirmation and notification, incl. notification failure** (Functional, Fault injection)

| Field | Content |
|---|---|
| Requirement ID | FR-009 (A-06) |
| Objective | A confirmed reservation produces an on-screen confirmation and one notification request; notification failure does not remove the reservation. |
| Preconditions | `studentA` logged in; EQ-01 Valid; Notification stub recording. |
| Test Data | Two reservations on different free slots; stub in *success* mode for the first, *fail* mode for the second. Also one rejected request (calibration invalid). |
| Steps | 1. Reserve (stub OK). 2. Reserve a different slot (stub fails). 3. Attempt a rejected reservation (EQ-03). |
| Expected Result | 1: confirmation shown; stub received exactly one request with student, equipment, slot, token. 2: confirmation still shown, reservation Confirmed, failure entry in the application log. 3: stub received no request. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-15 – Student self-overlap rejected** (Functional, Negative)

| Field | Content |
|---|---|
| Requirement ID | FR-010 |
| Objective | One student cannot hold two overlapping reservations on different equipment. |
| Preconditions | `studentA` has Confirmed EQ-01 on day D 10:00–11:00; EQ-02 Valid, free. |
| Test Data | `studentA` requests EQ-02, D 10:30, 30 min. |
| Steps | 1. Submit the request. |
| Expected Result | Rejected with HTTP 409 `STUDENT_SLOT_CONFLICT`; no new record; EQ-02 slot remains available. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-16 – Reservation latency** (Non-functional – Performance)

| Field | Content |
|---|---|
| Requirement ID | NFR-001 |
| Objective | Reservation requests are processed in ≤ 200 ms under the A-03 test load. |
| Preconditions | Baseline data; accounts `student01`…`student20` logged in; timing facility ready. |
| Test Data | 20 concurrent requests, one per student, each for a different non-overlapping slot of EQ-01 or EQ-02 (so every request is legitimate and can succeed). |
| Steps | 1. Send the 20 requests simultaneously. 2. Record the processing time of each (request received → response sent). 3. Repeat the run 5 times. |
| Expected Result | Every recorded processing time ≤ 200 ms in all runs; all 20 requests per run succeed. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-17 – Concurrent requests for the same slot** (Non-functional – Concurrency / data integrity)

| Field | Content |
|---|---|
| Requirement ID | NFR-003, FR-001 |
| Objective | With simultaneous identical-slot requests, exactly one reservation is confirmed. |
| Preconditions | EQ-01 Valid and free at slot X; accounts `student01`…`student20` logged in. |
| Test Data | 20 simultaneous requests for EQ-01, slot X (tomorrow 10:00, 60 min). |
| Steps | 1. Release all 20 requests at the same instant. 2. Count responses by status. 3. Query the store for reservations of EQ-01 at X. |
| Expected Result | Exactly 1 × HTTP 201; 19 × HTTP 409 `SLOT_CONFLICT`; exactly 1 stored reservation for the slot; exactly one token issued. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-18 – Student blocked from technician-only functions** (Security)

| Field | Content |
|---|---|
| Requirement ID | NFR-002, SEC-REQ-01 |
| Objective | Technician-only endpoints reject a Student session without changing data. |
| Preconditions | `studentA` logged in; a Confirmed reservation R and equipment EQ-01 exist. |
| Test Data | Calls: update calibration of EQ-01 → Expired; add equipment; update equipment; remove equipment; return R. |
| Steps | 1. Send each call with `studentA`'s token. 2. Compare store state before and after. |
| Expected Result | Each call → HTTP 403 `FORBIDDEN_ROLE`; EQ-01 status, inventory and R unchanged. Same calls with `tech1`'s token succeed (control). |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-19 – Session expiry after 30 minutes of inactivity** (Security, Boundary)

| Field | Content |
|---|---|
| Requirement ID | NFR-002, SEC-REQ-02, FR-006 |
| Objective | A session idle 29 min still works (and its idle timer restarts); one idle 31 min is rejected. |
| Preconditions | Test clock available; two logins of `studentA` (sessions S1, S2). |
| Test Data | S1: idle 29 min then request, then idle 29 min again then request. S2: idle 31 min then request. |
| Steps | 1. Advance clock 29 min; S1 requests availability. 2. Advance 29 min; S1 requests again. 3. Advance S2's idle time to 31 min; S2 requests availability. 4. Log in again. |
| Expected Result | 1 and 2: HTTP 200 (activity resets the timer). 3: HTTP 401 `SESSION_EXPIRED`, no data returned. 4: new session works. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-20 – Unauthenticated access and credential handling** (Security)

| Field | Content |
|---|---|
| Requirement ID | SEC-REQ-04, SEC-REQ-07, FR-006 |
| Objective | Protected functions need a valid session; credentials are not exposed. |
| Preconditions | None logged in. |
| Test Data | Every protected endpoint of Design §9 called with (a) no token, (b) a malformed token. Login attempts with a known password. |
| Steps | 1. Call each protected endpoint without a token, then with a malformed token. 2. Perform successful and failed logins. 3. Inspect the application log, audit records and the stored user record. |
| Expected Result | 1: HTTP 401 `AUTHENTICATION_REQUIRED` for every endpoint, no data (SEC-REQ-04). 3: the password does not appear in any log or response, and is not stored as plain text (SEC-REQ-07). |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-21 – Invalid input and injection strings** (Security, Negative)

| Field | Content |
|---|---|
| Requirement ID | SEC-REQ-05, FR-001, FR-005 |
| Objective | Malformed or hostile input is rejected on the server and does not change data. |
| Preconditions | `studentA` and `tech1` logged in; baseline data. |
| Test Data | Reservation: duration 0, −30, "abc"; start in the past; missing equipmentId; equipmentId `1 OR 1=1`. Availability filter `category=' OR '1'='1`. Inventory: empty name; name = `'; DROP TABLE equipment;--`. |
| Steps | 1. Send each request. 2. After all requests, read equipment and reservation tables and the equipment list. |
| Expected Result | Reservation/filter/validation cases → HTTP 400/422 with a field-level error and no state change; the injection filter returns no extra rows. The inventory name containing SQL text is either rejected by validation or stored literally as text. All tables and baseline rows remain intact. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-22 – Audit records for privileged actions** (Security)

| Field | Content |
|---|---|
| Requirement ID | SEC-REQ-06, FR-004, FR-005, FR-008 |
| Objective | Each privileged action creates an attributable audit record. |
| Preconditions | `tech1` logged in; empty audit log; Confirmed reservation R. |
| Test Data | Actions: set EQ-01 calibration Expired; add equipment; update equipment; remove equipment; return R. |
| Steps | 1. Perform the five actions. 2. Read the audit records. |
| Expected Result | Exactly 5 records, each with user id (`tech1`), role, action type, target id, timestamp (≈ action time). Failed/rejected attempts (TC-18) create no record of success. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-23 – Cancel another student's reservation** (Security, Negative)

| Field | Content |
|---|---|
| Requirement ID | SEC-REQ-03, FR-003 |
| Objective | A student cannot cancel a reservation owned by someone else. |
| Preconditions | `studentA` owns Confirmed reservation R (starts in 3 hours); `studentB` logged in. |
| Test Data | R's id. |
| Steps | 1. `studentB` sends the cancel request for R. 2. Read R. |
| Expected Result | HTTP 403 `FORBIDDEN_RESOURCE`; R remains Confirmed and its slot stays reserved. |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-24 – Availability display and filters** (Functional)

| Field | Content |
|---|---|
| Requirement ID | FR-001(a) |
| Objective | The availability list shows equipment with its calibration status, the filters work, and reserved slots equal the Confirmed reservations. |
| Preconditions | Baseline equipment EQ-01…EQ-05 (§7); `studentA` logged in; EQ-01 has one Confirmed reservation R1 (day D 10:00–11:00) and one Cancelled reservation R2 (day D 14:00–15:00). |
| Test Data | Filters: `category=Oscilloscope`; `calibrationStatus=Expired`; both together; availability of EQ-01 for day D. |
| Steps | 1. List equipment without filter. 2. List with `category=Oscilloscope`. 3. List with `calibrationStatus=Expired`. 4. List with both filters. 5. Request availability of EQ-01 for day D. |
| Expected Result | 1: five items, each with its calibration status. 2: EQ-01 and EQ-02 only. 3: EQ-03 only. 4: empty list (empty-list message in the UI). 5: exactly one reserved slot, 10:00–11:00 (R2 is not shown as reserved). |
| Actual Result | – |
| Pass/Fail | Not Executed |

**TC-25 – Remove equipment that has a future reservation** (Functional, Negative; depends on assumption A-07)

| Field | Content |
|---|---|
| Requirement ID | FR-005 |
| Objective | Equipment with a future Confirmed reservation cannot be removed; equipment without one can. |
| Preconditions | `tech1` logged in; EQ-01 has a future Confirmed reservation R; EQ-02 has none. |
| Test Data | Remove EQ-01; remove EQ-02. |
| Steps | 1. Remove EQ-01. 2. Read EQ-01 and R. 3. Remove EQ-02. 4. List equipment. |
| Expected Result | 1: HTTP 409 `EQUIPMENT_HAS_ACTIVE_RESERVATIONS`. 2: EQ-01 still listed, R still Confirmed. 3: HTTP 200. 4: EQ-02 no longer listed. If the instructor decides otherwise for A-07, this case is revised. |
| Actual Result | – |
| Pass/Fail | Not Executed |

## 13. Traceability Matrix (Requirement → Test Case)

| Requirement | Test cases | Coverage note |
|---|---|---|
| FR-001 | TC-01, TC-02, TC-03, TC-04, TC-17, TC-21, TC-24 | clause (a) TC-24; (b) TC-02; (c) TC-03; (d) TC-04, TC-17; (e) TC-01; invalid input TC-21 |
| FR-002 | TC-01, TC-05, TC-13 | clause (a) TC-01, TC-13; (b), (c) TC-05 |
| FR-003 | TC-06, TC-07, TC-23 | |
| FR-004 | TC-08, TC-09, TC-22 | |
| FR-005 | TC-10, TC-21, TC-22, TC-25 | |
| FR-006 | TC-11, TC-19, TC-20 | |
| FR-007 | TC-12 | |
| FR-008 | TC-13, TC-22 | |
| FR-009 | TC-14 | |
| FR-010 | TC-15 | |
| NFR-001 | TC-16 | |
| NFR-002 | TC-18, TC-19 | |
| NFR-003 | TC-17 | |
| SEC-REQ-01 | TC-18 | |
| SEC-REQ-02 | TC-19 | |
| SEC-REQ-03 | TC-12, TC-23 | |
| SEC-REQ-04 | TC-20 | |
| SEC-REQ-07 | TC-11, TC-20 | |
| SEC-REQ-05 | TC-21 | |
| SEC-REQ-06 | TC-22 | |

Totals: 25 test cases – 17 functional (TC-01…TC-15, TC-24, TC-25), 2 non-functional (TC-16, TC-17), 6 security (TC-18…TC-23); TC-11 and TC-12 also carry security requirements. Every requirement in the SRS has at least one test case. Test types present: normal-flow, invalid-input, boundary, error-handling, fault-injection, performance, concurrency and security.
