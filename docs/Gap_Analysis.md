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
| Security objectives (≥ 2) and requirements (≥ 2) | missing → SRS §4 (4 objectives, 7 requirements) |
| IEEE-style Test Plan, sections 3, 4, 5, §5.1 Security Validation, traceability | missing → `Test_Plan.md` |
| ≥ 7–10 test cases covering FR and NFR | missing → 25 test cases |
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

## 5. Final audit (strict-evaluator pass) – problems found and what was changed

| # | Finding | Change |
|---|---|---|
| 1 | FR-001 and FR-002 bundled several verifiable statements in one sentence (not atomic). | Kept the IDs; rewrote them as clauses (a)–(e) and (a)–(c) with a per-clause pass criterion; tests now name the clause they cover. |
| 2 | New requirements FR-006…FR-010, NFR-003 did not state where they came from. | Added a *Status / basis* column naming the Lab 1 source (diagram use case, UC-03 step/precondition, or the split of NFR-001). |
| 3 | Several security requirements were not in Lab 1 and looked invented. | Added a *Basis* column; marked SEC-REQ-03, 05, 06, 07 as *Proposed* with the reason; kept only requirements tied to a Lab 1 use case or NFR-002. |
| 4 | SEC-REQ-04 combined three obligations. | Split: SEC-REQ-04 (401 without a session) and SEC-REQ-07 (generic login error, no plain-text credentials); tests and matrix updated. |
| 5 | FR-010 read the UC-03 precondition one specific way without saying so. | Added assumption A-14 and the condition under which FR-010/TC-15 would be dropped. |
| 6 | "Relational database" was stated as fact; Lab 1 only says "database-level lock isolation". | Reworded to "database with transactions and locking (relational assumed – A-13)". |
| 7 | Documents claimed to follow IEEE Std 830/829/1016 formally. | Replaced by "IEEE-style structure as requested by the assignment; no formal compliance claimed". |
| 8 | Coverage gaps: availability display / filters (FR-001(a)) and equipment removal with future reservations (A-07) had no dedicated test; test data lacked the accounts needed by TC-16/17 and equipment EQ-05 for TC-05. | Added TC-24, TC-25 (suite is now 25); extended test data (§7). |
| 9 | API section did not say why an API exists or which endpoints are additions. | §9 now cites NFR-002 ("endpoints") and marks endpoints 10 and 12 as the only design additions. |
| 10 | Component diagram: the *ILog* arrow from the services package suggested all four services log, while the table says three. | Caption and §4.2 now state exactly which components use each interface. |
| 11 | Diagram text was too small when printed (sequence diagram with 8 participants on a portrait page). | UC-03 split into two readable parts (SD-01 part 1 / part 2); all figures are on landscape pages with larger fonts. |
| 12 | Authorization-path arrow crossed another arrow in the component diagram. | Re-routed. |
| 13 | PDF/DOCX defects found on a page-by-page read: empty shaded first row in the document-info tables, the SRS security table rendered as raw text, headings stranded before landscape figures, figures printed small, a stray control character before a figure. | Fixed in the SRS table markup and in `build_docs.py`; headings now sit on the same landscape page as their figure; PDFs and DOCX rebuilt and re-checked (no raw Markdown, no near-empty pages except one section-lead page). |
| 14 | draw.io files had unconnected arrows. | In the use-case and component `.drawio` files, arrows whose ends touch a shape are now attached to it (verified by re-rendering in draw.io). Sequence diagrams keep free-standing message arrows. |
