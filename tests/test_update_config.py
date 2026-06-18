import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import update_config


class TestFirmwareConfigAutomation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name)

        self.specs_file = self.project_dir / "specs.json"
        self.firmware_file = self.project_dir / "firmware_config.c"
        self.backup_dir = self.project_dir / "backups"
        self.report_file = self.project_dir / "validation_report.txt"

        self.specs_file.write_text(
            json.dumps(
                {
                    "voltage_limit": 12.5,
                    "current_limit": 3.2,
                    "calibration_gain": 1.08,
                    "temperature_cutoff": 85,
                    "startup_delay_ms": 500,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        self.firmware_file.write_text(
            """// firmware_config.c
#define VOLTAGE_LIMIT 10.0
#define CURRENT_LIMIT 2.5
#define CALIBRATION_GAIN 1.00
#define TEMP_CUTOFF 75
#define STARTUP_DELAY_MS 250
""",
            encoding="utf-8",
        )

        self.original_paths = {
            "SPECS_FILE": update_config.SPECS_FILE,
            "FIRMWARE_FILE": update_config.FIRMWARE_FILE,
            "BACKUP_DIR": update_config.BACKUP_DIR,
            "REPORT_FILE": update_config.REPORT_FILE,
        }

        update_config.SPECS_FILE = self.specs_file
        update_config.FIRMWARE_FILE = self.firmware_file
        update_config.BACKUP_DIR = self.backup_dir
        update_config.REPORT_FILE = self.report_file

    def tearDown(self):
        update_config.SPECS_FILE = self.original_paths["SPECS_FILE"]
        update_config.FIRMWARE_FILE = self.original_paths["FIRMWARE_FILE"]
        update_config.BACKUP_DIR = self.original_paths["BACKUP_DIR"]
        update_config.REPORT_FILE = self.original_paths["REPORT_FILE"]

        self.temp_dir.cleanup()

    def test_load_specs_reads_json_values(self):
        specs = update_config.load_specs()

        self.assertEqual(specs["voltage_limit"], 12.5)
        self.assertEqual(specs["current_limit"], 3.2)
        self.assertEqual(specs["calibration_gain"], 1.08)
        self.assertEqual(specs["temperature_cutoff"], 85)
        self.assertEqual(specs["startup_delay_ms"], 500)

    def test_create_backup_creates_backup_file(self):
        backup_file = update_config.create_backup()

        self.assertTrue(backup_file.exists())
        self.assertIn("firmware_config_backup", backup_file.name)

    def test_update_firmware_config_updates_c_defines(self):
        specs = update_config.load_specs()

        update_config.update_firmware_config(specs)

        updated_text = self.firmware_file.read_text(encoding="utf-8")

        self.assertIn("#define VOLTAGE_LIMIT 12.5", updated_text)
        self.assertIn("#define CURRENT_LIMIT 3.2", updated_text)
        self.assertIn("#define CALIBRATION_GAIN 1.08", updated_text)
        self.assertIn("#define TEMP_CUTOFF 85", updated_text)
        self.assertIn("#define STARTUP_DELAY_MS 500", updated_text)

    def test_validate_updates_passes_after_update(self):
        specs = update_config.load_specs()

        update_config.update_firmware_config(specs)
        validation_results = update_config.validate_updates(specs)

        validation_text = "\n".join(str(result) for result in validation_results)

        self.assertIn("PASS", validation_text)
        self.assertNotIn("FAIL", validation_text)


if __name__ == "__main__":
    unittest.main()
