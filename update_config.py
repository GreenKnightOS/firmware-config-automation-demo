import json
import sys
import re
from pathlib import Path


PROJECT_DIR = Path(__file__).parent

import json
import re
import shutil
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).parent

SPECS_FILE = PROJECT_DIR / "specs.json"
FIRMWARE_FILE = PROJECT_DIR / "firmware_config.c"
BACKUP_DIR = PROJECT_DIR / "backups"
REPORT_FILE = PROJECT_DIR / "validation_report.txt"


SPEC_TO_C_DEFINE = {
    "voltage_limit": "VOLTAGE_LIMIT",
    "current_limit": "CURRENT_LIMIT",
    "calibration_gain": "CALIBRATION_GAIN",
    "temperature_cutoff": "TEMP_CUTOFF",
    "startup_delay_ms": "STARTUP_DELAY_MS",
}


def load_specs():
    if not SPECS_FILE.exists():
        raise FileNotFoundError(f"Missing specs file: {SPECS_FILE}")

    try:
        with open(SPECS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in specs.json: {error}") from error


def create_backup():
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"firmware_config_backup_{timestamp}.c"

    shutil.copy2(FIRMWARE_FILE, backup_file)

    return backup_file


def update_firmware_config(specs):
    firmware_text = FIRMWARE_FILE.read_text(encoding="utf-8")
    changes = []

    for spec_key, c_define in SPEC_TO_C_DEFINE.items():
        new_value = specs[spec_key]

        pattern = rf"^#define\s+{c_define}\s+(.+)$"
        match = re.search(pattern, firmware_text, flags=re.MULTILINE)

        if not match:
            changes.append(f"{c_define}: FAILED - define not found")
            continue

        old_value = match.group(1).strip()
        new_line = f"#define {c_define} {new_value}"

        firmware_text = re.sub(
            pattern,
            new_line,
            firmware_text,
            flags=re.MULTILINE
        )

        changes.append(f"{c_define}: {old_value} -> {new_value}")

    FIRMWARE_FILE.write_text(firmware_text, encoding="utf-8")

    return changes


def validate_updates(specs):
    firmware_text = FIRMWARE_FILE.read_text(encoding="utf-8")
    results = []

    for spec_key, c_define in SPEC_TO_C_DEFINE.items():
        expected_value = str(specs[spec_key])
        pattern = rf"^#define\s+{c_define}\s+{re.escape(expected_value)}$"

        passed = re.search(pattern, firmware_text, flags=re.MULTILINE) is not None

        if passed:
            results.append(f"{c_define}: PASS")
        else:
            results.append(f"{c_define}: FAIL")

    return results


def write_report(backup_file, changes, validation_results):
    lines = []

    lines.append("Firmware Config Update Report")
    lines.append("=" * 38)
    lines.append(f"Backup created: {backup_file}")
    lines.append("")

    lines.append("Changes")
    lines.append("-" * 38)
    lines.extend(changes)
    lines.append("")

    lines.append("Validation")
    lines.append("-" * 38)
    lines.extend(validation_results)
    lines.append("")

    if all("PASS" in result for result in validation_results):
        lines.append("Final Result: SUCCESS")
    else:
        lines.append("Final Result: FAILED")

    report_text = "\n".join(lines)

    REPORT_FILE.write_text(report_text, encoding="utf-8")

    return report_text


def main():
    print("Starting firmware config update...")

    try:
        specs = load_specs()
        backup_file = create_backup()
        changes = update_firmware_config(specs)
        validation_results = validate_updates(specs)
        report_text = write_report(backup_file, changes, validation_results)

        print()
        print(report_text)

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit(1)

    except ValueError as error:
        print(f"ERROR: {error}")
        sys.exit(1)

    except KeyError as error:
        print(f"ERROR: Missing required spec value: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()