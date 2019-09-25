# In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process.
# You will be give a set of poll data called election_data.csv. 
# The dataset is composed of three columns: Voter ID, County, and Candidate. 
# Your task is to create a Python script that analyzes the votes and calculates each of the following:
# The total number of votes cast
# A complete list of candidates who received votes
# The percentage of votes each candidate won
# The total number of votes each candidate won
# The winner of the election based on popular vote.
# As an example, your analysis should look similar to the one below:
# Election Results
# -------------------------
# Total Votes: 3521001
# -------------------------
# Khan: 63.000% (2218231)
# Correy: 20.000% (704200)
# Li: 14.000% (492940)
# O'Tooley: 3.000% (105630)
# -------------------------
# Winner: Khan
# -------------------------
# In addition, your final script should both print the analysis 
# to the terminal and export a text file with the results.

import os
import csv
import numpy as np

CANDIDATE = 2
NL = "\n"

#This is primary function of this program.
#It opens and reads the file.
#Calls the function "processRow()" to get the information from each line.
def openWithCSV(file_path, data):
    #file_path - relative path to the data file.
    #data - the dictionary created in main
    #Open the file and start reading the data.
    
    with open(file_path, 'r') as csvfile:
    # Split the data on commas
        csv_reader = csv.reader(csvfile, delimiter=',')
        file_header = next(csv_reader)          #Dont need the header.
        
        # Loop through the rest of the rows.
        for row in csv_reader:
            processRow(row, data)

#Extracts the data from each row and keeps the running totals.
#There is a dictionary entry for each candidate.
def processRow(aRow, data):
   #aRow - One row of the file separated into a list.
   #data - The dictionary used to store running results.
   data.setdefault(aRow[CANDIDATE], 0)  #Create the dictionary entry if it doesn't exist.
   data[aRow[CANDIDATE]] += 1           #Count the votes.

#Using the acquired data, the results are calcualted, formatted and put in a list.
def createResultsList(data):
    #data - The acquired data dictionary after the file has been read.
    #returns a list of strings formatted as required.
 
    #Put each line in as an entry in a list.
    finish_list = []
    total_vote_count = 0
    winner = ""
    spacer = "----------------------------"

    finish_list.append("Election Results")
    finish_list.append(spacer)
    for key,  value in data.items():
        total_vote_count += value   
    
    finish_list.append("Total Votes: " + str(total_vote_count))
    finish_list.append(spacer)

    for key, value in sorted(data.items(),  reverse=True, key=lambda item: item[1]):
        if (len(winner) == 0):
            winner = key
        percent = ("%.3f" % round((np.divide(value, total_vote_count) * 100))) + "%"
        finish_list.append("%s: %s (%s)" % (key, percent, value))
        
    finish_list.append(spacer)
    finish_list.append("Winner: " + winner)
    finish_list.append(spacer)

    return finish_list

#Prints the results to the console.
#The newline is added by the print function.
def printToConsole(results_list):
    print()
    for each in results_list:
        print(each)   

#Writes the results to a file.
#Strange that Python doesnt have a writeline() function to 
#automatically add the newline.
def writeToFile(file_path, results_list):
    #Path and file name.  Subdirectories must exist if in path.
    with open(file_path, 'w') as txt_file:
        for each in results_list:
            txt_file.write(each)
            txt_file.write(NL)

def main():
    #Create a dictionary to pass to functions and hold the running data.
    voteCountSummary = {}
    #Source file path.
    file_path = os.path.join("Resources", "election_data.csv")
    openWithCSV(file_path, voteCountSummary )

    #The file has been read and processed.  Write the results.
    results_list = createResultsList(voteCountSummary)
    printToConsole(results_list)
    
    file_path = os.path.join("voting_results.txt")
    writeToFile(file_path, results_list)

if __name__ == '__main__':
    main()

