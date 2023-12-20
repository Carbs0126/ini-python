from ini.atom.interfaces.ini_content import INIContent


class INIComment(INIContent):

    def __init__(self, comment, ini_position):
        self.comment = comment
        self.ini_position = ini_position

    def get_position(self):
        return self.ini_position

    def to_ini_output_string(self):
        return self.comment

    def __str__(self):
        return "INIComment{comment=" + self.comment + ", iniPosition=" + self.ini_position + '}'
