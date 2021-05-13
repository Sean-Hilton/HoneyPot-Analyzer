from enum import IntEnum

class LogKeys(IntEnum):
    '''Enum to store'''
    INVALID=0
    EVENT_ID=1
    SRC_IP=2
    SRC_PORT=3
    DEST_IP=4
    DEST_PORT=5
    SESSION=6
    PROTOCOL=7
    MESSAGE=8
    SENSOR=9
    TIMESTAMP=10
    USERNAME=11
    PASSWORD=12
    HASH=13


    def all_keys_dictionary():
        '''method to get this dictionary'''

            #dictionary of keys used for getting message values. 
        keyStringSwitch = {
            LogKeys.EVENT_ID:"eventid",
            LogKeys.SRC_IP:"src_ip",
            LogKeys.SRC_PORT:"src_port",
            LogKeys.DEST_IP:"dst_ip",
            LogKeys.DEST_PORT:"dst_port",
            LogKeys.SESSION:"session",
            LogKeys.PROTOCOL:"protocol",
            LogKeys.MESSAGE:"message",
            LogKeys.SENSOR:"sensor",
            LogKeys.TIMESTAMP:"timestamp",
            LogKeys.USERNAME:"username",
            LogKeys.PASSWORD:"password",
            LogKeys.HASH:"hassh"
        }

        return keyStringSwitch



    def key(self):
        '''gets the string value of the key for the enum. Matches key used in JSON logs dictionaries. (Returns 'Invalid' as default if key not found.)'''

        return LogKeys.all_keys_dictionary().get(self, "Invalid")


    def description(self):
        '''Gets more user readable form of the LogKey type.'''

        key = self.key()

        if key == "Invalid":#check if we failed to get a key
            print("Invalid key! Aborting!")
            return ""

        #convert to user readable and return
        key = key.capitalize()
        description = ""
        for i in range(len(key)):
            if (key[i] == '_'):
                description += ' '
            else:
                description += key[i]
        
        return description