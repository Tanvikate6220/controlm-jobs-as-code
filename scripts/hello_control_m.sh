#!/usr/bin/env bash
# ==============================================================================
# Script Name : hello_control_m.sh
# Description : Target script executed by Control-M job HELLO_CONTROL_M
# ==============================================================================

set -euo pipefail

echo "======================================================"
echo "          CONTROL-M JOB EXECUTION STARTED             "
echo "======================================================"
echo "Job Name    : HELLO_CONTROL_M"
echo "Timestamp   : $(date '+%Y-%m-%d %H:%M:%S')"
echo "Executed By : $(whoami)"
echo "Host Machine: $(hostname)"
echo "======================================================"
echo "Hello from Control-M Jobs-as-Code CI/CD Pipeline!"
echo "SUCCESS: Control-M Agent executed the script cleanly."
echo "======================================================"

exit 0
