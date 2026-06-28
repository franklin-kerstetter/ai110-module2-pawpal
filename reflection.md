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

The design didn't change dramatically.
Conceptually it is the same, but there were a couple tweaks made.

> If yes, describe at least one change and why you made it.

One change that was added were missing relationship representations.
Those were not added from the UML diagram during the initial AI-built skeleton.
This second pass allowed Claude to catch that they were missing, letting it more accurately build the desired model.

Another change was a migration in logic. Claude recommended having `applies_to_date(target_date)` logic directly on the `RecurrencePattern`, which it then implemented.

Additionally, I made a call to allow for specifying a `TimeOfDay` rather than requiring strict times. This offered a less conflict-heavy approach to users, delegating time scheduling to the system rather than forcing them to track exact times or experience post-setup validations. This was my preferred method for schedule generation as it allowed time-range scheduling instead of strict time scheduling.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

> What constraints does your scheduler consider (for example: time, priority, preferences)?

My schedule considers time,  priority, and available hours.
As a product choice, I've built this around time-ranges instead of strict times. There is the option for explicit times, but it's designed more in favor of allowing the schedule to setup the best times rather than already having a schedule.

> How did you decide which constraints mattered most?

The goal is to make the best product for the end user and their pets.
Thus, whenever determining which task to schedule, the algorithm checks time of day, priority, and then pet age as younger pets are more resillient to missed tasks.


**b. Tradeoffs**

> Describe one tradeoff your scheduler makes.

One tradeoff the scheduler makes is that it is built more around task time ranges (i.e. morning, midday, evening, and night) instead of strict times.
This is to promote schedule flexibility and reduce missed tasks or conflicts.

> Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because, in my view, an end user who has all strict times for their tasks already has their schedule. They wouldn't need a scheduling application, they would need a notepad. I made the tradeoff to build a schedule generator for users who know they need to complete tasks throughout the day, but don't know the best way to assign times to complete them all.

---

## 3. AI Collaboration

**a. How you used AI**

> How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

AI was used heavily throughout this project.

One use was as a sounding board for the initial design. Although I did design it independently first, I had it evaluate and question the design for resiliency and scalability.

Claude was incredibly helpful during the implementation.
Specifically, it implemented all of the core algorithms (such as [generate_schedule](./pawpal_system.py#673)) and the various schedule printing formatting.

Lastly, as more requirements arose, it was instrumental in refactoring the code. This saved an immense amount of time. For example, having it add 1-line docstrings was really helpful as it saved me the monotonous work of doing so.

> What kinds of prompts or questions were most helpful?

Most of my prompting worked in 2 passes.
First, I'd start generic to get at least an algorithmic framework in place.
Second, I'd ask for specific alterations or enhancements to the newly added code.
I found that working from actual code was much more easy to follow and evaluate than re-prompting from suggestions. This combined with frequent git commits made tracking updates far easier.

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
