#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Prüft die Datensätze gegen die PLZ Datenbank #
################################################

import csv
import os
import argparse

# workDir is the parent folder
workDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Ignore this
foldersToIgnore = [".", "..", "upload", ".git", "docs"]

parser = argparse.ArgumentParser("generic_csv_exporter.py")
parser.add_argument("--source", help="Path to inventory.csv. Default ~/auskunftsbegehren_at_adressen")
args = vars(parser.parse_args())
sourceFolder = args["source"] if args["source"] else "~/auskunftsbegehren_at_adressen"

# Read in the plz database
plzFile = open(workDir + "/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzFile)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

# Iterate through all folders exept the ones we want to ingore
for folder in [x for x in os.listdir(sourceFolder) if (os.path.isdir(sourceFolder + "/" + x) and x not in foldersToIgnore)]:
    # Load the csvs
    for csvFile in [x for x in os.listdir(sourceFolder + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # path to the file
        csvFile = sourceFolder + "/" + folder + "/" + csvFile
        log.info("Using File: {0}".format(csvFile))

        # read the csv and parse it
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                if record["PLZ"]:
                    ort = plz[record["PLZ"]][0] # In case the plz is not in the plz database, this throws an exception and stops the CI

print("All Postleitzahlen are valid!")
