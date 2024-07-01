import requests
import csv
import os
import re
import json
import logging
from datetime import datetime 

BASE_URL = 'https://karten.nabu.de/insektensommer/data/beobachtungen-'
START_YEAR = 2018
MONTHS = ["august", "juni"]
RANKINGS = ["top100","top5Lebensraeume","top100Bundeslaender"]
DATA_PATH = "src/components/dataimport/seasons/"
IMPORT_PATH = "./seasons/"
BUNDESLAENDER = [
    "Baden-Württemberg",
    "Bayern",
    "Brandenburg & Berlin",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen & Bremen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein & Hamburg",
    "Thüringen"
]
LEBENSRAEUME = [
    "Garten",
    "Balkon",
    "Park",
    "Wiese",
    "Wald",
    "Feld",
    "Teich",
    "Bach/Fluss",
    "Sonstiges"
]
END_YEAR = datetime.now().year
GENERATED_FILES = []

logging.basicConfig(format='[%(asctime)s][%(levelname)s]:%(message)s', datefmt='%d.%m.%y %H:%M:%S', level=logging.INFO)


class Season:
    aktion = {}
    year = 0
    month = ""
    top100 = []
    top100Bundeslaender = []
    top5Lebensraeume = []
    status = 200

    def __init__(self, year, month="juni"):
        if month == "august":
            monthStr = "08"
        else:
            monthStr = "06"

        self.observations, status = self.getAllObservations(year, monthStr)
        if status == 200:
            self.setTop100()
            self.setTop100Bundeslaender()
            self.setTop5Lebensraeume()
            self.year = year
            self.month = month
            self.aktion = self.setAktionValue(monthStr)
        else:
            self.status = status

    def setAktionValue(self, monthStr):
        aktion = {"text":f"{month.capitalize()} {year}", "value":f"{year}-{monthStr}"}
        return aktion

    def getAllObservations(self, year, monthStr):
        observations = []

        r = requests.get(f"{BASE_URL}{year}-{monthStr}.csv")
        lines = (line.decode('utf-8') for line in r.iter_lines())

        for n, row in enumerate(csv.reader(lines)):
            if n == 0:
                header = row
            else:
                observations.append(dict(zip(header, row)))
        
        return observations, r.status_code

    def setTop100(self):
        summarized = {}
        for observation in self.observations:
            summarized = self.updateSummarized(summarized, observation)

        self.top100 = self.sortAndRankList(summarized)

    def setTop100Bundeslaender(self):
        self.top100Bundeslaender = []
        for bundesland in BUNDESLAENDER:
            self.top100Bundeslaender.append({
                "name":bundesland,
                "data":self.getTop100Bundesland(bundesland)
            })

    def getTop100Bundesland(self, bundesland):
        summarized = {}
        for observation in self.observations:
            if observation["bundesland"].strip() == bundesland:
                summarized = self.updateSummarized(summarized, observation)
        
        return self.sortAndRankList(summarized)

    def setTop5Lebensraeume(self):
        self.top5Lebensraeume = []
        for lebensraum in LEBENSRAEUME:
            self.top5Lebensraeume.append({
                "name":lebensraum,
                "data":self.getTop5Lebensraum(lebensraum)
            })

    def getTop5Lebensraum(self, lebensraum):
        summarized = {}
        for observation in self.observations:
            if observation["lebensraum"].strip() == lebensraum:
                summarized = self.updateSummarized(summarized, observation)
    
        return self.sortAndRankList(summarized, 5)

    # BEGIN SECTION HELPER FUNCTIONS

    def updateSummarized(self, summarized, observation):
        '''
            updates the summarized dictionary
            Info:
                Convenience function to avoid redundancy
            Parameters:
            - summarized
            - observation
            Returns:
            - summarized [updated version]
        '''
        if summarized.get(observation["artid"]) is None:
            item = {}
            item["artid"] = observation["artid"]
            item["artname"] = observation["artname"]
            item["taxon"] = observation["taxon"]
            item["gattung"] = observation["gattung"]
            item["anzahl"] = int(observation["anzahl"])
            item["beobachtungen"] = 1
            item["durchschnitt"] = round(item["anzahl"] / item["beobachtungen"], 2)
            summarized[observation["artid"]] = item
        else:
            summarized[observation["artid"]]["anzahl"] += int(observation["anzahl"])
            summarized[observation["artid"]]["beobachtungen"] += 1
            summarized[observation["artid"]]["durchschnitt"] = round(summarized[observation["artid"]]["anzahl"] / summarized[observation["artid"]]["beobachtungen"], 2)
        return summarized

    def sortAndRankList(self, unsortedList, limiter=100):
        '''
            Sorts and Ranks the given unsorted list
            Paramters:
            - unsortedList
            - limiter
            Returns:
            - result
        '''
        result = []
        sortedList = sorted(unsortedList.items(), key=lambda item: item[1]["beobachtungen"], reverse=True)
        sortedList = sortedList[:limiter]

        for n, entry in enumerate(sortedList,1):
            entry[1]["rang"] = n
            result.append(entry[1])
        
        return result

    # END SECTION HELPER FUNCTIONS
    # BEGIN SECTION WRITE FUNCTION
    def writeData(self):
        self.writeLebensraumTop5()
        self.writeBundeslandTop100()
        self.writeTop100()
        GENERATED_FILES.append((self.year, self.month))

    def writeLebensraumTop5(self):
        prefix = f"{self.month}{self.year}"
        writeFile = open(f"{DATA_PATH}{prefix}_top5Lebensraeume.js","w")
        data = json.dumps({"aktion":self.aktion,"top5Lebensraeume":self.top5Lebensraeume}, indent=2, ensure_ascii=False)
        writeFile.write(f"export const {prefix}_top5Lebensraeume={str(data)};\n")
        writeFile.write(f"export default {prefix}_top5Lebensraeume;")
        writeFile.close()
        logging.info(f"{prefix}_top5Lebensraeume.js generated.")

    def writeBundeslandTop100(self):
        prefix = f"{self.month}{self.year}"
        writeFile = open(f"{DATA_PATH}{prefix}_top100Bundeslaender.js","w")
        data = json.dumps({"aktion":self.aktion,"top100Bundeslaender":self.top100Bundeslaender}, indent=2, ensure_ascii=False)
        writeFile.write(f"export const {prefix}_top100Bundeslaender={data};\n")
        writeFile.write(f"export default {prefix}_top100Bundeslaender;")
        writeFile.close()
        logging.info(f"{prefix}_top100Bundeslaender.js generated.")


    def writeTop100(self):
        prefix = f"{self.month}{self.year}"
        writeFile = open(f"{DATA_PATH}{prefix}_top100.js","w")
        data = json.dumps({"aktion":self.aktion,"top100":self.top100}, indent=2, ensure_ascii=False)
        writeFile.write(f"export const {prefix}_top100={data};\n")
        writeFile.write(f"export default {prefix}_top100;")
        writeFile.close()
        logging.info(f"{prefix}_top100.js generated.")

    
    # END SECTION WRITE FUNCTIONS

