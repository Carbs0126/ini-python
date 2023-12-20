import abc


class INIContent(abc.ABC):

    @abc.abstractmethod
    def get_position(self):
        pass

    @abc.abstractmethod
    def to_ini_output_string(self):
        pass

    def __lt__(self, other):
        # sorted()函数的返回值，将会从大到小排序
        # return self.population > other.population
        if other is None:
            return False
        ini_position_a = self.get_position()
        ini_position_b = other.get_position()
        if ini_position_a is None or ini_position_b is None:
            return False
        line_number_delta = ini_position_a.line_number - ini_position_b.line_number
        if line_number_delta < 0:
            return True
        elif line_number_delta > 0:
            return False
        else:
            return ini_position_a.char_begin < ini_position_b.char_begin
