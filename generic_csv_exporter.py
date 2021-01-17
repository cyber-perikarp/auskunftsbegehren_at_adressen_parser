#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
parser.add_argument("--source", help="Path to inventory.csv. Default ~/auskunftsbegehren_at_adressen")
args = vars(parser.parse_args())

# Logging
loglevelFromCli = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
jsonLogFromCli = args["jsonlog"].upper() if args["jsonlog"] else "N"
logzero.loglevel(loglevelFromCli)

# Do we want to log as json?
if (jsonLogFromCli == "Y" or jsonLogFromCli == "YES"):
    logzero.json()

log.debug("Command Line Parameters: {0}".format(args))

# This is the current folder
workDir = os.path.dirname(os.path.realpath(__file__))

# Defaults
sourceFolder = args["source"] if args["source"] else "~/auskunftsbegehren_at_adressen"
log.info("Source folder: {0}".format(sourceFolder))

# Hardcoded Paramaters
outFile = workDir + "/upload/generic.csv"
csvHeader = ["Name", "Name_Lang", "Branche", "Typ", "Adresse", "PLZ", "Ort", "Ebene", "E-Mail", "Homepage", "Tel", "Fax", "Datenquelle", "Pruefung"]
foldersToIgnore = [".", "..", "upload", ".git", "docs"]
administrationLevels = {
    "bund": "Bund",
    "burgenland": "Burgenland",
    "kaernten": "Kärnten",
    "niederoesterreich": "Niederösterreich",
    "oberoesterreich": "Oberösterreich",
    "privat": "Privat",
    "salzburg": "Salzburg",
    "steiermark": "Steiermark",
    "tirol": "Tirol",
    "vorarlberg": "Vorarlberg",
    "wien": "Wien"
}

# read in file with plz
plzFile = open(workDir + "/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzFile)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

# remove spaces etc from phone number
def sanitizePhoneNumber(number):
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("/", "")
    number = number.replace("(", "")
    number = number.replace(")", "")
    number = number.replace("'", "") # Wegen LibreOffice
    number = number.replace("‘", "") # Auch wegen LibreOffice
    log.debug("Sanitized Phone Number: {0}".format(number))
    return number

# Are all required fields filled?
def checkIfFullRecord(record):
    if (not record["Id"]
        or not record["Name"]
        or not record["Name_Lang"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Pruefung"]):
            log.error("Not exporting: {0}".format(record["Name"]))
            return False
    return True

def populateGeneratedFields(record):
    record["Tel"] = sanitizePhoneNumber(record["Tel"])
    record["Fax"] = sanitizePhoneNumber(record["Fax"])

    # plz from db
    record["Ort"] = plz[record["PLZ"]][0]

    record["Ebene"] = ' '.join([administrationLevels.get(i, i) for i in record["Ordner"].split()])

    log.debug("Found city: {0}".format(record["Ort"]))

    return record

# Write Header
try:
    with open(outFile, "w") as outFileHandler:
        log.debug("Headers: {0}".format(str(csvHeader)))
        writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader, quoting=csv.QUOTE_ALL)
        writer.writeheader()
except IOError:
    log.critical("Cant write to file!")
    exit(1)

log.debug(os.listdir(sourceFolder))

recordsToWrite = []
# Iterate through all folders exept the ones we want to ingore
for folder in [x for x in os.listdir(sourceFolder) if (os.path.isdir(sourceFolder + "/" + x) and x not in foldersToIgnore)]:
    log.debug("Folder: {0}".format(folder))
    # Load the csvs
    for csvFile in [x for x in os.listdir(sourceFolder + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # path to the file
        csvFile = sourceFolder + "/" + folder + "/" + csvFile
        log.info("Using File: {0}".format(csvFile))

        # read the file
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                record["Ordner"] = folder # we need this field later for sorting

                # only insert records that have the required fields
                if (checkIfFullRecord(record)):
                    log.debug("Processing entry: {0}".format(record["Name"]))
                    record = populateGeneratedFields(record)
                    log.debug(record)
                    recordsToWrite.append(record)

sortedRecords = sorted(recordsToWrite, key = lambda tup: (
            strxfrm(tup["Ordner"].lower()),
            strxfrm(tup["Branche"].lower()),
            strxfrm(tup["Typ"].lower()),
            strxfrm(tup["Name"].lower()))
        )

log.debug(sortedRecords)

for entry in sortedRecords:
    # write the csv
    try:
        with open(outFile, "a+") as outFileHandler:
            del entry["Ordner"]
            del entry["Id"]

            log.debug("Writing entry: {0}".format(entry["Name"]))

            writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader, quoting=csv.QUOTE_ALL)
            writer.writerow(entry)

    except IOError:
        log.critical("Cant write to file!")
        exit(1)
