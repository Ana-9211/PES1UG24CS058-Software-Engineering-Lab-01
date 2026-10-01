# Gap Analysis – Lab 1 baseline vs. Mini-Project Part-1

Baseline files (kept unchanged in the repository root): `Requirements_Table.docx`, `UseCase_Flow_Specification.docx`, `UML_UseCase_Diagram.pdf`. No source code exists in the repository.

## 1. EXISTING
| Item | Content |
|---|---|
| Requirements | FR-001…FR-005 and NFR-001, NFR-002 with type, priority, acceptance criteria, rationale (Lab 1 mandated exactly these 5 + 2). |
| Use case flow | UC-03 Reserve Equipment Slot: preconditions, postconditions, 8-step main flow, alternate flows A1 (calibration) and A2 (slot conflict). |
| UML use-case diagram | Actors Student, Lab Technician, Notification System; 12 use cases; 3 «include» from Reserve Equipment Slot, 1 «extend» (Apply Late-Return Penalty → Return Equipment). |

## 2. MISSING (required by the Part-1 assignment)
| Assignment item | Status before |
|---|---|
| IEEE-style SRS with introduction, FR, NFR, interfaces | missing → `SRS.md` |
| Security objectives (≥ 2) and requirements (≥ 2) | missing → SRS §4 (4 objectives, 6 requirements) |
| IEEE-style Test Plan, sections 3, 4, 5, §5.1 Security Validation, traceability | missing → `Test_Plan.md` |
| ≥ 7–10 test cases covering FR and NFR | missing → 23 test cases |
| Architecture: component diagram + description, pattern, traceability, security architecture | missing → Architecture §2–§7, Figure 2 |
| Design: ≥ 2 sequence diagrams, API design, error handling | missing → Design §8–§11, Figures 3–4 |
| IDs for use cases other than UC-03; use-case descriptions for the rest | missing → UC-01…UC-12 assigned and described |

## 3. NEEDS REVISION
| # | Existing material | Problem | Resolution (intent preserved) |
|---|---|---|---|
| 1 | Diagram vs. FR-004 | Diagram links **Student** to *Return Equipment*, but FR-004 says a Lab Technician marks the return. | Association removed in the redrawn diagram; documented in SRS §5.1. |
| 2 | Diagram vs. requirements | *Login*, *View Reservation History*, *Update Calibration Status* and *Send Confirmation Notification* have no requirement (NFR-002 mentions calibration update only as a restriction). | Added FR-006, FR-007, FR-008, FR-009 (marked [NEW]). |
| 3 | UC-03 precondition "no conflicting reservation for the same time slot" | Not backed by a requirement. | Added FR-010. |
| 4 | FR-001 | "real-time availability" is not measurable; one sentence bundles viewing, reserving, limits, token. | Kept ID and intent; reworded: availability reflects all Confirmed reservations; limits stated as 120 min / 7 days / overlap; marked [REFINED]. |
| 5 | NFR-001 | Bundles latency and lock isolation; "peak load" and "security standards" undefined → untestable as written. | Latency kept as NFR-001 (≤ 200 ms, load = test parameter A-03); isolation outcome split into NFR-003; "security standards" dropped (covered by SEC-REQs). |
| 6 | NFR-002 | Fine as a requirement but combines RBAC and session expiry. | Kept unchanged; derived SEC-REQ-01 and SEC-REQ-02 so each half has its own test. |
| 7 | FR-003 | "up to 1 hour before" ambiguous at exactly 60 min. | Assumption A-04 (inclusive), boundary test TC-07. |
| 8 | FR-004 | Which reservation states can be returned is unstated. | Only Confirmed (Design §9, 409 `INVALID_RESERVATION_STATE`). |
| 9 | UC-03 | Secondary actor "Lab Technician" has no step in the main flow; flow ends at A2 with no invalid-session/input, student-overlap or notification-failure paths. | Technician listing kept (fidelity) and footnoted; A3, A4 and E1 added and marked as Part-1 additions. |
| 10 | UC-03 step 5/7 | The overlap check and the lock are separate steps. | Design performs them atomically in one transaction (DD-02) – same observable behaviour, needed for NFR-003. |
| 11 | Diagram | No use-case IDs. | UC-01…UC-12 assigned (UC-03 retained from the Lab 1 specification). |

## 4. Information that Lab 1 does not provide (assumptions A-01…A-12 in SRS §2.6)
Technology stack; definition of "peak load"; slot granularity / minimum duration; behaviour on notification failure; deletion of equipment with future reservations; whether the due date changes status automatically; deployment security (HTTPS). Each was resolved with a labelled assumption – none is stated as fact – and should be confirmed with the instructor.
