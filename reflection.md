# PawPal+ Project Reflection

## 1. System Design

> Document three core actions a user should be able to perform

A user should be able to
1. Build a user profile
2. Add, edit, remove pet care tasks for a given pet
3. Add, edit, remove pets associated with their profile

**a. Initial design**

> Briefly describe your initial UML design.

My UML diagram is represented by [uml_draft.mmd](./diagrams/uml_draft.mmd).
To reduce clutter, all standard getter and setter methods are omitted from the UML model but will exist in the implementation.

At a high level, an `Owner` has a collection of `Pets`, each with prioritized `Tasks` and a `RecurrencePattern` those tasks need to be completed on for a given pet. `Owners` also have an available hours window with the ability to prevent certain times in the day from being scheduled (by creating a preventative `OwnerOwnerScheduleBlock`) or creating preferred time blocks to be filled with `TaskScheduleBlocks`. Since `Tasks` can be assigned across multiple `Schedules`, the abstract `ScheduleBlock` class acts as a joiner to the individual `Schedules` which are specific to a certain day.

>  What classes did you include, and what responsibilities did you assign to each?

* `Owner` - Represents a user/owner and stores their related pet configuration
* `Pet` - Represents a pet and relates to the collection of `Tasks` required by the pet
* `Task` - This is the action an owner must complete (walk the dog, feed the bird, etc.) and stores task-related information to be used during schedule generation
* `Scheduler` - This is an internal service/factory class which holds the logic to generate the schedule
* `Schedule` - This is the complete schedule for the given day with the various `ScheduleBlocks` mapped.
* `ScheduleBlock` - This is an abstract representation of a calendar timeslot and can be created by the system to assign a task to complete or by a user to represent a non-scheduleable time window. It has an abstract methods of `get_timedelta()` and `        +is_completed()` which are overridden by the `OwnerScheduleBlock` and `TaskScheduleBlock` classes.

**b. Design changes**

> Did your design change during implementation?
> If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

> What constraints does your scheduler consider (for example: time, priority, preferences)?
> How did you decide which constraints mattered most?

**b. Tradeoffs**

> Describe one tradeoff your scheduler makes.
> Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

> How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
> What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

> Describe one moment where you did not accept an AI suggestion as-is.
> How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

> What behaviors did you test?
> Why were these tests important?

**b. Confidence**

> How confident are you that your scheduler works correctly?
> What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

> What part of this project are you most satisfied with?

**b. What you would improve**

> If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

> What is one important thing you learned about designing systems or working with AI on this project?
