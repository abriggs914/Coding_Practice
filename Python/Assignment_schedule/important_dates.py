#code

important_dates = {"September" : ["2019-09-13 CS3035 Assignment 0",
                                  "2019-09-23 CS3035 Assignment 1",
                                  "2019-09-20 CS4725 Assignment 1",
                                  "2019-09-25 CS4725 Lab 1 due",
                                  "2019-09-27 CS3113 Assignment 1",
                                  "2019-09-27 CS4411 Project Topic deadline"],
                   "October"   : ["2019-10-04 CS3035 Assignment 2",
                                  "2019-10-18 CS3035 Assignment 3",
                                  "2019-10-29 CS3035 MIDTERM",
                                  "2019-10-31 CS3035 Group Project Announced",
                                  "2019-10-04 CS4725 Assignment 2",
                                  "2019-10-09 CS4725 Lab 2 due",
                                  "2019-10-18 CS4725 MIDTERM",
                                  "2019-10-23 CS4725 Lab 3 due",
                                  "2019-10-30 CS4725 Assignment 3",
                                  "2019-10-31 CS4355 Assignment 1",
                                  "2019-10-29 CS4355 MIDTERM",
                                  "2019-10-18 CS3113 MIDTERM 1",
                                  "2019-10-22 CS4411 MIDTERM",
								  "2019-10-11 CS3113 Assignment 2",
                                  "2019-10-04 CS4411 Project Outline deadline"],
                   "November"  : ["2019-11-22 CS3113 MIDTERM 2",
                                  "2019-11-21 CS4355 Assignment 2",
                                  "2019-11-06 CS4725 Lab 4 due",
                                  "2019-11-20 CS4725 Assignment 4",
                                  "2019-11-27 CS4725 Programming Project due",
                                  "2019-11-01 CS3035 Assignment 4",
                                  "2019-11-18 CS3035 Assignment 5",
                                  "2019-11-29 CS3035 Assignment 6",
                                  "2019-11-01 CS4411 Interium Report",
                                  "2019-11-26 CS4411 Presentation"],
                   "December"  : ["2019-12-04 CS4725 Assignment 5",
                                  "2019-12-03 CS4355 Programming Project due",
                                  "2019-12-05 CS4411 Final Report"]}
    
sorted_important_dates = {}          
        
def stringify(dictionary):
    res = ""
    for key in dictionary:
        res += key + " "
        for item in dictionary[key]:
            res += item + " "
    return res
        

def determineNumDuePerDay(dates):
    days_and_assignments = []
    checked_dates = []
    big_string = stringify(dates)
    for month in dates:
        num_assignments_due = len(dates[month])
        for assignment in dates[month]:
            date_due = assignment[0:10]
            if date_due not in checked_dates:
                checked_dates.append(date_due)
                days_and_assignments.append(date_due + ":  " + str(big_string.count(date_due)))
    
    days_and_assignments = sorted(days_and_assignments)
    for day in days_and_assignments:
        print(day)
        file.write(day + "\n")
            
try :
    file = open("important_dates_output.txt", "w")
    
    for month in important_dates:
        sorted_important_dates[month] = sorted(important_dates[month])
        month_separator = "\n\n\t-- " + str(month) + " -- \n"
        print(month_separator)
        file.write(month_separator)
        for assignment in sorted_important_dates[month]:
            print(assignment)
            file.write(assignment + "\n")
            
    print("\n\n\n")
    determineNumDuePerDay(sorted_important_dates)
    file.close()
except :
	print("failed writing")


        
input("type to quit\n")