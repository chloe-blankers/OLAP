#!/usr/bin/env python3

import argparse
import os
import sys
import csv

def num_sub_categories(dictionary, category):
    

    '''This function takes a dictionary and category and returns the number of distinct subcategories.'''

    i = 0

    subcategories = []


    while (i < len(dictionary[category])):


        if(dictionary[category][i] not in subcategories):

            subcategories.append(dictionary[category][i])


        i += 1


    return len(subcategories)


def print_header(field_type_dict, num_subcategories):

    '''This function takes a field type dictionary as a parameter an uses that to check weather the column should be printed. 
       if the an agregate is being requested of an invalid field type, it will not print the column. Otherwise is prints
       the 'argegave_filednames'.'''

    i = 3

    length = len(sys.argv)
    
    
    while (i < length):    


        if (sys.argv[i].startswith("--")): # If it is an agregate
            
            if (i != length - 1):
               
                result = check_field(field_type_dict, sys.argv[i + 1], sys.argv[i])
                
            else:

                result = -1

            if (sys.argv[i] == "--count"):
                
                if (i == length - 1):

                    print("count", end = "")
                
                else:

                    print("count,", end = "")

            elif (sys.argv[i] == "--top"):

                if (i == length - 3):
                    
                    print("top_" + sys.argv[i + 2], end = "")

                else:

                    print("top_" + sys.argv[i + 2] + ",", end = "")
        
                if (num_subcategories > 20 and int(sys.argv[i + 1]) > 20):

                    print("_capped", end = "")

            elif (result == 1):
                
                if (sys.argv[i] == "--group-by"):
                
                    if (i == length - 2):

                        print(sys.argv[i + 1], end = "")

                    else:

                        print(sys.argv[i + 1] + ",", end = "")
                 
                else:

                    if (i == length - 2):

                        print(sys.argv[i].strip("--") + "_" + sys.argv[i + 1], end = "")

                    else:

                        print(sys.argv[i].strip("--") + "_" + sys.argv[i + 1] + ",", end = "")


        i += 1

    print("")


def computing_agregates(dictionary, csv_file, count, field_type_dict, line):

    '''This function takes the dictionary, input file, count and field type dictionary and loops through the command line 
       computing the agregates through out and printing them to stdout.'''
    
    csv_file.seek(0)

    i = 0


    while (i < len(sys.argv)): # Going through the command line and computing valid operations as requested 


        if (sys.argv[i] == "--count"):
    
            if (i == len(sys.argv) - 1):
                
                print(str(line), end = "")
            
            else:
                
                print(str(line) + ",", end = "")

        if (sys.argv[i] == "--min"):
           
            i += 1
            
            if (field_type_dict[sys.argv[i]] == "categorical"):
                
                None
            
            else:
                
                min_val = min(dictionary[sys.argv[i]])
                
                if (i == len(sys.argv) - 1):
                    
                    print(str(min_val), end = "")
                
                else:
                    
                    print(str(min_val) + ",", end = "")

        elif (sys.argv[i] == "--max"):
            
            i += 1
            
            if (field_type_dict[sys.argv[i]] == "categorical"):
                
                None
            
            else:
                
                max_val = max(dictionary[sys.argv[i]])
                
                if (i == len(sys.argv) - 1):
                    
                    print(str(max_val), end = "")
                
                else:
                    
                    print(str(max_val) + ",", end = "")

        elif (sys.argv[i] == "--mean"):
            
            i += 1
            
            if (field_type_dict[sys.argv[i]] == "categorical"):
                
                None
            
            else:
                
                mean = sum(dictionary[sys.argv[i]])/count
                
                if (i == len(sys.argv) - 1):
                    
                    print(str(mean), end = "")
                
                else:    
                   
                    print(str(mean) + ",", end = "")

        elif (sys.argv[i] == "--sum"):
            
            i += 1
            
            if (field_type_dict[sys.argv[i]] == "categorical"):
                
                None
            else:

                sumation = sum(dictionary[sys.argv[i]])
                
                if (i == len(sys.argv) - 1):
                    
                    print(str(sumation), end = "")
                
                else:
                    
                    print(str(sumation) + ",", end = "")
        
        elif (sys.argv[i] == "--top"):
            
            i += 2
            
            top_k(dictionary, sys.argv[i - 1], sys.argv[i], count) 

        else:
            
            i += 1


