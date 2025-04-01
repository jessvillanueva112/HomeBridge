#!/bin/bash

echo "Running security scan..."

# Check for outdated packages
echo "Checking for outdated packages..."
pip list --outdated

# Run bandit security check
echo "Running Bandit security check..."
bandit -r .

# Run safety check for known vulnerabilities
echo "Running Safety check..."
safety check

# Check for exposed secrets
echo "Checking for exposed secrets..."
git secrets --scan

# Run dependency check
echo "Running dependency check..."
pip-audit

echo "Security scan complete!" 