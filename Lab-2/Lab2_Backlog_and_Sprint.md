# Lab 2: Agile Backlog Creation & Sprint Simulation (Jira)

**PES1UG24CS058 - Anagha Nagaragadde**
Scenario: Smart Lab Equipment & Slot Reservation Portal (Lab 1 requirements, see `docs/SRS.md`).
Roles: Student, Lab Technician.

> Screenshots from the real Jira project go in `evidence/` (see `evidence/README.md`).
> This file is the written backlog, estimates and sprint plan that the Jira project is built from.

## 1. Epics

| Epic | Name | Description | Lab 1 source |
|---|---|---|---|
| E1 | Equipment Reservation | Students check availability and book, and cancel equipment slots. | FR-001, FR-002, FR-003, FR-010 |
| E2 | Access & Identity | Users log in and get role-based access. | FR-006, NFR-002 |
| E3 | Equipment & Calibration Management | Technicians keep equipment records and calibration status correct. | FR-005, FR-008 |
| E4 | Returns & Penalties | Technicians record returns and flag late returns. | FR-004 |
| E5 | Reservation Tracking & Notifications | Students see their history and receive confirmations. | FR-007, FR-009 |
| E6 | Performance & Data Integrity | Fast responses and no double booking under load. | NFR-001, NFR-003 |

## 2. User stories, priority and story points (Fibonacci)

| ID | Epic | User story | Priority | Points | Sprint |
|---|---|---|---|---|---|
| S1.1 | E1 | As a student, I want to see equipment availability filtered by category and calibration status, so that I can choose an instrument that is free and usable. | High | 3 | 1 |
| S1.2 | E1 | As a student, I want to reserve a slot of up to 120 minutes within the next 7 days and receive a unique token, so that my slot is guaranteed. | High | 8 | 1 |
| S1.3 | E1 | As a student, I want a request that overlaps an existing booking to be rejected, so that two people never hold the same slot. | High | 5 | 1 |
| S1.4 | E1 | As a student, I want to be blocked from booking equipment with Expired or Pending calibration and be offered an alternative, so that I do not run experiments on uncalibrated instruments. | High | 5 | 1 |
| S1.5 | E1 | As a student, I want to cancel my reservation up to 60 minutes before it starts, so that the slot is released for others without a penalty. | Medium | 3 | 2 |
| S1.6 | E1 | As a student, I want to be stopped from booking two overlapping slots myself, so that I do not double-book my own time. | Medium | 2 | 2 |
| S2.1 | E2 | As a user, I want to log in with my credentials and get the right role, so that I only see what I am allowed to use. | High | 5 | 1 |
| S2.2 | E2 | As a lab technician, I want technician-only actions blocked for students and my session to expire after 30 minutes idle, so that the system stays secure. | High | 5 | 1 |
| S3.1 | E3 | As a lab technician, I want to add, update and remove equipment records, so that the list matches the lab. | Medium | 3 | 2 |
| S3.2 | E3 | As a lab technician, I want to set calibration status to Valid, Expired or Pending, so that bookings follow the real instrument state. | High | 3 | 1 |
| S4.1 | E4 | As a lab technician, I want to mark a reservation Returned and have late returns flagged, so that penalties are applied correctly. | High | 5 | 2 |
| S5.1 | E5 | As a student, I want to view my own reservation history with status, token and penalty flag, so that I can track my bookings. | Medium | 3 | 2 |
| S5.2 | E5 | As a student, I want an on-screen confirmation and a notification after booking, so that I know the booking succeeded. | Medium | 3 | 2 |
| S6.1 | E6 | As a student, I want reservation requests processed in 200 ms or less under 20 concurrent requests, so that booking feels instant. | High | 5 | 2 |
| S6.2 | E6 | As a student, I want only one of several simultaneous requests for the same slot to be confirmed, so that the database never double-books. | High | 8 | 1 |

Total: 66 points. Scale used: 1, 2, 3, 5, 8.

Estimation rationale: 8 points go to the stories with the most uncertainty (the full reservation rules in S1.2, database-level locking in S6.2). Simple list or form stories get 2-3.

## 3. Estimation notes (Planning Poker basis)

These are the starting estimates to bring to Planning Poker. The reasons for the highest points:

- S1.2 (8): five validation clauses (duration, 7-day window, overlap, token, slot lock).
- S6.2 (8): database-level locking plus concurrent testing.
- S3.2 (3): one status field, with the rule applied in the booking path.

## 4. Sprint 1 plan

Goal: A student can log in, see calibrated equipment and book a slot that cannot be double-booked.
Sprint length: 1 week (as the handout requires). Two sprints are run.

| Story | Points |
|---|---|
| S1.1 | 3 |
| S1.2 | 8 |
| S1.3 | 5 |
| S1.4 | 5 |
| S2.1 | 5 |
| S2.2 | 5 |
| S3.2 | 3 |
| S6.2 | 8 |
| **Total** | **42** |

Sprint 1 holds the High-priority stories that form the booking path.

Board columns: To Do -> In Progress -> Done.

## 5. Planned burndown (ideal line)

Sprint length 5 working days, 42 points, ideal burn of 8.4 points per day.

| Day | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Ideal remaining | 42 | 33.6 | 25.2 | 16.8 | 8.4 | 0 |

The actual burndown comes from Jira's Burndown Chart after the stories are moved to Done. It is not filled in here because it must come from the real sprint.

## 6. Backlog beyond Sprint 1

Sprint 2 (24 points): S1.5, S1.6, S3.1, S4.1, S5.1, S5.2, S6.1.

## 7. Traceability to Lab 1

Every story maps to a Lab 1 requirement (see the Lab 1 source column). All 10 FRs and 3 NFRs are covered.
