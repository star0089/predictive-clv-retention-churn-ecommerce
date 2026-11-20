"""Run the complete Olist analytics workflow from the repository root."""
import argparse
import json
from src.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Olist CLV, retention and churn analytics.")
    parser.add_argument("--data-dir", default="data_raw", help="Folder containing Olist CSV files.")
    parser.add_argument("--output-dir", default="outputs", help="Folder for generated analytical tables.")
    parser.add_argument("--model-dir", default="models", help="Folder for fitted model artifacts.")
    parser.add_argument("--analysis-end", default="2018-08-31 23:59:59",
                        help="Last timestamp included in analysis; default excludes sparse dataset tail.")
    args = parser.parse_args()
    summary = run_pipeline(args.data_dir, args.output_dir, args.model_dir, args.analysis_end)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
