PYTHON = python3
DATA_SOURCE = ~/auskunftsbegehren_at_adressen
SOURCE_REPO = https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen
LOGLEVEL = INFO
export

all: validate csv

clean:
	rm -rf upload

prepare: clean
	mkdir -p upload/qrcodes

fetch: prepare
	bash data/update.sh $(SOURCE_REPO) $(DATA_SOURCE)

validate: clean prepare fetch
	$(MAKE) -C check all

csv: validate
	$(MAKE) -C csv_export all