if __name__ == '__main__':
    available = []
    seasons = []

    # Check available files using regular expressions
    logging.info(f"Loading existing previous data.")
    for fileName in os.listdir(DATA_PATH):
        match = re.match(r'(?P<month>juni|august)(?P<year>\d{4})', fileName)
        if match is not None:
            year = int(match.groupdict()["year"])
            month = match.groupdict()["month"]
            item = (year, month)
            if item not in available:
                available.append((year, month))

    # Creates Season Object for every missing file
    logging.info(f"Loading missing data")
    for year in range(START_YEAR, END_YEAR + 1):
        for month in MONTHS:
            if (year, month) not in available:
                season = Season(year, month)
                if season.status == 200:
                    seasons.append(season)
                    logging.info(f"Season {month}{year} created.")
                else:
                    logging.info(f"Season {month}{year} does not exist yet.")
                season = None

    logging.info("Generating missing data files.")
    for season in seasons:
        season.writeData()

    available = available + GENERATED_FILES
    available.sort()

    # GENERATING DataImport.vue
    indent = 4 * " "

    data = {}

    logging.info(f"Generating DataImport.vue...")
    with open("src/components/dataimport/DataImport.vue", "w") as writeFile:
        # begin file
        writeFile.write("<script>\n/* GENERATED AUTOMATICALLY DO NOT CHANGE */\n")
        # writes imports into DataImport.vue
        for season in available:
            prefix = f"{season[1]}{season[0]}"
            for ranking in RANKINGS:
                writeFile.write(f'import {prefix}_{ranking} from "{IMPORT_PATH}{prefix}_{ranking}";\n')
            writeFile.write("\n")

        # writes export into DataImport.vue
        writeFile.write("\nexport const ImportList = {\n")
        for ranking in RANKINGS:
            writeFile.write(indent + ranking + ": [\n")
            for season in available:
                writeFile.write(2 * indent + f"{season[1]}{season[0]}_{ranking},\n")
            writeFile.write(indent + "],\n")
        writeFile.write("};\n")
        writeFile.write("export default ImportList;\n")

        # end file
        writeFile.write("</script>\n")
        writeFile.close()
    logging.info(f"Generated DataImport.vue successfully")
