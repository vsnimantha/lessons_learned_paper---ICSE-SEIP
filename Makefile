.PHONY: check check-seip clean
PY ?= python3 -B
check: check-seip
check-seip:
	cd analysis && $(PY) check_seip.py
clean:
	rm -rf analysis/__pycache__
