class INIPosition:
    def __init__(self, file_location, line_number, char_begin, char_end):
        self.file_location = file_location
        self.line_number = line_number
        self.char_begin = char_begin
        self.char_end = char_end

    def __str__(self):
        return "INIPosition{file_location=" + self.file_location + \
               ", line_number=" + self.line_number + \
               ", char_begin=" + self.char_begin + \
               ", char_end=" + self.char_end + \
               '}'
