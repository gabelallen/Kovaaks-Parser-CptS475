import os
import csv
import sys
from datetime import datetime
from pathlib import Path

# this script was made to parse data from KovaaK's .csv files for a school project
# it takes a main folder containing subfolders filled with 4 .csv files each as input
# it then looks through the .csv files in order of time for specific values
# and then adds those values to an output.csv file containing only the parsed data in the format:
# folder_name,scenario_order,empty_space,scenario_name,total_shots,hit_count,miss_count,total_overshots,sens_increment

# made for voltaic's psalmTS and Air scenarios, but it shouldn't be hard to adapt this code to other scenarios

def get_datetime_from_filename(filename):
    date_time_str = filename.split(" - ")[-1].split(" ")[-2]
    date_time_str = date_time_str.replace(':', '-')
    return datetime.strptime(date_time_str, "%Y.%m.%d-%H.%M.%S")

def extract_stats_from_csv(csv_path):
    hit_count = total_overshots = miss_count = sens_increment = None

    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for row in reader:
            if not row:
                break

        for row in reader:
            if len(row) >= 2:
                if row[0] == 'Hit Count:':
                    hit_count = int(row[1])
                elif row[0] == 'Total Overshots:':
                    total_overshots = int(row[1])
                elif row[0] == 'Miss Count:':
                    miss_count = int(row[1])
                elif row[0] == 'Sens Increment:':
                    sens_increment = float(row[1])

    if hit_count is None or total_overshots is None or miss_count is None:
        print(f"Warning: Required information not found in {csv_path}")

    return hit_count, miss_count, total_overshots, sens_increment

def remove_non_numeric(input_string):
    return ''.join(char for char in input_string if char.isdigit())

def replace_substring(input_string):
    if "Air" in input_string:
        return "Air"
    elif "psalmTS" in input_string:
        return "psalmTS"
    else:
        return input_string

def parse_csv_contents(folder_path, outputcsv):
    for root, dirs, files in os.walk(folder_path):
        if len(files) == 4 and all(file.endswith(".csv") for file in files):
            files = sorted(files, key=get_datetime_from_filename) #sort the files in order of time

            order = 1 #order starts at 1
            for file in files:
                #read variables
                hit_count, miss_count, total_overshots, sens_increment = extract_stats_from_csv(Path(root) / file)

                #write to outputcsv
                writer = csv.writer(outputcsv)
                writer.writerow([remove_non_numeric(root),order,"",replace_substring(file),(hit_count+miss_count), hit_count, miss_count, total_overshots, sens_increment])

                #increment order
                if(order == 4):
                    order = 1
                else: order+=1




        else: #exit if there is not exactly 4 csv files in a subfolder
            if root != 'content':
                print(f"ERROR: Subfolder {root} does not contain exactly 4 CSV files.")
                sys.exit("Exiting program.")    

main_folder_path = 'content' #folder containing the subfolders

with open('output.csv', mode='w', newline='') as csvfile:
    parse_csv_contents(main_folder_path, csvfile)
