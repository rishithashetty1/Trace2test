#!/usr/bin/env bash

set -euo pipefail

TEST_FILE="./trace2test/tests/test_payment_crash.py"
SERVICE_FILE="./trace2test/payment_service.py"
BACKUP_FILE="./trace2test/payment_service.py.bak"
CRASH_LOG="./trace2test/crash.log"

if [ -f "$TEST_FILE" ]; then
  rm "$TEST_FILE"
  echo "Deleted $TEST_FILE"
else
  echo "No test file to delete"
fi

if [ -f "$BACKUP_FILE" ]; then
  cp "$BACKUP_FILE" "$SERVICE_FILE"
  echo "Restored buggy payment_service.py from backup"
else
  echo "No backup found; keeping current payment_service.py"
fi

set +e
python3 "$SERVICE_FILE"
EXIT_CODE=$?
set -e

if [ -f "$CRASH_LOG" ]; then
  echo "crash.log created successfully"
else
  echo "crash.log was not created"
  exit 1
fi

exit 0

# Made with Bob
