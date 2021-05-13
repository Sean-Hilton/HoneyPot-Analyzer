from CowrieDefinitions import LogKeys
from Utilities import DictionaryUtilites, GeneralUtilities
from aslookup import get_as_data#For ASN

class ReportGenerator:
    '''Class that handles report generation.'''

    def generate_standard_top_10_report(data, report_name_base):
        '''generates original report we had.'''
        items = [LogKeys.PASSWORD, LogKeys.USERNAME]
        ReportGenerator.generate_top_10_report(data, report_name_base)


    def generate_top_10_report(data, report_name_base, query_keys):
        '''Generates a report for the top 10 most common IP addresses for the supplied query keys.'''

        print("Beginning top 10 report generation for the following keys.")

        report_name = "{}_Top10.txt".format(report_name_base)

        ## Get a list of all IP addresses that connected to the honeypot.
        ## And a deduplicated list too, Then calculate the top ten IP addresses
        ## and how often they connected
        print("Getting list of ip addresses.")
        ip_list, deduped_ip_list = DictionaryUtilites.get_lists(data, LogKeys.SRC_IP.key())
        print("Getting top 10 list by ip address.")
        top_ten_ips, ip_freq_dict = DictionaryUtilites.get_top_ten(ip_list, deduped_ip_list)

        top_ten_lists = {}

        for key in query_keys:
            #src ip will always be in a report
            if key == LogKeys.SRC_IP:
                continue
            ## Get a list of all key type used and a list of deduplicated items
            ## Then use those to calculate the top ten key type and how often they were used
            desc = key
            key = key
            if isinstance(key,LogKeys):
                desc = key.description()
                key = key.key()

            print("Getting list of {}.".format(desc))
            item_list, deduped_item_list = DictionaryUtilites.get_lists(data, key)
            print("Getting top 10 list by {}.".format(desc))
            top_ten_items, item_freq_dict = DictionaryUtilites.get_top_ten(item_list, deduped_item_list)

            top_ten_lists[key] = [top_ten_items, item_freq_dict]
        

        print("Beginning to write report '{}'.".format(report_name))
        #write report
        with open(report_name, 'w') as f:
            #write header for report
            f.write("\n\n\t\tHONEYPOT Top 10 IP ANALYSIS\n\n")
            f.write ("Total unique attacker IPS: {}\n".format(len(deduped_ip_list)))
            f.write("Top 10 attackers by IP:\n")
            f.write("\tIP\t\tConnections\tCountry\tCity")

            for x in top_ten_ips:

                #Gets ASN
                xx = get_as_data(x, service='cymru')
                
                f.write("\t{:15}\t{}".format(x, ip_freq_dict[x])),
                country, city = GeneralUtilities.get_ip_location(x)
                f.write ('\t\t\t\t\t{}\t{}'.format(country, city))
                f.write("\n\nAs #: "+ xx[1]+ "\t\t" + xx[2])
                f.write("\n----------------\n" )
                for key in query_keys:
                    f.write("\tMost common {}s".format(key.description()))
                f.write(":\n")
                
                for x in range(0,10):
                    for key,items in top_ten_lists.items():
                        try:
                            top_ten_items = items[0]
                            top_ten_freq = items[1]
                            f.write("\t{:25}\t{}".format(top_ten_items[x], top_ten_freq[top_ten_items[x]]))
                        except:
                            pass
                    f.write("\n")

        print("Done Generating report named '{}'.".format(report_name))
