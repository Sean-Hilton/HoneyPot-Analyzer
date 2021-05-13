from Utilities import GeneralUtilities, FileReadingUtilities, DictionaryUtilites
from ReportGeneration import ReportGenerator
from CowrieDefinitions import LogKeys
 
def run_key_chooser_menu():
    '''Menu to get the key for the item from. (Returns a string value for the key.)'''
    selected_key = ""
    key_options = """Select a key. \n"""

    custom_value_option = -1
    #build list of keys for the user to choose to query. (they may also enter a string and try to query that.)
    for log_key, _ in LogKeys.all_keys_dictionary().items():
        key_int = int(log_key)
        if key_int < 10:
            key_options += " "
        key_options += "     {}) {}\n".format(str(key_int), log_key.description())
        if key_int > custom_value_option:
            custom_value_option = key_int + 1

    key_options += "     {}) To enter custom value. \n".format(str(custom_value_option))
    key_options += "      0) Done\n"

    key_input = input(key_options)
    
    enum_value = LogKeys.INVALID

    #try to cast selected value to LogKeys type
    try:
        enum_value = LogKeys(int(key_input))
    except:
        pass

    #get key value
    if enum_value != LogKeys.INVALID:
        selected_key = enum_value
    elif key_input == str(custom_value_option):
        selected_key = input("Ok. Please enter the message and we will parse that for you.")
    elif key_input == '0':
        return ""
    else:
        print("Command not recognized...\n")
        return run_key_chooser_menu()

    return selected_key
    

def run_reports_menu(report_name_base, data, list_of_paths):
    '''runs report menu for generating a report on data'''
    picking_reports = True

    while picking_reports:
        report_selection = input("""What kind of report would you like to generate?
            1) General Top 10 Report
            2) Custom Top 10 Report
            0) Exit 
            """)

        if report_selection == '1':#generate top10 report
            ReportGenerator.generate_standard_top_10_report(data, report_name_base)
        elif report_selection == '2':
            keys = []
            add_keys = True
            while add_keys:
                chosen_key = run_key_chooser_menu()
                if chosen_key == "":
                    print("Done adding keys. Generate top 10 report.")
                    add_keys = False
                elif chosen_key in keys:
                    print("Key already in dictionary, choose again.\n")
                else:
                    keys.append(chosen_key)
            if len(keys) == 0:
                print("No keys added, generating default report.")
                ReportGenerator.generate_standard_top_10_report(data,report_name_base)
            else:
                ReportGenerator.generate_top_10_report(data,report_name_base,keys)
        elif report_selection == '0':
            picking_reports = False
        else:
            print("Unrecognized command! - '{}'".format(report_selection))


def run_query_results_menu(data, list_of_paths):
    """Querying the results allows for the user to supply a key or enum value to get percentages of responses for item."""
    #get key for query
    key = run_key_chooser_menu()
    if key != "" and isinstance(key,LogKeys) :
        key = key.key()
    #get lists
    whole_list, deduped_list = DictionaryUtilites.get_lists(data, key)
    count = DictionaryUtilites.get_all_items(whole_list,deduped_list)
    total_items = 0.0


    sorted_values = sorted(count.values(),reverse=True) # Sort by the values
    sorted_dict = {}

    for i in sorted_values:
        total_items += float(i)
        for k in count.keys():
            if count[k] == i:
                sorted_dict[k] = count[k]
                break

    #get percentages of values for supplied key
    print("\nPercentages of '{}' values in cowrie logs ({} total calls with this key)...".format(key, str(int(total_items))))


    #print off percentages for each
    for k,v in sorted_dict.items():
        percent = float(v)/total_items
        percentage = round(percent*100,2)
        print("{}- {}% ({})\n".format(k,str(percentage),str(v)))
    
    print("\n\n")


def run_main_menu():
    '''runs main menu and stores data and paths and report names we are using'''

    #set the path here if you want. Relative or absolute. If it is a folder it will combine all of the shallow contents in that folder.
    path_to_look = "/Users/jcheist/Coding/CSCI_432/SecurityFinalProject/logFiles"
    list_of_paths = []
    report_name = ""
    data = []


    keepGoing = True #sentry variable to keep program running

    while (keepGoing):#true until user chooses to quit the program
        
        #retains functionality of seeting path to look in line above this if desired. Get path if needed.
        if path_to_look == "":
            path_to_look = FileReadingUtilities.get_path_to_use()

        #determine file paths and report output name
        if len(list_of_paths) == 0 or report_name == "":
            #list of files to parse and read in, report name
            list_of_paths, report_name = FileReadingUtilities.get_files_to_parse(path_to_look)

        #read in data from files
        if len(data) == 0:
            data = DictionaryUtilites.get_data_from_logs(list_of_paths)

        #allow user to choose program mode
        selection = input("""Would you like to...
            1) Run Reports
            2) Query Results
            3) Choose new data.
            0) Quit the Program\n""")


        if selection == '1':# enter report selection
            run_reports_menu(report_name, data, list_of_paths)

        elif selection == '2': #query results
            run_query_results_menu(data, list_of_paths)
            
        elif selection == '3': #reset current data so user can enter new files for new data
            path_to_look = ""
            list_of_paths = []
            report_name = ""
            data = []
            needs_to_choose_location = True
        elif selection == '0':#exit program
            keepGoing = False
        else:#input not recognized
            print("Input not recognized.\n")


if __name__ == "__main__":
    run_main_menu()
