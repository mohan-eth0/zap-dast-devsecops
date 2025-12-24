#!/bin/bash
set -e

./scripts/zap-healthcheck.sh
./scripts/run-baseline.sh
./scripts/run-full-scan.sh
