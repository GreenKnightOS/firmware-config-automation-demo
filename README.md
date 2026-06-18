# Firmware Config Automation Demo

A Python automation tool that updates hard-coded values in a C firmware configuration file using engineering specifications from a JSON file.

## Why This Project Exists

Firmware and embedded software projects often contain configuration values such as voltage limits, current limits, calibration gains, temperature cutoffs, and timing values.

Manually updating those values can be slow and error-prone.

This demo shows how a simple automation workflow can:

* Read engineering specs from a JSON file
* Update matching `#define` values in a C source file
* Create a backup before making changes
* Validate that the updates were applied correctly
* Generate a validation report

## Project Files

```text
firmware-config-automation-demo/
├── specs.json
├── firmware_config.c
├── update_config.py
├── validation_report.txt
├── backups/
└── README.md
```

## Example Input

```json
{
  "voltage_limit": 12.5,
  "current_limit": 3.2,
  "calibration_gain": 1.08,
  "temperature_cutoff": 85,
  "startup_delay_ms": 500
}
```

## Example Firmware Config

```c
#define VOLTAGE_LIMIT 10.0
#define CURRENT_LIMIT 2.5
#define CALIBRATION_GAIN 1.00
#define TEMP_CUTOFF 75
#define STARTUP_DELAY_MS 250
```

## What the Script Does

Running `update_config.py` updates the C file using the values from `specs.json`.

It also creates a timestamped backup and writes a validation report.

## How to Run

```bash
python update_config.py
```

## Skills Demonstrated

* Python scripting
* File automation
* JSON parsing
* Regular expressions
* C configuration file editing
* Backup generation
* Validation reporting
* Engineering workflow automation

## Future Improvements

* Add unit tests
* Add command-line arguments
* Support multiple firmware files
* Add safer dry-run mode
* Add optional AI-assisted spec extraction
