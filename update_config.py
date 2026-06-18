import json
import re
from pathlib import Path


PROJECT_DIR = Path(__file__).parent

SPECS_FILE = PROJECT_DIR / "specs.json"
FIRMWARE_FILE = PROJECT_DIR / "firmware_config.c"


SPEC_TO_C_DEFINE = {
    "voltage_limit": "VOLTAGE_LIMIT",
    "current_limit": "CURRENT_LIMIT",
    "calibration_gain": "CALIBRATION_GAIN",
    "temperature_cutoff": "TEMP_CUTOFF",
    "startup_delay_ms": "STARTUP_DELAY_MS",
}


def load_specs():
    with open(SPECS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def update_firmware_config(specs):
    firmware_text = FIRMWARE_FILE.read_text(encoding="utf-8")

    for spec_key, c_define in SPEC_TO_C_DEFINE.items():
        new_value = specs[spec_key]

        pattern = rf"^#define\s+{c_define}\s+(.+)$"
        new_line = f"#define {c_define} {new_value}"

        firmware_text = re.sub(
            pattern,
            new_line,
            firmware_text,
            flags=re.MULTILINE
        )

    FIRMWARE_FILE.write_text(firmware_text, encoding="utf-8")


def main():
    print("Starting firmware config update...")

    specs = load_specs()
    update_firmware_config(specs)

    print("Done. firmware_config.c has been updated from specs.json.")


if __name__ == "__main__":
    main()