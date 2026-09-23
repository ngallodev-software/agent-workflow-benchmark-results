from pathlib import Path
import sys

from agent_workflow_benchmark.benchmarking.universal_scoring import main

if __name__ == "__main__":
    bundle = Path(__file__).resolve().parent
    raise SystemExit(main(["--bundle", str(bundle), *sys.argv[1:]]))
