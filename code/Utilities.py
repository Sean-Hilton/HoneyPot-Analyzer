from datetime import datetime
import os
import json
import sys
import urllib.request#for getting ip location

class FileReadingUtilities:
    '''Utilities around reading in a file'''
    def get_path_to_use():
        """Has user enter path to log or folder containing logs as shallow children."""
        response = input(""""Please enter the file path to the log file(s) you would like to know about it.\n""")
        path = os.path.abspath(response)

        while (os.path.exists(path) == False):
            response = input('Im sorry, that path does not seem to exist. Please put your path to your JSON log files folder. \n')
            path = os.path.abspath(response)


        return path


    def get_files_to_parse(path):
        """locates the files in given path we will try to parse. RETURNS: (list_of_paths, report_name)"""
        path_to_look = os.path.abspath(path)
        defaultReportName = "HONEYPOT_REPORT"
        reportName = defaultReportName
        list_of_paths = []

        if os.path.isfile(path_to_look):
            fileName = os.path.basename(path_to_look)
            inputName,inputExt = os.path.splitext(fileName)
            reportName = "{}_REPORT".format(inputName)

            list_of_paths.append(path_to_look)
        elif os.path.isdir(path_to_look):
            file_count = 0
            for root,dirs,files in os.walk(path_to_look):
                for f in files:
                    fullpath = os.path.join(root,f)
                    file_count += 1
                    list_of_paths.append(fullpath)

            #set report name based on combined file amount
            reportName = "{}_file_report".format(str(file_count))

        else:
            print("Unable to find file or director at path: {}".format(path_to_look))

        reportName += "-{}".format(GeneralUtilities.get_date_string())

        return list_of_paths, reportName


class DictionaryUtilites:
    '''Utilites for dictionary manipulation.'''

    def remove_duplicates(seq,idfun=None):
        '''removes duplicates from supplied list and returns a list with no duplicates (we usually call this list 'deduped_list')'''
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result
    
    def get_lists(json_data, key_string):
        '''gets list of all values for supplied key. Key should be a string value. Can be passed in as a 'LogKey.[enumValue].key()'.'''
        full_list = ""

        for x in range(0, len(json_data)):
            try:
                item = json_data[x]
                full_list += str(json_data[x] [key_string]) + "\n"
            except Exception as e:
                pass
        deduped_list = DictionaryUtilites.remove_duplicates(full_list.split())
        return full_list, deduped_list
    
    def get_data_from_logs(list_of_paths):
        '''given a list of paths of individual JSON log files. gives us our data array'''
        path_count = len(list_of_paths)
        data = []
        #exit program if we have found no paths
        if path_count == 0:
            print("No path found at path: {}".format(path_to_look))
            return

        #list of paths as a string as we read them in
        read_in_paths = ""
        index = 0
        #begin to add all found json objects to list of data
        for path in list_of_paths:
            print("Reading in: {}".format(path))
            read_in_paths += "'{}'".format(path)
            
            index += 1

            if index != path_count:
                read_in_paths += ","

            index += 1

            #Add inside quotes the location of the .json data file
            with open (path) as file:
                for line in file:
                    try:
                        info = json.loads(line)
                        data.append(info)
                    except Exception as e:
                        print("Exception reading file: {}".format(e))

        return data
    
    def get_all_items(full_list, deduped_list):
        """Given a list with no duplicates and a list with duplicates, this finds the frequency of each value"""
        count_dict = {}
        for item in deduped_list:
            count_dict[item] = full_list.count(item)

        return count_dict#return count of all items


    def get_top_ten(full_list, deduped_list):
        """Given a list with no duplicates and a list with duplicates, this finds the top 10 most frequent values and the counts for them in a dictionary."""
        count_dict = DictionaryUtilites.get_all_items(full_list, deduped_list)
        top_ten = sorted(count_dict, key=count_dict.get, reverse=True)[:10]
        
        return top_ten, count_dict



class GeneralUtilities:
    '''Some general utility functions'''
    def get_date_string():
        """Used to get string for current data"""
        now = datetime.now()

        current_time = now.strftime("%H_%M_%S_%F")    
        return current_time

    def get_ip_location(ip):
        """uses api to get (country, city) tuple it returns"""

        url = 'http://ipinfo.io/'+ip+'/json'
        response = urllib.request.urlopen(url)
        data = json.load(response)
    
        city = data['city']
        country = data['country']
    
        return country, city