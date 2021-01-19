all: generic noyb
	@echo "Done"

generic:
	$(PYTHON) generic_csv_exporter.py --loglevel INFO --source ${DATA_SOURCE}

noyb:
	$(PYTHON) noyb_exporter.py --loglevel INFO
