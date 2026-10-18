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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=============================================
       PAWPAL+ DAILY SCHEDULE FOR ALEX
   Daily Time Budget: 60 minutes
=============================================

✅ SCHEDULED TASKS:
  • [Health] Give Luna Joint Supplement (5m) - Priority 1
  • [Exercise] Luna Neighborhood Walk (30m) - Priority 2
  • [Grooming] Groom Milo's Fur (15m) - Priority 3

Total Scheduled Time: 50 / 60 mins

⚠️ OMITTED TASKS (Over Budget):
  • [Enrichment] Extended Dog Park Play (25m) - Priority 4

📋 SCHEDULER LOG / REASONING:
  - Included 'Give Luna Joint Supplement' (5m) - Priority 1.
  - Included 'Luna Neighborhood Walk' (30m) - Priority 2.
  - Included 'Groom Milo's Fur' (15m) - Priority 3.
  - Omitted 'Extended Dog Park Play' (25m) - Exceeds daily limit of 60m.
=============================================

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

| Feature           | Method(s)                                                                                   | Notes                                                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_duration()`, `Scheduler.sort_by_time()`, `Scheduler.generate_schedule()` | Sorts by duration, or by priority then duration when generating the schedule. `sort_by_time()` is a compatibility alias for duration sorting.                   |
| Filtering         | `Owner.filter_tasks()`, `Scheduler.generate_schedule()`                                     | Filters by pet name and/or completion status; scheduling includes each priority-ordered task that fits the remaining daily minutes and omits tasks that do not. |
| Conflict handling | `Scheduler._get_overlap_warnings()`                                                         | Detects and logs overlapping scheduled time slots on the same due date; back-to-back tasks are not treated as overlapping.                                      |
| Recurring tasks   | `Task.mark_complete()`, `Pet.mark_task_complete()`                                          | Completing a daily or weekly task creates its next occurrence; other frequencies do not recur.                                                                  |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
