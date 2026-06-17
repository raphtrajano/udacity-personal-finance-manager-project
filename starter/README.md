# Design pattern reflection

In this project, we implemented four design patterns: Singleton, Adapter, Observer, and Strategy (this last one chosen by me).

**Singleton** is important to guarantee that only one instance is created, avoiding duplicates. This is essential to prevent conflicts and compromised data. Although it introduces global state, which can make testing and tracking dependencies harder, it helps maintain data integrity, which is crucial in a finance project.

**Adapter** helps us, as the name suggests, adapt one data format into another expected by our system. This is useful for pulling data from different sources and converting it into a single, consistent structure. In this project, it transforms income data from external sources into the expected balance structure our system works with. The trade-off is an extra layer of abstraction, since every new data source requires writing a new adapter, which adds maintenance overhead as sources grow.

**Observer** deals with notifications and is event-driven. It's useful for tracking specific events and triggering an action when an expected condition is met. In this project, it notifies users when a threshold is reached, alerting them that a safe limit has been surpassed. One challenge here was making sure observers don't introduce tight coupling with the subject, since too much logic leaking into the notification step can make it harder to keep the subject simple and decoupled.

**Strategy** is useful when we want to apply a different algorithm without modifying the main logic. I chose this pattern because it allows us to generate different types of net reports without changing the core reporting code. This guarantees flexibility and makes the system easier to test and scale. The trade-off is a bit more upfront complexity, introducing multiple strategy classes even for simpler reporting cases.
