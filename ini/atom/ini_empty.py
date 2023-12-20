from ini.atom.interfaces.ini_content import INIContent


class INIEmpty(INIContent):

    def __init__(self, ini_position):
        self.ini_position = ini_position

    def get_position(self):
        return self.ini_position

    def to_ini_output_string(self):
        return ""

    def __str__(self):
        return "INIEmpty{iniPosition=" + self.ini_position + '}'
