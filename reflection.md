# PawPal+ Project Reflection

## 1. System Design

The main goal was to let an owner track pet-care tasks and generate a plan that respects a daily time budget and task priorities. The Streamlit interface supports creating pets and tasks, changing the owner's name and available time, completing tasks, and reviewing a generated schedule. Editing or deleting existing pets and tasks is not yet available through the UI, even though some related operations exist in the model classes.

### a. Initial design

My initial UML included `Owner`, `Pet`, `Task`, and a separate `DailyPlan` class. `Owner` stores owner information, the available daily minutes, and a collection of pets. `Pet` stores pet details and its tasks. `Task` stores care-task details such as title, category, duration, priority, and completion state. I initially thought `DailyPlan` should hold the scheduled tasks, omitted tasks, date, and reasoning log.

### b. Design changes

During implementation, I added a separate `Scheduler` so scheduling rules would not be mixed into the data classes, then removed `DailyPlan` from the final design. The scheduler now returns a tuple containing scheduled tasks, omitted tasks, and a reasoning log. This keeps the model focused on the data we actually use and makes scheduler behavior straightforward to test. I also added recurrence and scheduled-time information to `Task`, plus completion and filtering behavior, as the requirements became clearer. Keeping `Scheduler` separate from `Owner`, `Pet`, and `Task` lets those classes represent data and basic operations while the scheduler owns the planning rules.

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

The scheduler considers the owner's available minutes, each task's duration, and numeric priority (1 is highest). It orders tasks by priority and then by shorter duration. It includes a task if it fits in the remaining time; if a task does not fit, it can still consider and include a later, shorter task. For scheduled tasks, it also checks start-time intervals for overlaps on the same due date. Owner preferences beyond the time budget and task priorities are not modeled yet.

### b. Tradeoffs

The scheduler uses a greedy strategy rather than searching every possible combination. This makes its decisions easy to explain and ensures higher-priority tasks are considered first, but it can leave unused minutes or miss a combination that would fit more tasks. I consider this reasonable for pet care because honoring the assigned priorities is more important than maximizing the number of tasks or filling every minute. The app reports which tasks were included or omitted and why, and separately warns about overlapping scheduled times. Tasks whose intervals meet exactly end-to-start are not treated as conflicts.

## 3. AI Collaboration

### a. How I used AI

I used the AI coding assistant to think through the class responsibilities, refine the scheduler rules, identify edge cases for tests, and improve project documentation. The most effective features were iterative, code-aware discussion and assistance with inspecting or changing project files. Asking focused questions—such as how to separate model responsibilities, what should happen when a task does not fit, and how recurring tasks should behave—was more useful than asking for the whole application at once. I verified behavior against the implementation and tests instead of treating generated suggestions as automatically correct.

I kept work organized in separate chat sessions for different phases: design and UML, implementation and testing, then UI and documentation. This helped each conversation stay focused and made it easier to return to the relevant goal without mixing design decisions with later presentation work. I treated the source code, tests, and run output as the shared reference between sessions.

### b. Judgment and verification

One AI-assisted design suggestion I modified was to keep a separate `DailyPlan` class. I chose not to add a class that only wrapped the scheduler's output: the final `Scheduler.generate_schedule()` returns the scheduled list, omitted list, and reasoning log directly. That better matched the project structure and gave the tests concrete return values to check. I also verified the scheduling behavior with tests, including priority and duration ordering, skipping a task that exceeds the remaining budget while allowing a later shorter task, recurrence, and overlap boundaries.

The most important lesson was that I need to act as the lead architect. AI can generate options and code quickly, but I am responsible for deciding what belongs in the system, keeping the design understandable, checking suggestions against requirements, and verifying behavior with tests and actual output. A suggestion is a starting point, not a decision.

## 4. Testing and Verification

### a. What I tested

The test suite covers marking tasks complete; daily and weekly recurrence and one-time completion; adding tasks; sorting by duration without mutating the input; scheduling within a budget and considering later shorter tasks; overlap warnings, including same-time tasks and non-overlapping back-to-back tasks; and filtering by completion status and pet name. These tests matter because recurrence and schedule selection change application state or affect care planning, while boundary tests help avoid false conflict warnings.

### b. Confidence

I am reasonably confident in the core model and scheduler behavior: the project test suite passes (14 tests). I would still test invalid or unusual inputs, such as negative durations, zero or negative budgets passed directly to the scheduler, duplicate task IDs, and tasks whose duration runs past midnight. I would also add UI tests and tests for editing and deleting records. The current app has no persistent database, so state is held in the Streamlit session rather than saved across sessions.

## 5. Reflection

### a. What went well

I am most satisfied that the scheduler has separable, explainable decisions: it accounts for priority and available time, records why tasks were included or omitted, and flags time conflicts. I also covered recurrence and important scheduling edge cases with automated tests, then connected the system to a usable Streamlit interface.

### b. What I would improve

I would add UI flows to edit and delete pets and tasks, and persistent storage so records survive beyond the current session. I would also make the schedule explicitly select tasks due on the chosen date, improve input validation in the model layer, and add tests for those behaviors. If the product needed to optimize time utilization rather than favor priority order, I would evaluate a more advanced selection algorithm and explain that tradeoff to users.

### c. Key takeaway

I learned that good system design is not about adding the most classes or accepting the fastest generated solution. It is about choosing clear responsibilities, stating tradeoffs, and verifying that the implementation actually meets the intended requirements. AI is a powerful collaborator, but the human developer remains accountable for the architecture and the final behavior.
