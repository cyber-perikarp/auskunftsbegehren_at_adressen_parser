PYTHON = python3
DATA_SOURCE = ~/auskunftsbegehren_at_adressen
export

csv:
	$(MAKE) -C csv_export all
