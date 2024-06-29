import csv
import os

def saveToCsv(username, results):
    filename = os.path.join("results", f"{username}_results.csv")
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Site", "URL"])
        for result in results:
            site, url = result.split(": ")
            writer.writerow([site, url])
