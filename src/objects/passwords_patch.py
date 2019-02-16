class PasswordPatch:
    def __init__(self, storage):
        self.storage = storage
        self.ops = {}

    def set_value(self, key, value):
        self.ops[key] = PasswordOperation(False, key, value)

    def remove_value(self, key):
        self.ops[key] = PasswordOperation(True, key)

    def get_values(self, key):
        if key in self.ops:
            operation = self.ops[key]
            if operation.del_op:
                return None
            else:
                return [operation.value]
        else:
            return self.storage.get_values(key)


class PasswordOperation:
    def __init__(self, del_op, key, value=None):
        self.del_op = del_op
        self.key = key
        if not self.del_op:
            self.value = value
