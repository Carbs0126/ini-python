class INIEntryObject:

    def __init__(self):
        self.ini_kv_pair = None
        self.comments = None

    def set_kv_pair(self, ini_kv_pair):
        self.ini_kv_pair = ini_kv_pair

    def get_kv_pair(self):
        return self.ini_kv_pair

    def add_comments(self, comments):
        if (comments is None) or len(comments) == 0:
            return

        if self.comments is None:
            self.comments = list()

        self.comments.extend(comments)

    def add_comment(self, comment):
        if self.comments is None:
            self.comments = list()
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

    def generate_content_lines(self):
        lines = list()
        if self.comments is not None:
            lines.extend(self.comments)
        if self.ini_kv_pair is not None:
            lines.append(self.ini_kv_pair)
        return lines
