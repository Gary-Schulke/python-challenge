# In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. 
# You will give a set of financial data called budget_data.csv. 
# The dataset is composed of two columns: Date and Profit/Losses. 
# Your task is to create a Python script that analyzes the records to calculate each of the following:
# The total number of months included in the dataset
# The net total amount of "Profit/Losses" over the entire period
# The average of the changes in "Profit/Losses" over the entire period
# The greatest increase in profits (date and amount) over the entire period
# The greatest decrease in losses (date and amount) over the entire period
# As an example, your analysis should look similar to the one below:
# Financial Analysis
# ----------------------------
# Total Months: 86
# Total: $38382578
# Average  Change: $-2315.12
# Greatest Increase in Profits: Feb-2012 ($1926159)
# Greatest Decrease in Profits: Sep-2013 ($-2196167)
# In addition, your final script should both print the analysis to the terminal and export a text file with the results.

import os
import csv
import numpy as np

DATE = 0
PROFIT = 1
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
        file_header = next(csv_reader)
        first_row = next(csv_reader)

        # The first row of data must be read and set or the
        # greatest profit and greatest loss might not be accurate. 
        setFirstData(first_row, data)

        # Loop through the rest of the rows.
        for row in csv_reader:
            processRow(row, data)

#Sets default values and read values from the first line data.
#No math to do here.
def setFirstData(firstRow, data):
   #firstRow - The first n0n-header row of data read from the file.
   #data - The dictionary used to store running results.
    data["TOTALMONTHS"] = 1
    data["NETTOTAL"] = int(firstRow[PROFIT])
    data["RUNNINGCHANGE"] = 0
    data["PREVIOUSPROFIT"] = int(firstRow[PROFIT])
    data["BIGGESTPROFIT"] = {firstRow[DATE]:0}
    data["BIGGESTLOSS"] = {firstRow[DATE]:0}   

#Extracts the data from each row and keeps the running totals.
def processRow(aRow, data):
   #aRow - One row of the file separated into a list.
   #data - The dictionary used to store running results.
    data["TOTALMONTHS"] += 1
    profit = int(aRow[PROFIT])
    data["NETTOTAL"] += profit
    month_change =  profit - data["PREVIOUSPROFIT"]
    data["RUNNINGCHANGE"] += month_change

    #Tracking the biggest profit and loss takes a little logic.
    #Gains and Losses values are replaced when its current value is exceeded.
    if(month_change > 0):
        #There was an increase in profit.
        tempDict = {}
        #There is only one entry so it only runs once.
        for key, value in data["BIGGESTPROFIT"].items():
             if (value < month_change):
                tempDict = {aRow[DATE] : month_change}
        if not (len(tempDict) == 0):
            data["BIGGESTPROFIT"] = tempDict

    elif (month_change < 0):
        #There as a decrease in profit.
        tempDict = {}
        #There is only one entry so it only runs once.
        for key, value in  data["BIGGESTLOSS"].items():  
            if (value > month_change):
                tempDict = {aRow[0] : month_change}
        if not (len(tempDict ) == 0):
            data["BIGGESTLOSS"] = tempDict
    #Save for the next look.       
    data["PREVIOUSPROFIT"] = profit

def createResultsList(data):
    #data - The acquired data after the file has been read.
    #returns a list of strings formatted as required.
    #Compose the results into a formatted output
    results_list = []
    spacer = "-----------------------------------------"
    results_list.append("Financial Analysis")
    results_list.append(spacer)
    results_list.append("Total Months: " + str(data['TOTALMONTHS']))
    results_list.append("Total: " + str(data["NETTOTAL"])) 
    results_list.append("Average Change: " + "%.2f" % (np.divide(data["RUNNINGCHANGE"], (data["TOTALMONTHS"] - 1))))
 
    increase = "Greatest Increase in Profits: "
    for key, value in data["BIGGESTPROFIT"].items():
        increase = increase + key + " ($" + str(value) + ")" 
    results_list.append(increase)

    decrease = "Greatest Decrease in Profits: "
    for key, value in data["BIGGESTLOSS"].items():
        decrease = decrease + key + " ($" + str(value) + ")" 
    results_list.append(decrease)

    return results_list

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
    dataSummary = {"DATE": 0,
            "PROFIT": 1,
            "NETTOTAL": 0,
            "RUNNINGCHANGE" : 0,
            "PREVIOUSPROFIT" : 0,
            "BIGGESTPROFIT" : {},
            "BIGGESTLOSS" : {},
            "TOTALMONTHS" : 0}
    #Source file path.
    file_path = os.path.join("Resources", "budget_data.csv")
    openWithCSV(file_path, dataSummary )

    #The file has been read and processed.  Write the results.
    results_list = createResultsList(dataSummary)
    printToConsole(results_list)
    
    file_path = os.path.join("budget_results.txt")
    writeToFile(file_path, results_list)

if __name__ == '__main__':
    main()

