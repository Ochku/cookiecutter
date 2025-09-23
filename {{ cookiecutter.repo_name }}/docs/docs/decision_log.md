# Decision Log

## Use API X with Model 1 instead of API Y with Model 2

**Date:** 2025-05-10  
**Status:** Accepted

---

### Context

We needed to integrate an external service to perform [describe task, e.g., “text classification” or “data enrichment”]. There were two main options:

- **API X with Model 1:** Modern API with fast response times, strong Python support, and high accuracy on our test dataset.
- **API Y with Model 2:** More established service, but slower, higher latency, and less flexible integration with our stack.

We evaluated both APIs based on:
- Accuracy on domain-specific test cases
- Response speed
- Cost
- Python client support
- API reliability and documentation

---

### Decision

We chose to proceed with **API X using Model 1** due to:
- Higher prediction accuracy (+7% F1 score on validation data)
- Lower latency (avg. 350ms vs. 900ms)
- Simpler integration with our Python backend
- Transparent pricing and better documentation

Although API Y had more enterprise features, they were not essential for our current use case.

---

### Consequences

- Immediate performance gains and improved prediction quality
- Reduced integration effort due to Python-native client
- Tied to a smaller, less mature vendor — may need reevaluation if we scale or require SLAs
- Future codebase may need to abstract model-specific logic to allow easy switching

