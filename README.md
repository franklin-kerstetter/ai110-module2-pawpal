# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

**CLI Output**
```
Test generating simple schedule

================================================================================
Schedule for Sunday, June 28, 2026
================================================================================

MORNING
[ ] Feed Queen                     05:00 AM     (5m) | Queen
[ ] Feed Archie                    05:05 AM     (5m) | Archie
--------------------------------------------------------------------------------

MIDDAY
[ ] Feed Queen                     11:00 AM     (5m) | Queen
[ ] Feed Archie                    11:05 AM     (5m) | Archie
--------------------------------------------------------------------------------

EVENING
[ ] Feed Queen                     05:00 PM     (5m) | Queen
[ ] Feed Archie                    05:05 PM     (5m) | Archie
--------------------------------------------------------------------------------

NIGHT
[ ] Feed Queen                     11:00 PM     (5m) | Queen
[ ] Feed Archie                    11:05 PM     (5m) | Archie
--------------------------------------------------------------------------------
Notes: All tasks scheduled.
================================================================================

Test marking morning tasks as done!

================================================================================
Schedule for Sunday, June 28, 2026
================================================================================

MORNING
[✓] Feed Queen                     05:00 AM     (5m) | Queen
[✓] Feed Archie                    05:05 AM     (5m) | Archie
--------------------------------------------------------------------------------

MIDDAY
[ ] Feed Queen                     11:00 AM     (5m) | Queen
[ ] Feed Archie                    11:05 AM     (5m) | Archie
--------------------------------------------------------------------------------

EVENING
[ ] Feed Queen                     05:00 PM     (5m) | Queen
[ ] Feed Archie                    05:05 PM     (5m) | Archie
--------------------------------------------------------------------------------

NIGHT
[ ] Feed Queen                     11:00 PM     (5m) | Queen
[ ] Feed Archie                    11:05 PM     (5m) | Archie
--------------------------------------------------------------------------------
Notes: All tasks scheduled.
================================================================================

Test generating complex schedule

================================================================================
Schedule for Sunday, June 28, 2026
================================================================================

MORNING
[ ] Feed Buddy                     06:00 AM     (5m) | Buddy
[ ] Feed Fluffy                    06:05 AM     (5m) | Fluffy
--------------------------------------------------------------------------------

MIDDAY
[ ] Feed Buddy                     11:00 AM     (5m) | Buddy
[ ] Feed Fluffy                    11:05 AM     (5m) | Fluffy
--------------------------------------------------------------------------------

EVENING
[ ] Feed Buddy                     05:00 PM     (5m) | Buddy
[ ] Feed Fluffy                    05:05 PM     (5m) | Fluffy
--------------------------------------------------------------------------------
Notes: Scheduled 6/8 tasks. Missing: NIGHT: Feed Fluffy (Fluffy), Feed Buddy (Buddy).
================================================================================


================================================================================
SORTING AND FILTERING DEMONSTRATION
================================================================================

Completed Blocks (3):
  [✓] Feed Buddy                     06:00 AM     (5m) | Buddy
  [✓] Feed Buddy                     11:00 AM     (5m) | Buddy
  [✓] Feed Buddy                     05:00 PM     (5m) | Buddy

Uncompleted Blocks (3):
  [ ] Feed Fluffy                    06:05 AM     (5m) | Fluffy
  [ ] Feed Fluffy                    11:05 AM     (5m) | Fluffy
  [ ] Feed Fluffy                    05:05 PM     (5m) | Fluffy

--------------------------------------------------------------------------------

All Tasks Sorted by Time of Day, Priority, and Pet Age:
  Feed Buddy | Buddy | MORNING (explicit: 06:00:00)
  Feed Fluffy | Fluffy | MORNING (explicit: 06:00:00)
  Feed Buddy | Buddy | MIDDAY (explicit: 12:30:00)
  Feed Fluffy | Fluffy | MIDDAY (explicit: 12:30:00)
  Feed Buddy | Buddy | EVENING (explicit: 17:30:00)
  Feed Fluffy | Fluffy | EVENING (explicit: 17:30:00)

--------------------------------------------------------------------------------

Tasks for Fluffy (3):
  Feed Fluffy | MORNING (explicit: 06:00:00)
  Feed Fluffy | MIDDAY (explicit: 12:30:00)
  Feed Fluffy | EVENING (explicit: 17:30:00)

--------------------------------------------------------------------------------

Tasks for Buddy (3):
  Feed Buddy | MORNING (explicit: 06:00:00)
  Feed Buddy | MIDDAY (explicit: 12:30:00)
  Feed Buddy | EVENING (explicit: 17:30:00)

================================================================================
CONFLICT DETECTION DEMONSTRATION (Complex Schedule)
================================================================================

No scheduling conflicts detected.

================================================================================
CONFLICT DETECTION DEMONSTRATION (Conflicting Schedule)
================================================================================

Generating schedule with intentional overlapping tasks...

================================================================================
Schedule for Sunday, June 28, 2026
================================================================================

MORNING
[ ] Morning Walk                   08:00 AM     (30m) | Max
[ ] Grooming                       08:15 AM     (20m) | Max
[ ] Vet Appointment                08:20 AM     (25m) | Bella
--------------------------------------------------------------------------------
Notes: Schedule with intentional conflicts for testing
================================================================================

✓ Successfully detected 3 conflict(s):
  ⚠ Conflict: 'Morning Walk' (Max) and 'Grooming' (Max) overlap [same pet]
  ⚠ Conflict: 'Morning Walk' (Max) and 'Vet Appointment' (Bella) overlap [different pets]
  ⚠ Conflict: 'Grooming' (Max) and 'Vet Appointment' (Bella) overlap [different pets]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

The various one-off methods the instructions ask for are listed below.
My implementation doesn't necessarily leverage them for the schedule generation.
All of the schedule generation logic around this is handled within the core [generate_schedule](./pawpal_system.py#673) method where [_schedule_time_period](./pawpal_system.py#594) deals with sorting, conflicts, etc.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | [sort_task_pet_tuples_by_time](./pawpal_system.py#474), [sort_by_time](./pawpal_system.py#478) | Sorts tasks by time of day, priority, associated pet age, and then pet uuid |
| Filtering | [filter_tasks_by_pet_name](./pawpal_system.py#483), [filter_blocks_by_completion_status](./pawpal_system.py#487) | offers various filter capabilities|
| Conflict handling | [detect_schedule_conflicts](./pawpal_system.py#510) | creates a list of warnings for overlapping blocks |
| Recurring tasks | [RecurrencePattern Class](./pawpal_system.py#76) | abstract patterns which offer daily, weekly, and monthly patterns|

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
