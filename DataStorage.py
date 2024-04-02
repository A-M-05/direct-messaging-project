from Profile import Profile, DsuFileError, DsuProfileError
from ds_messenger import DirectMessage
from pathlib import Path
import json, time


class DataStorage(Profile):
    def __init__(self, dsuserver = None, username = None, password = None):
        super().__init__(dsuserver=dsuserver, username=username, password=password)
        self.dm_dictionary = dict()

    def add_dm(self, dm: DirectMessage):
        if dm.get_recipient() in self.dm_dictionary.keys():
            self.dm_dictionary[dm.get_recipient()].append(dm)
        else:
            self.dm_dictionary[dm.get_recipient()] = list()
            self.dm_dictionary[dm.get_recipient()].append(dm)

    def convert_dms_to_tuples(self) -> None:

        temp = dict()
        for key in self.dm_dictionary.keys():
            temp[key] = []
            for dm in self.dm_dictionary[key]:
                temp[key].append(self._unpack_dm(dm))

        self.dm_dictionary.clear()
        self.dm_dictionary.update(temp)
        print(self.dm_dictionary)
        del temp

    def _unpack_dm(self, dm: DirectMessage):
        return (dm.get_recipient(), dm.get_message(), dm.get_timestamp(), dm.get_sender())

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.dm_dictionary = obj['dm_dictionary']
                try:
                    for i in self.dm_dictionary.values():
                        temp = DirectMessage(None, None, None, None)
                        for j in range(len(i)):
                            temp = DirectMessage(i[j][0], i[j][1], i[j][2], i[j][3])
                            i[j] = temp
                except:
                    raise
                f.close()
    

            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
        
        