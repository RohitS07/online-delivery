---
id: NFR-0001
title: API requests from the app time out
type: nfr
domain: platform
status: review
budget: 10 seconds per request
enforced_by: US-0002 acceptance criteria AC-0002-04 and AC-0002-05
---

# NFR-0001 — API requests from the app time out

Every request the app sends to the API gives up after 10 seconds. A request with no time limit
can leave the visitor waiting forever on a screen that says "checking" or "loading".

**How it is checked.** The app's shared API client sets the limit once. A test checks the client's
limit is 10 seconds, and a test with fake timers checks that a request with no answer ends as unreachable.
Both are acceptance criteria of [US-0002](../stories/US-0002-a-visitor-sees-one-clear-api-status.md).

**What a failure means.** A request that runs past the limit is treated as a failed request, and
the screen that made it shows its error state. A slower budget for one endpoint, such as a PDF
download, is a new NFR, not a change to this one.
