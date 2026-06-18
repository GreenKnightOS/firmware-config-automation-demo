# Firmware Config Automation Demo

A Python automation tool that updates hard-coded values in a C firmware configuration file using engineering 
specifications from a JSON file.

## Why This Project Exists

Firmware and embedded software projects often contain configuration values such as voltage limits, current limits, 
calibration gains, temperature cutoffs, and timing values.

Manually updating those values can be slow and error-prone.

This demo shows how a simple automation workflow can:

* Read engineering specs from a JSON file
* Update matching `#define` values in a C source file
* Create a backup before making changes
* Validate that the updates were applied correctly
* Generate a validation report
## Use Case

This project demonstrates how engineering configuration work can be automated to reduce manual editing errors.

A workflow like this could be used when engineers need to update firmware constants from approved product specifications
, calibration data, or datasheet-style values. Instead of manually editing hard-coded C values, the tool reads 
structured JSON input, updates the matching firmware definitions, creates a backup, validates the changes, and 
generates a report.
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
## Product-Style Example

This project includes a product-style specs example at `examples/ds_mini_specs_example.json`.

The example shows how real datasheet-style values such as nominal input power, supply voltage, current limit, 
temperature stability, operating frequency, and MTTF could be represented in structured JSON before being used in an 
automation workflow.

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

## How to Run Tests

```bash
python -m unittest tests/test_update_config.py
```

The test suite checks that the tool can:

* Read values from `specs.json`
* Create a backup of the firmware file
* Update C `#define` values correctly
* Validate that the updated values were applied


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
