# Lab 2: Agile Backlog Creation & Sprint Simulation (Jira)

**PES1UG24CS058 - Anagha N**
Jira site: `pes1ug24cs058.atlassian.net`, space **Scrum_BPS#25** (company-managed Scrum, key `SCRUMBPS25`).
Scenario: Smart Lab Equipment & Slot Reservation Portal (Lab 1 requirements, see `../docs/SRS.md`).

This summary is read from the Jira project. Screenshots are in `evidence/`.

## 1. Epics

| Key | Epic |
|---|---|
| SCRUMBPS25-1 | Equipment Discovery & Reservation |
| SCRUMBPS25-2 | Reservation Management |
| SCRUMBPS25-3 | Equipment Return & Accountability |
| SCRUMBPS25-4 | Equipment Inventory Management |
| SCRUMBPS25-5 | Security & Reservation Integrity |

## 2. User stories, priority, story points (Fibonacci) and sprint

| Key | Epic | Story | Priority | Points | Sprint |
|---|---|---|---|---|---|
| SCRUMBPS25-6 | 1 | FR-001 View Availability and Reserve Equipment Slot | High | 8 | 1 |
| SCRUMBPS25-7 | 1 | FR-002 Verify Calibration Status Before Confirming Reservation | High | 5 | 1 |
| SCRUMBPS25-8 | 2 | FR-003 Cancel Reservation Before 1-Hour Cutoff | Medium | 3 | 2 |
| SCRUMBPS25-9 | 3 | FR-004 Log Equipment Return and Apply Late Penalty | High | 5 | 1 |
| SCRUMBPS25-10 | 4 | FR-005 Manage Equipment Inventory Records | Medium | 5 | 2 |
| SCRUMBPS25-11 | 5 | NFR-001 Fast, Race-Free Concurrent Reservation Processing | High | 8 | 1 |
| SCRUMBPS25-12 | 5 | NFR-002 Role-Based Access Control with Session Expiry | High | 8 | 1 |

Total: 42 points (Sprint 1: 34, Sprint 2: 8). Each story has an implementation task (SCRUMBPS25-13 to 20) and sub-tasks (SCRUMBPS25-21 to 37).

## 3. Sprints (1 week each, both closed, all work Done)

- **SCRUMBPS Sprint 1.** Goal: deliver all High-priority reservation and security requirements (FR-001, FR-002, FR-004, NFR-001, NFR-002) with their supporting tasks. Scope 34 points, completed 34.
- **SCRUMBPS Sprint 2.** Goal: deliver the remaining Medium-priority requirements (FR-003, FR-005) with their supporting tasks, completing the full backlog. Scope 8 points.

## 4. Evidence

| File | Shows |
|---|---|
| `evidence/backlog_epics_and_stories.png` | Epics with their stories and tasks, priorities, status |
| `evidence/story_points_sprint1.png` | Sprint 1 completed issues with story points (34) |
| `evidence/burnup_chart_sprint1.png` | Sprint 1 burnup chart (Reports) |
| `evidence/sprint1_report_burndown.png` | Sprint 1 report with burndown against the guideline |
| `evidence/sprint2_report.png` | Sprint 2 report, story points (8) |

Note on Sprint 2: the stories in it were completed on 2 Sep, before the sprint's configured start date of 9 Sep, so Jira lists them as "completed outside of this sprint" and the Sprint 2 chart is flat. This comes from running the sprints back to back in one sitting.
