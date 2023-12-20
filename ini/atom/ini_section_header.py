from ini.atom.interfaces.ini_content import INIContent


class INISectionHeader(INIContent):

    def __init__(self, name, ini_position):
        self.name = name
        self.ini_position = ini_position

    def get_position(self):
        return self.ini_position

    def to_ini_output_string(self):
        if (self.name is None) or len(self.name) == 0:
            raise RuntimeError("Key of INISectionHeader should not be empty")

        return self.name

    def __str__(self):
        return "INISectionHeader{name=" + self.name + ", iniPosition=" + self.ini_position + '}';
