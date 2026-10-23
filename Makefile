.PHONY: check check-seip pipeline clean
PY ?= python3 -B
check: check-seip
check-seip:
	cd analysis && $(PY) check_seip.py
pipeline:
	pipeline/run_pipeline.sh --dry-run
clean:
	rm -rf pipeline/work analysis/__pycache__