def top_k(dictionary, K, categorical_name, count):
    
    '''This function takes the dictionary, value K, categorical field name and count as parameters
       to compute top k agregate. It will also output an error if top k is requested on a field with
       more than 20 distinct values.'''


    i = 0

    lst = list(dictionary[categorical_name])

    dict_topk = {}
    
    subcategories = []


    while (i < len(lst)): # Going through the subcategories of the given category and counting the number of occurences of each
        
        if (lst[i] not in subcategories):
            
            subcategories.append(lst[i])
            
            dict_topk.update( { lst[i] : 1 } )
        
        else:
        
            dict_topk[lst[i]] += 1
         
        i += 1
  

    topk_vals = []
    
    topk_vals = sorted(dict_topk.values(), reverse = True)
    
    topk_vals = topk_vals[:int(K)]

    topk_keys = []
    
    topk_keys = list(dict_topk.keys())

    
    if (len(subcategories) > 20 and int(K) > 20):  
        
        sys.stderr.write("Error: " + sys.argv[2] + ": " + categorical_name + " has been capped at 20 distinct values\n")


    i = 0
    
    s = '\"'
    
    while (i < int(K)): # printing the top k values in a string
       

        if (i == len(subcategories)):
            
            break

        if (i == 20):
            
            break

        key = topk_keys[i] 

        if (i != 0):

            s += ","

        s += key + ": " + str(topk_vals[i])

        i += 1
    

    s += '\"'
    
    print(s, end = "")


def check_field(field_type_dict, fieldname, agregate):

    '''This function takes the field type dictionary, fieldname and agregate as parameters to check
       if the agregate computation are valid. If it is the fucntion returns 1, otherwise it returns -1.'''
    

    if (agregate == "--group-by" and field_type_dict[fieldname] == "categorical"):

        return 1

    elif (agregate != "--top" and agregate != "--group-by" and agregate != "--count" and field_type_dict[fieldname] == "categorical"):

        sys.stderr.write("Error: " + sys.argv[2] + ": can't compute " + agregate.strip("--") + " on non-numeric field '" + fieldname + "'\n")
        
        return -1

    elif (agregate != "--top" and agregate != "--group-by" and agregate != "--count" and field_type_dict[fieldname] == "numerical"):
        
        return 1

    return 1


def subcategory_dictionary(subcategory, field_type_dict, index):

    '''This function takes the name of the subcategory, the field type dictionary and the header index 
       of the given categorical field to create a dictionary for the subcategory. It also checks for
       corrupt data in the numerical fields and prints errors accordingly.''' 
    

    with open(sys.argv[2],"r", encoding = "utf-8-sig") as csv_file:


        csv_file.seek(0)
        
        reader = csv.reader(csv_file)
        
        row = next(csv_file)
        
        row = row.split(",")
        
        length = len(row)
        
        fieldnames = []

        dictionary = {}
        
        i = 0


        while (i < length): # Adding the field names as keys to the dictionary and the value as an empty lists


            if (i == length - 1):
                
                row[i] = row[i].strip("\n")

            row[i] = row[i].lower()

            fieldnames.append(row[i])

            dictionary.update( {row[i] : []} )

            i += 1


        corrupt_data_count = []

        i = 0


        while (i < len(fieldnames)): # Making list the size of the field names to keep track of corrupt/invalid data for each field


            corrupt_data_count.append(0)
            
            i += 1
        
        corrupt = False
        
        first_corrupt = True

        line = 0

        count = 0

        first_row = True

        for row in reader:

        

            if (row[index] == subcategory): 

                line += 1

                if (corrupt == False):

                    count += 1

                i = 0

                while (i < length): # Adding each value to the appropriate field name key while keeping track of corrupt/invalid data 


                    if (field_type_dict[fieldnames[i]] == "numerical"):

                        try:

                            row[i] = float(row[i])
                            
                            dictionary[fieldnames[i]].append(float(row[i]))
                            
                            corrupt = False 
                        
                        except:
                                
                            if (first_corrupt == True):
                                
                                count -= 1

                                first_corrupt = False

                            corrupt = True

                            corrupt_data_count[i] += 1

                            if (corrupt_data_count[i] > 100):

                                sys.stderr.write("Error: " + sys.argv[2] + ":more than 100 non-numeric values found in aggregate column '" + fieldnames[i] + "'\n")
                                
                                exit(7)

                            n = 0
                        
                            while (n < len(sys.argv) - 1):

                                if (sys.argv[n + 1] == fieldnames[i]):

                                    sys.stderr.write("Error: " + sys.argv[2] + ":" + str(line + 1) + ": can't compute " + sys.argv[n].strip("--") +  " on non-numeric value " + "'" + row[i] + "'"+ "\n")
                                
                                n += 1

                    else:

                        dictionary[fieldnames[i]].append(row[i])
                
                    
                    first_row = False

                    i += 1
        
        if (len(sys.argv) == 5):

            print(subcategory, end = "")

        else:

            print(subcategory + ",", end = "")


        computing_agregates(dictionary, csv_file, count, field_type_dict, line)



