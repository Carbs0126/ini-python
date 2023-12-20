class INIObject:

    def __init__(self):
        self.sections_map = dict()
        self.ordered_sections_name = list()

    def generate_string_lines(self):
        ini_content_lines = list()
        for section_name in self.ordered_sections_name:
            if (section_name is not None) and (section_name in self.sections_map):
                ini_section_object = self.sections_map.get(section_name)
                one_section_lines = ini_section_object.generate_content_lines()
                if (one_section_lines is not None) and len(one_section_lines) > 0:
                    ini_content_lines.extend(one_section_lines)

        ini_content_lines = sorted(ini_content_lines)

        string_lines = list()

        string_buffer_one_line = ""

        pre_line_number = -1
        cur_line_number = -1

        for ini_content in ini_content_lines:
            if ini_content is None:
                continue
            cur_ini_position = ini_content.get_position()
            if cur_ini_position is None:
                if len(string_buffer_one_line) > 0:
                    string_lines.append(string_buffer_one_line)
                    string_buffer_one_line = ""
                string_lines.append(ini_content.to_ini_output_string())
                continue
            cur_line_number = cur_ini_position.line_number
            if pre_line_number != cur_line_number:
                if pre_line_number > -1:
                    string_lines.append(string_buffer_one_line)
                    string_buffer_one_line = ""
                line_delta = cur_line_number - pre_line_number
                if line_delta > 1:
                    # 中间有空行
                    for i in range(0, line_delta - 1):
                        string_lines.append("")
                string_buffer_one_line += ini_content.to_ini_output_string()
            else:
                string_buffer_one_line += ini_content.to_ini_output_string()

            pre_line_number = cur_line_number
        string_lines.append(string_buffer_one_line)
        return string_lines

    def add_section(self, ini_section_object):
        self.ordered_sections_name.append(ini_section_object.get_name())
        self.sections_map[ini_section_object.get_name()] = ini_section_object

    def get_section(self, section_name):
        if (section_name is None) or len(section_name) == 0 or (section_name not in self.sections_map):
            return None
        return self.sections_map[section_name]

    def get_sections_map(self):
        return self.sections_map

    def get_ordered_sections_name(self):
        return self.ordered_sections_name
