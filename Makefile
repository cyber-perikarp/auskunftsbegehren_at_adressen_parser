PYTHON = python3
DATA_SOURCE = ~/auskunftsbegehren_at_adressen
SOURCE_REPO = https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen
LOGLEVEL = INFO
export

.PHONY: default
default:
	@echo "pls specify target"

prepare:
	rm -rf upload
	mkdir -p upload/qrcodes

fetch:
	bash data/update.sh

checkplz:
	$(MAKE) -C check all

csv:
	$(MAKE) -C csv_export all
