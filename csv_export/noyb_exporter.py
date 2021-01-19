#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################
# https://www.mydatadoneright.eu/ #
###################################

import csv
import argparse
import sys
import os
import logzero
from logzero import logger as log
from locale import strxfrm

#### Config ####
# CLI Params
parser = argparse.ArgumentParser("generic_csv_exporter.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL. Default INFO")
parser.add_argument("--jsonlog", help="Log output as JSON. Default no")
args = vars(parser.parse_args())

# Logging
loglevelFromCli = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
jsonLogFromCli = args["jsonlog"].upper() if args["jsonlog"] else "N"
logzero.loglevel(loglevelFromCli)

# Do we want to log as json?
if (jsonLogFromCli == "Y" or jsonLogFromCli == "YES"):
    logzero.json()

log.debug("Command Line Parameters: {0}".format(args))

# workDir is the parent folder
workDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Defaults
sourceFile = workDir + "/upload/generic.csv"

# Hardcoded Parameters
outFile = workDir + "/upload/noyb.csv"
csvHeader = ["status", "id", "display_name", "legal_name", "url", "department", "street_address", "city", "neighbourhood", "postal_code", "region", "country", "requires_identification", "operating_countries", "custom_identifier", "identifiers", "generic_url", "generic_email", "generic_note", "access_url", "access_email", "access_note", "deletion_url", "deletion_email", "deletion_note", "portability_url", "portability_email", "portability_note", "correction_url", "correction_email", "correction_note"]

def checkIfFullRecord(record):
    if (not record["Name"]
        or not record["Name_Lang"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Pruefung"]
        or not record["E-Mail"]):
            log.error("Not exporting: {0}".format(record["Name"]))
            return False
    return True

def populateGeneratedFields(record):
    recordToReturn = {}

    # Felder für noyb
    recordToReturn["status"] = ""
    recordToReturn["id"] = ""
    recordToReturn["display_name"] = record["Name"]
    recordToReturn["legal_name"] = record["Name_Lang"]
    recordToReturn["url"] = record["Homepage"]
    recordToReturn["department"] = ""
    recordToReturn["street_address"] = record["Adresse"]
    recordToReturn["city"] = record["Ort"]
    recordToReturn["neighbourhood"] = ""
    recordToReturn["postal_code"] = record["PLZ"]
    recordToReturn["region"] = record["Bundesland"]
    recordToReturn["country"] = "AT"
    recordToReturn["requires_identification"] = ""
    recordToReturn["operating_countries"] = ""
    recordToReturn["custom_identifier"] = "{0}_{1}_{2}_{3}_{4}".format(record["Branche"], record["Ebene"], record["Ort"].replace(" ", "-"), record["Pruefung"].replace(".", "-"), record["Name"].replace(" ", "-"))
    recordToReturn["identifiers"] = ""
    recordToReturn["generic_url"] = ""
    recordToReturn["generic_email"] = record["E-Mail"]
    recordToReturn["generic_note"] = "Phone: {0}, Fax: {1}".format(record["Tel"], record["Fax"])
    recordToReturn["access_url"] = ""
    recordToReturn["access_email"] = ""
    recordToReturn["access_note"] = ""
    recordToReturn["deletion_url"] = ""
    recordToReturn["deletion_email"] = ""
    recordToReturn["deletion_note"] = ""
    recordToReturn["portability_url"] = ""
    recordToReturn["portability_email"] = ""
    recordToReturn["portability_note"] = ""
    recordToReturn["correction_url"] = ""
    recordToReturn["correction_email"] = ""
    recordToReturn["correction_note"] = ""

    return recordToReturn

# Write Header
try:
    with open(outFile, "w") as outFileHandler:
        log.debug("Headers: {0}".format(str(csvHeader)))
        writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader, quoting=csv.QUOTE_ALL)
        writer.writeheader()
except IOError:
    log.critical("Cant write to file!")
    exit(1)

# read the file
with open(sourceFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)
    for record in readFile:
        # only insert records that have the required fields
        if (checkIfFullRecord(record)):
            log.debug("Processing entry: {0}".format(record["Name"]))
            record = populateGeneratedFields(record)
            log.debug(record)
            try:
                with open(outFile, "a+") as outFileHandler:
                    log.debug("Writing entry: {0}".format(record["display_name"]))

                    writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader, quoting=csv.QUOTE_ALL)
                    writer.writerow(record)

            except IOError:
                log.critical("Cant write to file!")
                exit(1)
