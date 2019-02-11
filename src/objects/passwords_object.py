from helpers import date_helper
import json
import pickle

class StorageNode:
    _MAX_LEVELS = 3

    def __init__(self, parent=None, key=None) -> None:
        super().__init__()

        if not key:
            key = ""

        if not parent:
            self.level = 0
            self.key = ""
        else:
            self.level = parent.level + 1
            self.key = key

        self.last_modified = date_helper.curr_time_in_secs()
        if self.level == StorageNode._MAX_LEVELS:
            self.value = ""
        else:
            self.children = {}

    def set_value(self, key, value):
        if self.level == StorageNode._MAX_LEVELS:
            self.value = value
            self.last_modified = date_helper.curr_time_in_secs()
            return

        if key == "":
            self.last_modified = date_helper.curr_time_in_secs()
            return

        keys = key.split("/")
        if keys[0] not in self.children:
            self.children[keys[0]] = StorageNode(self, keys[0])

        self.children[keys[0]].set_value("/".join(keys[1:]), value)

    def get_values(self, key):
        if self.level == StorageNode._MAX_LEVELS:
            if key != "":
                return None
            else:
                return [self.value]

        if key == "":
            return [*self.children]

        keys = key.split("/")
        if keys[0] not in self.children:
            return None

        return self.children[keys[0]].get_values("/".join(keys[1:]))

    def remove_value(self, key, force=False):
        if self.level == StorageNode._MAX_LEVELS:
            return key == ""

        if key == "":
            return force

        keys = key.split("/")
        if keys[0] not in self.children:
            return False

        if self.children[keys[0]].remove_value("/".join(keys[1:]), force):
            del self.children[keys[0]]

        return len(self.children) == 0

    def to_bytes(self):
        return pickle.dumps(self)
        # return json.dumps(self, default=lambda o: o.__dict__,
        #                   sort_keys=True, indent=4)

    @classmethod
    def from_bytes(cls, data):
        return pickle.loads(data)


# sNode = StorageNode()
# sNode.set_value("google/gmail/utka", "asdf")
# sNode.set_value("voda/gmail/utka", "asdf")
# sNode.set_value("google/drive/utka", "asdf")
# sNode.set_value("google/gmail/riya", "asdf")
# print(sNode.get_values("google/gmail"))
# print(sNode.to_bytes())
#
# sNode2 = StorageNode.from_bytes(sNode.to_bytes())
# print(sNode2.to_bytes())