def main():


    ''' Validating CSV file '''
    

    if (len(sys.argv) == 1 or len(sys.argv) == 2): 

        sys.stderr.write("Error: No input file specified\n")
        
        exit(6)

    try:

        f = open(sys.argv[2],"r")
        
        f.close()

    except IOError as e:
        
        sys.stderr.write("Error: " +  sys.argv[2] + " : does not exist or cannot be read\n")
        
        exit(6)

    if (os.path.splitext(sys.argv[2])[1] != ".csv"):
        
        sys.stderr.write("Error: " + sys.argv[2] + " is not a .csv file\n")
        
        exit(6)


    ''' Validating command line arguments '''


    parser = argparse.ArgumentParser()

    parser.add_argument("--count", help = "counts the number of records\n", action = "store_true")
    parser.add_argument("--input", nargs = 1, type = argparse.FileType("r"), help = "the input file in csv format\n") 
    parser.add_argument("--min", nargs = 1, type = str, help = "computes the minimum value of a numeric-field-name\n")
    parser.add_argument("--max", nargs = 1, type = str, help = "computes the maximum value of a numeric-field-name\n")
    parser.add_argument("--mean", nargs = 1, type = str, help = "computes the average of numeric-field-name\n")
    parser.add_argument("--sum", nargs = 1, type = str, help = "computes the sum of numeric-field-name\n")
    parser.add_argument("--top", nargs = 2, type = str, help = "computes the top k most common values of categorical-field-name\n")
    parser.add_argument("--group-by", nargs = 1, type = str, help = "computes one row of output per distinct value in given categorical-field\n")

    args = parser.parse_args()
    

    ''' Checking if fieldnames are numeric or categorical and storing their type in a dictionary '''


    with open(sys.argv[2],"r", encoding = "utf-8-sig") as csv_file:
        

        reader = csv.reader(csv_file)
        
        try :
            
            row = next(csv_file)
        
        except:

            sys.stderr.write("Error : " + sys.argv[2] + " is empty\n")
            
            exit(6)

        row = row.split(",")
        
        length = len(row)
        
        field_names = []
        
        field_type_dict = {}

        i = 0
        
        index = 0;


        while (i < length): # Adding each field name as a key to a dictionary with empty strings as their values


            if (i == length - 1):
                
                row[i] = row[i].strip("\n")
                
            row[i] = row[i].lower() 

            field_names.append(row[i])
            
            field_type_dict.update( { field_names[i] : "" } )
            
            i += 1
    

        for row in reader:

            i = 0

            while (i < length): # Setting the values of the fields

                
                try:
                    row[i] = float(row[i])

                    field_type_dict[field_names[i]] = "numerical"
                
                except:
                    
                    field_type_dict[field_names[i]] = "categorical"
            
                i += 1

            break # Stop reading the file as we only needed the header
    

    ''' Storing the file header indexes as numerical or categorical '''


    length = 0
    
    for key in field_type_dict:

        length += 1


    numeric_field_indexes = []
    
    i = 0


    while (i < length): # Making a list of the numerical field indexes 


        if (field_type_dict[field_names[i]] == "numerical"):
        
            numeric_field_indexes.append(i)
        

        i += 1

    
    ''' Checking if requested computations are valid '''


    i = 3
 
    top = False
    

    while (i < len(sys.argv)): # Chceking for errors


        if not (sys.argv[i].startswith("--")):
            
            if (sys.argv[i - 1] == "--top" or sys.argv[i - 1] == "--group"):
                    
                 if (sys.argv[i + 1] not in field_names):

                    sys.stderr.write("Error: " + sys.argv[2] + ":no field with name '" +  sys.argv[i + 1] + "' found\n")

                    exit(8)
                    
                 if (sys.argv[i].isalpha() == True):

                     sys.stderr.write("Error: " + sys.argv[2] + ":top k must take a digit as the first argument\n")

                     exit(6)
                
                 try:

                     if (int(sys.argv[i]) <= 0):

                         print("Error: " + sys.argv[2] + ":top k must take a digit larger than 0 as it's first argument\n")
                         
                         exit(6)

                 except TypeError:

                     sys.stderr.write("Error: " + sys.argv[2] + ":top k must take a digit as the first argument\n")

                     exit(6)


                 except ValueError:
                    
                     sys.stderr.write("Error: " + sys.argv[2] + ":top k must take a digit as the first argument\n")

                     exit(6)

                
                 if (sys.argv[i + 1] not in field_names):

                    sys.stderr.write("Error: " + sys.argv[2] + ":no top k argument with name '" + sys.argv[i + 1] + "'\n")
                    
                    exit(6)
                
                 if (field_type_dict[sys.argv[i + 1]] == "numerical"):

                    sys.stderr.write("Error: " + sys.argv[2] + ":can't compute top k on numeric field '" + sys.argv[i + 1] + "'\n")
                    
                    exit(6)
                
            if (sys.argv[i] not in field_names and sys.argv[i - 1] != "--top" and sys.argv[i - 1] != "--group-by"):
                
                sys.stderr.write("Error: " + sys.argv[2] + ":no field with name '" +  sys.argv[i] + "' found")
                
                exit(8)

        if (sys.argv[i] == "--group-by" and sys.argv[i + 1] not in field_names):
            
            sys.stderr.write("Error: " + sys.argv[2] + ":no group-by argument with name '" + sys.argv[i + 1] + "' found\n")

            exit(9)

            
        if (sys.argv[i] == "--group-by" and sys.argv[i + 1] in field_names):

            if (sys.argv[i] == "--group-by" and field_type_dict[sys.argv[i + 1]] == "numerical"):
            
                sys.stderr.write("Error: " + sys.argv[2] + ":" + "can't compute group-by on numeric-field '" + sys.argv[i + 1] + "'\n")

                exit(6)
        


        i += 1


    ''' Checking for validated group-by request'''


    i = 3

    while (i < len(sys.argv)): # Checking the command line for group-by
            
        
        if (sys.argv[i] == "--group-by"):    

            categorical_fieldname = sys.argv[i + 1]

            subcategories = []

            with open(sys.argv[2],"r", encoding = "utf-8-sig") as csv_file:


                csv_file.seek(0)
                
                reader = csv.reader(csv_file)
                
                row = next(csv_file)
                
                row = row.split(",") 
                
                length = len(row) 
                
                fieldnames = []
    
                i = 0
                
                index = 0;

                
                while (i < length): # Making a  finding the index of the categorical fieldname        
    

                    if (i == length - 1):
                    
                        row[i] = row[i].strip("\n")

                    fieldnames.append(row[i])    
                    
                    row[i] = row[i].lower()

                    if (row[i] == categorical_fieldname):
                    
                        index = i


                    i += 1

        
                for row in reader:
                
                    if (row[index] not in subcategories):
                        
                        subcategories.append(row[index])
                
                
                subcategories.sort()
                
                num_subcategories = len(subcategories)

                n = 0
                
                print_header(field_type_dict, num_subcategories)

                
                while (n < len(subcategories)): # Making a dictionary and computing the agregates for each subcategory until it is cappped at 20
                

                    if (n == 20):
                    
                        sys.stderr.write("Error: " + sys.argv[2] + ":" + categorical_fieldname + " has been caped at 20 values\n") 
                        
                        sys.stderr.write("Error: " + sys.argv[2] + ":" + "group-by argument " + categorical_fieldname + " has high cardinality\n")

                        break
                    
                    if(subcategories[n] == ""):
                        
                        sys.stderr.write("Error: " + sys.argv[2] + ": cannot perform group-by on empty data\n")

                    else:
                        
                        subcategory_dictionary(subcategories[n], field_type_dict, index)

                        print("")


                    n += 1


            exit(0)


        i += 1


    ''' Creating dictionary - no group-by argument '''
 

    with open(sys.argv[2],"r", encoding = "utf-8-sig") as csv_file:
        
        csv_file.seek(0)

        reader = csv.reader(csv_file)
        
        row = next(csv_file)
        
        row = row.split(",")
        
        dictionary = {}
        
        length = len(row) 
        
        i = 0
        
        fieldnames = []


        while (i < length): # Adding field names to dictionary as valuesand empty lists as keys


            if (i == length - 1):
            
                row[i] = row[i].strip("\n")
             
            row[i] = row[i].lower()

            fieldnames.append(row[i])
                
            dictionary.update( {row[i] : []} )


            i += 1


        corrupt_data_count = []
        
        i = 0


        while (i < len(fieldnames)): # Making list the size of the field names to keep track of corrupt/invalid data for each field


            corrupt_data_count.append(0)
            
            i += 1


        count = 0
        
        line = 0

        for row in reader:  
            
            line += 1
            
            i = 0
            

            while (i < length): # Adding each value to the appropriate field name key while keeping track of corrupt/invalid data 


                if (field_type_dict[fieldnames[i]] == "numerical"):

                    try:
                    
                        row[i] = float(row[i])
                        
                        dictionary[fieldnames[i]].append(float(row[i]))
                     
                        count += 1
                    
                    except:
                        
                        corrupt_data_count[i] += 1

                        if (corrupt_data_count[i] > 100):
                            
                            sys.stderr.write("Error: " + sys.argv[2] + ":more than 100 non-numeric values found in aggregate column '" + fieldnames[i] + "'\n")
                    
                            exit(7)

                        n = 0


                        while (n < len(sys.argv) - 1):


                            if (sys.argv[n + 1] == fieldnames[i]):

                                sys.stderr.write("Error: " + sys.argv[2] + ":" + str(line + 1) + ": can't compute " + sys.argv[n].strip("--") +  " on non-numeric value " + "'" + row[i] + "'"+ "\n")

                            n += 1

                else:

                    dictionary[fieldnames[i]].append(row[i])
            

                i += 1
        
            
    ''' No parameters given - default to --count '''


    if (len(sys.argv) == 3):

        print("count")

        count = str(count)
        
        print(count)
        
        exit(0)
    

    ''' computing agregates requested '''
    
    i = 0

    top = False


    while (i < len(sys.argv)): # Finding categorical value for top k


        if (sys.argv[i] == "--top" and i < len(sys.argv) - 2):
            
            top = True

            category = sys.argv[i + 2]


        i += 1


    with open(sys.argv[2],"r") as csv_file:
    
        num_topk = -1

        if (top == True):
            
            num_topk = num_sub_categories(dictionary, category)  

        print_header(field_type_dict, num_topk)
        
        computing_agregates(dictionary, csv_file, count, field_type_dict, line)
            
    print("")

    exit(0)



if __name__ == '__main__':
    main()





