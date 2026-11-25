
import csv
import hashlib
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def run_pipeline():

    start = time.time()

    # Read YAML configuration
    with open("config.yaml", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Create folders
    output = Path(config["paths"]["output_dir"])
    logs = Path(config["paths"]["log_dir"])

    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    # Configure timestamped logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logging.basicConfig(
        filename=logs / f"run_{timestamp}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )

    logger.info("Pipeline started")

    # Check input file
    input_file = Path(config["paths"]["input"])

    if not input_file.exists():
        logger.error("Input file not found: %s", input_file)
        raise FileNotFoundError(input_file)

    file_hash = hashlib.sha256(input_file.read_bytes()).hexdigest()

    # Read manifest
    manifest_file = Path(config["paths"]["manifest"])

    if manifest_file.exists() and manifest_file.stat().st_size > 0:
        try:
            manifest = json.loads(manifest_file.read_text())
        except json.JSONDecodeError:
            logger.warning(
                "Manifest file is invalid. Starting with an empty manifest."
            )
            manifest = {}
    else:
        manifest = {}

    # Skip previously processed files
    if manifest.get(str(input_file.resolve())) == file_hash:
        logger.info("File already processed. Skipping.")

        summary = {
            "status": "skipped",
            "records_read": 0,
            "records_written": 0,
            "duration_seconds": round(time.time() - start, 3),
        }

    else:
        # Read CSV
        with open(
            input_file,
            encoding=config["csv"]["encoding"],
            newline=""
        ) as file:
            reader = csv.DictReader(
                file,
                delimiter=config["csv"]["delimiter"]
            )
            records = list(reader)

        logger.info("File loaded: %d records", len(records))

        # Validate columns
        required = config["validation"]["required_columns"]

        if not records:
            logger.error("Input file is empty")
            raise ValueError("Input file is empty")

        missing_columns = set(required) - set(records[0])

        if missing_columns:
            logger.error("Missing required columns: %s", missing_columns)
            raise ValueError(f"Missing columns: {missing_columns}")

        # Validate missing values
        threshold = config["validation"]["max_missing_percentage"]

        for column in required:
            missing = sum(
                not (row.get(column) or "").strip()
                for row in records
            )

            missing_percentage = missing / len(records) * 100

            if missing_percentage > threshold:
                logger.error(
                    "Missing value threshold exceeded for column: %s",
                    column
                )
                raise ValueError(
                    f"Too many missing values in {column}"
                )

            if missing > 0:
                logger.warning(
                    "Column %s contains %d missing values",
                    column,
                    missing
                )

        # Apply mappings
        for row in records:
            for column, mapping in config["mappings"].items():
                value = row.get(column)

                if value:
                    row[column] = mapping.get(
                        value.strip().lower(),
                        value
                    )

        # Write CSV
        csv_path = output / config["output"]["csv"]

        with open(
            csv_path,
            "w",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=records[0].keys()
            )
            writer.writeheader()
            writer.writerows(records)

        logger.info("Clean CSV file created")

        # Write JSON
        json_path = output / config["output"]["json"]

        json_path.write_text(
            json.dumps(records, indent=4),
            encoding="utf-8"
        )

        logger.info("Clean JSON file created")

        # Update manifest
        manifest[str(input_file.resolve())] = file_hash

        manifest_file.write_text(
            json.dumps(manifest, indent=4)
        )

        logger.info("Manifest updated")

        summary = {
            "status": "success",
            "records_read": len(records),
            "records_written": len(records),
            "duration_seconds": round(time.time() - start, 3),
        }

    # Save run summary
    summary_path = output / config["output"]["summary"]

    summary_path.write_text(
        json.dumps(summary, indent=4),
        encoding="utf-8"
    )

    logger.info("Pipeline finished: %s", summary["status"])

    return summary
