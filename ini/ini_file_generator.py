from ini.entity.ini_object import INIObject


class INIFileGenerator:
    @staticmethod
    def generate_file_from_ini_object(ini_object: INIObject, file_absolute_path: str):
        if ini_object is None:
            raise RuntimeError("IniObject should not be None")
        lines = ini_object.generate_string_lines()
        if lines is None:
            return None

        output_file = INIFileGenerator.write_file(lines, file_absolute_path)
        return output_file

    @staticmethod
    def write_file(lines: list, file_absolute_path: str):
        fd = open(file_absolute_path, encoding='utf-8', mode='w')
        # print(file_absolute_path)
        line_len = len(lines)
        for index, line in enumerate(lines):
            # for line in lines:

            fd.write(line)
            if index < line_len - 1:
                fd.write("\n")
        fd.close()
        return fd
