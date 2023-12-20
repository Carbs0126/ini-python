from ini.atom.interfaces.ini_content import INIContent


class INIKVPair(INIContent):

    def __init__(self, key, value, ini_position):
        self.key = key
        self.value = value
        self.ini_position = ini_position

    def get_position(self):
        return self.ini_position

    def to_ini_output_string(self):
        if (self.key is None) or len(self.key) == 0:
            raise RuntimeError("Key of INIEntry should not be empty")

        if self.value is None:
            self.value = ""

        return self.key + "=" + self.value

    def __str__(self):
        return "INIKVPair{key=" + self.key + " value=" + self.value + ", iniPosition=" + self.ini_position + '}';
