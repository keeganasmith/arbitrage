import csv


def team_name_abr_mapping():
    result = {}
    with open('./NFL/team_info.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            team_name = row[1].lower()
            team_abr = row[2]
            result[team_name] = team_abr
    return result
def team_abr_name_mapping():
    result = {}
    with open('./NFL/team_info.csv') as csvfile:
        for row in csvreader:
            team_name = row[1].lower()
            team_abr = row[2]
            result[team_abr] = team_name
    return result