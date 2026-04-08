# Trace2Fix Prompt Pack

This file contains the literal saved prompts for the Trace2Fix workflow.

## Prompt 1 — RCA
```text
Read the file crash.log in the current workspace. Identify the error type, the exact function and line that failed, the input values that triggered it, and the root cause in plain English.
```

## Prompt 2 — Test generation
```text
Based on the crash you just analyzed, write a pytest file called test_payment_crash.py that imports process_payment from payment_service.py, calls it with the exact inputs that caused the crash, and asserts that the correct exception is raised. Save the file to the workspace.
```

## Prompt 3 — Verify
```text
Run pytest test_payment_crash.py -v in the terminal and show me the output.
```

## Prompt 4 — Fix
```text
Suggest the minimal code change to fix this bug. Then apply it to payment_service.py and re-run the test.
```

## Prompt 1+2 Fallback — RCA and test generation together
```text
Read the file trace2test/crash.log in the current workspace. Identify the error type, the exact function and line that failed, the input values that triggered it, and the root cause in plain English. Then write a pytest file at trace2test/tests/test_payment_crash.py that imports process_payment from trace2test/payment_service.py, reproduces the crash using the same inputs, and asserts the correct exception is raised. Make sure the import works from the tests subfolder.
```

## Recommended Usage
- Run Prompt 1 after generating or receiving `crash.log`
- Run Prompt 2 after RCA is confirmed
- If context retention looks weak in chat, use the combined Prompt 1+2 fallback instead
- Run Prompt 3 to validate the regression test behavior
- Run Prompt 4 to apply and verify the minimal fix

## Current Workspace Mapping
Because this project uses a nested structure, adapt filenames to these paths when executing the prompts in this workspace:
- `crash.log` → `trace2test/crash.log`
- `payment_service.py` → `trace2test/payment_service.py`
- `test_payment_crash.py` → `trace2test/tests/test_payment_crash.py`

## Live Demo Guidance
- Keep [trace2test/payment_service.py](trace2test/payment_service.py) and [trace2test/tests/test_payment_crash.py](trace2test/tests/test_payment_crash.py) visible during the demo
- Use `python3 -m pytest ./trace2test/tests/test_payment_crash.py -v` instead of plain `pytest` to reduce environment-path issues
- Mention that the workspace is nested, so the test file adjusts `sys.path` to import [`process_payment`](trace2test/payment_service.py:1) correctly
- If you want the cleanest narrative, explain that [trace2test/crash.log](trace2test/crash.log) preserves the original failure while the current code reflects the post-fix state

## Workspace Note
The original prompt-product guidance preferred a flat directory for simpler imports. In this workspace, imports are handled in the test file by adjusting `sys.path`, so the prompts remain reusable without restructuring the project.

## Rehearsal Checklist
- Run the flow end-to-end before the live demo
- Time the demo and keep it under 3 minutes if possible
- Verify that [`python3 -m pytest`](trace2test/tests/test_payment_crash.py:1) works in the active environment
- Keep the terminal open so the pytest output is immediately visible
- Be ready to explain the import-path adjustment in [test_payment_crash.py](trace2test/tests/test_payment_crash.py)
- If the full fix-and-rerun flow feels too long, stop after showing the fix suggestion and test file
- Known live risks:
  - import-path mistakes in nested layouts
  - missing `pytest` in the active interpreter
  - confusion between pre-fix crash data and post-fix code behavior
  - context loss between separate prompts