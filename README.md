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
python -m pytest


The tests cover the core scheduler behaviors: sorting tasks by duration, recurring daily tasks correctly, detecting overlapping/conflicting scheduled times, respecting the daily time budget, and filtering tasks by completion status and pet.

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/mac/Desktop/ai110-module2show-pawpal-starter
collected 14 items

tests/test_pawpal.py ..............                                      [100%]

============================== 14 passed in 0.03s ==============================
```

My Confidence Level is 5/5 stars in the system's reliability

## ✨ Features

- **Task sorting:** Pending tasks can be displayed shortest-first by duration. The legacy `sort_by_time()` method is an alias for duration sorting; it does not sort by clock time.
- **Greedy, priority-based scheduling:** The scheduler considers tasks by ascending numeric priority, then by duration. It includes a task when it fits the remaining daily time and can still include later, shorter tasks when an earlier task does not fit. It does not search all combinations for an optimal plan.
- **Daily time budget:** The generated plan stays within the owner's available minutes. Tasks that do not fit are listed as omitted, with a reason in the scheduling log.
- **Conflict warnings:** Timed tasks in the generated plan are checked for overlapping intervals on the same due date. Back-to-back tasks are not considered conflicts.
- **Recurring care tasks:** Completing a daily task creates its next occurrence for tomorrow; completing a weekly task creates one for seven days later. One-time tasks do not recur.
- **Task filtering:** Tasks can be filtered by completion status and pet name; pet-name matching is case-insensitive.
- **Care-task tracking:** Owners can add pets and assign each pet care tasks with a category, duration, priority, frequency, due date, and optional scheduled time.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)                                                                                   | Notes                                                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_duration()`, `Scheduler.sort_by_time()`, `Scheduler.generate_schedule()` | Sorts by duration, or by priority then duration when generating the schedule. `sort_by_time()` is a compatibility alias for duration sorting.                   |
| Filtering         | `Owner.filter_tasks()`, `Scheduler.generate_schedule()`                                     | Filters by pet name and/or completion status; scheduling includes each priority-ordered task that fits the remaining daily minutes and omits tasks that do not. |
| Conflict handling | `Scheduler._get_overlap_warnings()`                                                         | Detects and logs overlapping scheduled time slots on the same due date; back-to-back tasks are not treated as overlapping.                                      |
| Recurring tasks   | `Task.mark_complete()`, `Pet.mark_task_complete()`                                          | Completing a daily or weekly task creates its next occurrence; other frequencies do not recur.                                                                  |

## 📸 Demo Walkthrough

1. **Set up the owner.** Launch the Streamlit app, enter the owner's name, and set the number of minutes available for pet care each day.
2. **Add a pet.** In **Add a Pet**, enter a name, choose a species, enter the pet's age, and select **Add pet**. The pet then appears in the pet list.
3. **Create a care task.** In **Schedule a Task**, choose the pet and enter a title, category, duration, priority, scheduled time, and repeat frequency. Select **Add task** to add it to that pet's pending tasks.
4. **Review and manage pending tasks.** The pending-task table can show all pets or one selected pet, and displays tasks shortest-duration-first. Use **Complete** to mark a task done; daily and weekly tasks create their next occurrence for tomorrow or seven days later, while one-time tasks do not recur.
5. **Generate a plan.** Set the daily time budget and select **Generate schedule**. The scheduler considers tasks by priority (1 is highest), then duration; it includes each task that fits the remaining minutes and lists tasks that do not fit, with a reason. This is a greedy selection, not a search for the globally optimal combination.
6. **Check conflicts and reasoning.** Review the plan's included and omitted tasks and the scheduler log. If scheduled tasks in the plan overlap on the same due date, the app displays conflict warnings; tasks that meet exactly end-to-start are not considered overlapping. Adjust a task's time or duration to resolve a warning.

The CLI example below is produced by running `main.py`. It demonstrates duration sorting, filtering, the 60-minute budget, omitted tasks, and an overlap warning. The warning date is the run date.

```text
🔀 TASKS SORTED BY DURATION:
  • [Health] Give Luna Joint Supplement (5m)
  • [Grooming] Groom Milo's Fur (15m)
  • [Enrichment] Extended Dog Park Play (25m)
  • [Exercise] Luna Neighborhood Walk (30m)

🔎 FILTERED TASKS (Pending, Luna):
  • [Enrichment] Extended Dog Park Play (25m)
  • [Health] Give Luna Joint Supplement (5m)
  • [Exercise] Luna Neighborhood Walk (30m)

✅ FILTERED TASKS (Completed, Milo):
  • [Feeding] Milo's Morning Feeding (10m)
=============================================
       PAWPAL+ DAILY SCHEDULE FOR ALEX
   Daily Time Budget: 60 minutes
=============================================

✅ SCHEDULED TASKS:
  • [Health] Give Luna Joint Supplement (5m) at 09:00 - Priority 1
  • [Exercise] Luna Neighborhood Walk (30m) at 09:00 - Priority 2
  • [Grooming] Groom Milo's Fur (15m) - Priority 3

Total Scheduled Time: 50 / 60 mins

⚠️ OMITTED TASKS (Over Budget):
  • [Enrichment] Extended Dog Park Play (25m) - Priority 4

📋 SCHEDULER LOG / REASONING:
  - Included 'Give Luna Joint Supplement' (5m) - Priority 1.
  - Included 'Luna Neighborhood Walk' (30m) - Priority 2.
  - Included 'Groom Milo's Fur' (15m) - Priority 3.
  - Omitted 'Extended Dog Park Play' (25m) - Exceeds daily limit of 60m.
  ⚠️ Warning: 'Give Luna Joint Supplement' and 'Luna Neighborhood Walk' overlap on 2026-10-18 at 09:00 and 09:00.
=============================================
```
