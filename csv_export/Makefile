all: generic noyb
	@echo "CSV Done"

generic:
	$(PYTHON) generic_csv_exporter.py --loglevel ${LOGLEVEL} --source ${DATA_SOURCE}

noyb:
	$(PYTHON) noyb_exporter.py --loglevel ${LOGLEVEL}
