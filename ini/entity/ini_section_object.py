class INISectionObject:

    def __init__(self):
        self.ini_section_header = None
        self.comments = None
        self.entry_objects = None

    def add_comment(self, ini_comment):
        if self.comments is None:
            self.comments = list()
        self.comments.append(ini_comment)

    def add_comments(self, ini_comments):
        if (ini_comments is None) or len(ini_comments) == 0:
            return
        if self.comments is None:
            self.comments = list()
        self.comments.extend(ini_comments)

    def get_comments(self):
        return self.comments

    def add_entry_object(self, entry_object):
        if self.entry_objects is None:
            self.entry_objects = list()
        self.entry_objects.append(entry_object)

    def get_name(self):
        return self.ini_section_header.name

    def set_section_header(self, ini_section_header):
        self.ini_section_header = ini_section_header

    def get_section_header(self):
        return self.ini_section_header

    def generate_content_lines(self):
        lines = list()
        if self.comments is not None:
            lines.extend(self.comments)
        if self.ini_section_header is not None:
            lines.append(self.ini_section_header)

        for ini_entry_object in self.entry_objects:
            if ini_entry_object is not None:
                entry_lines = ini_entry_object.generate_content_lines()
                if (entry_lines is not None) and len(entry_lines) > 0:
                    lines.extend(entry_lines)
        return lines
