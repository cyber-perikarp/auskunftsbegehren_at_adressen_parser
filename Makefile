PYTHON = python3
DATA_SOURCE = ~/auskunftsbegehren_at_adressen
SOURCE_REPO = https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen
LOGLEVEL = INFO
export

.PHONY: default
default:
	@echo "pls specify target"

clean:
	rm -rf upload

prepare:
	mkdir -p upload/qrcodes

fetch:
	bash data/update.sh $(SOURCE_REPO) $(DATA_SOURCE)

validate:
	$(MAKE) -C check all

csv:
	$(MAKE) -C csv_export all
