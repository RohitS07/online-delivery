---
id: SKILL-0002
title: Write a user story
type: skill
status: accepted
---

# SKILL-0002 — Write a user story

1. Scaffold it with `make new TYPE=US TITLE="..."`.
2. Name the one business process it belongs to, in `bpm:`. A story spanning two processes is two stories.
3. Write it from one actor's point of view, covering one slice of the process.
4. Write acceptance criteria as a table, one row each, in given, when, then form.
5. Every criterion gets a `verified_by` binding to a test or an eval, such as `test:path/to/test_file.py::test_name`. A criterion nothing checks is a wish. This is the gate that makes the whole chain real.
6. Add the story id to the process's `stories:` list.
7. Move the process to `accepted` only when its stories cover it.

**Gate.** `make fix && make harness-check`, coverage gate.
