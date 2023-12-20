from ini.atom.interfaces.ini_content import INIContent
from ini.atom.ini_comment import INIComment
from ini.atom.ini_section_header import INISectionHeader
from ini.atom.ini_empty import INIEmpty
from ini.atom.ini_kv_pair import INIKVPair
from ini.position.ini_position import INIPosition
from ini.entity.ini_object import INIObject
from ini.entity.ini_entry_object import INIEntryObject
from ini.entity.ini_section_object import INISectionObject


class INIFileParser:
    @staticmethod
    def parse_file_to_ini_object(ini_file_path):
        fd = open(ini_file_path, encoding='utf-8', mode='r')
        content = fd.readlines()
        fd.close()

        ini_lines = list()
        line_number = 0
        file_name = ini_file_path

        for item in content:
            origin_line = "" if item is None else item
            trimmed_line = origin_line.strip()
            if trimmed_line.startswith(";"):
                ini_comment = INIComment(origin_line.rstrip(), INIPosition(file_name, line_number, 0, len(origin_line)))
                INIFileParser.append_line_content_info_line_list(ini_comment, ini_lines)
            elif trimmed_line.startswith("["):
                right_square_brackets_position = trimmed_line.find(']')
                if right_square_brackets_position < 2:
                    raise RuntimeError(
                        "Right square bracket's position should be greater than 1, now it is " + right_square_brackets_position)
                section_name = trimmed_line[0: right_square_brackets_position + 1]
                if section_name.find(";") > -1:
                    raise RuntimeError("Section's name should not contain ';' symbol")
                char_begin = origin_line.find("[")
                char_end = origin_line.find("]")
                section_header = INISectionHeader(section_name,
                                                  INIPosition(file_name, line_number, char_begin, char_end))
                INIFileParser.append_line_content_info_line_list(section_header, ini_lines)
                INIFileParser.check_semicolon(origin_line, char_end + 1, ini_lines, file_name, line_number)
            elif len(trimmed_line) == 0:
                ini_empty = INIEmpty(INIPosition(file_name, line_number, 0, 0))
                INIFileParser.append_line_content_info_line_list(ini_empty, ini_lines)
            else:
                # kv
                index_of_equal_in_trimmed_string = trimmed_line.find("=")
                if index_of_equal_in_trimmed_string < 1:
                    raise RuntimeError("Equal's position should be greater than 0")
                index_of_equal_in_origin_string = origin_line.find("=")
                key_name = trimmed_line[0: index_of_equal_in_trimmed_string].strip()
                right_string_of_equal = trimmed_line[index_of_equal_in_trimmed_string + 1:]
                value_name_string_buffer = ""
                length = len(right_string_of_equal)
                if length > 0:
                    # 1. 过滤前面的空格，还未找到value
                    # 2. 正在记录value
                    # 3. value结束
                    stat = 0
                    i = 0
                    while (i < length):
                        c = right_string_of_equal[i]
                        if stat == 0:
                            # 过滤前面的空格
                            if c == " " or c == "\t":
                                continue
                            else:
                                stat = 1
                                value_name_string_buffer += c
                        elif stat == 1:
                            # 正在记录value
                            # value中允许有空格
                            if c == ";":
                                stat = 2
                                break
                            else:
                                stat = 1
                                value_name_string_buffer += c
                        i += 1

                    value_name = value_name_string_buffer
                    char_begin = origin_line.find(key_name)
                    char_end = index_of_equal_in_origin_string + 1 + i
                    ini_kv_pair = INIKVPair(key_name, value_name,
                                            INIPosition(file_name, line_number, char_begin, char_end))
                    INIFileParser.append_line_content_info_line_list(ini_kv_pair, ini_lines)
                    if i != length:
                        # 没有到结尾，检查是不是有分号
                        INIFileParser.check_semicolon(origin_line, index_of_equal_in_origin_string + 1 + i, ini_lines,
                                                      file_name, line_number)
            line_number += 1

        # 最终解析为一个实体
        ini_object = INIObject()
        # 收集 section 或者 kv 的 comments
        comments_cache = list()
        # 解析完当前的 section，一次存入
        current_section_object = None
        # 解析当前的 kvPair
        current_entry_object = None

        # 0 解析 section 阶段，还没有解析到 section
        # 1 已经解析出 sectionName阶段（刚刚解析完 section header）还没有解析到下一个section
        parse_state = 0
        pre_ini_content = None
        cur_ini_content = None
        for ini_content in ini_lines:
            if isinstance(ini_content, INIEmpty):
                continue
            cur_ini_content = ini_content
            if isinstance(cur_ini_content, INIComment):
                ini_comment = cur_ini_content
                if parse_state == 0:
                    # 还没解析到 section
                    comments_cache.append(ini_comment)
                else:
                    if isinstance(pre_ini_content, INISectionHeader):
                        if INIFileParser.check_same_line(pre_ini_content, cur_ini_content):
                            # 当前 comment 属于 section
                            comments_cache.append(ini_comment)
                            if current_section_object is None:
                                current_section_object = INISectionObject()
                            current_section_object.add_comments(comments_cache)
                            comments_cache.clear()
                            # 当前 section 的所有 comment 已经结束
                        else:
                            # 当前 comment 属于当前 section 的 kv 或者下一个 section 的 section
                            if current_section_object is None:
                                current_section_object = INISectionObject()
                            current_section_object.add_comments(comments_cache)
                            comments_cache.clear()
                            comments_cache.append(ini_comment)
                    elif isinstance(pre_ini_content, INIComment):
                        # comment 累加
                        comments_cache.append(ini_comment)
                    elif isinstance(pre_ini_content, INIKVPair):
                        if INIFileParser.check_same_line(pre_ini_content, cur_ini_content):
                            # 当前 comment 属于 kv
                            comments_cache.append(ini_comment)
                            if current_entry_object is None:
                                # 不走这里
                                current_entry_object = INIEntryObject()
                            current_entry_object.add_comments(comments_cache)
                            if current_section_object is None:
                                current_section_object = INISectionObject()
                            current_section_object.add_entry_object(current_entry_object)
                            current_entry_object = None
                            comments_cache.clear()
                            # 当前 kv 收尾
                        else:
                            # 当前 comment 属于当前 section 的下一个 kv 或者下一个 section 的 section
                            comments_cache.clear()
                            comments_cache.append(ini_comment)
            elif isinstance(cur_ini_content, INISectionHeader):
                ini_section_header = cur_ini_content
                if parse_state == 0:
                    # 解析到第一个 section
                    parse_state = 1
                    current_section_object = INISectionObject()
                    current_section_object.set_section_header(ini_section_header)
                else:
                    if isinstance(pre_ini_content, INISectionHeader):
                        # 连着两个 section header
                        # 收尾上一个 section header
                        if current_section_object is not None:
                            current_section_object.add_comments(comments_cache)
                            comments_cache.clear()
                            ini_object.add_section(current_section_object)

                        # 新建 section header
                        current_section_object = INISectionObject()
                        current_section_object.set_section_header(ini_section_header)
                    elif isinstance(pre_ini_content, INIComment):
                        if len(comments_cache) == 0:
                            # 说明上一个 comment 和其之前的元素是一行，需要收尾上一个 section
                            if current_section_object is not None:
                                ini_object.add_section(current_section_object)
                            current_section_object = INISectionObject()
                            current_section_object.set_section_header(ini_section_header)
                        else:
                            current_section_object = INISectionObject()
                            current_section_object.set_section_header(ini_section_header)
                            current_section_object.add_comments(comments_cache)
                            comments_cache.clear()
                    elif isinstance(pre_ini_content, INIKVPair):
                        # 说明上一个section 结束了，需要收尾
                        if current_section_object is not None:
                            if current_entry_object is not None:
                                current_section_object.add_entry_object(current_entry_object)
                                current_entry_object = None
                            ini_object.add_section(current_section_object)
                        current_section_object = INISectionObject()
                        current_section_object.set_section_header(ini_section_header)
            elif isinstance(cur_ini_content, INIKVPair):
                ini_kv_pair = cur_ini_content
                if parse_state == 0:
                    # 没有 section 就出现了 kv，说明格式出错
                    raise RuntimeError("There should be a section header before key-value pairs")
                else:
                    if isinstance(pre_ini_content, INISectionHeader):
                        current_entry_object = INIEntryObject()
                        current_entry_object.set_kv_pair(ini_kv_pair)
                    elif isinstance(pre_ini_content, INIComment):
                        if len(comments_cache) == 0:
                            # 说明上一行中，comment 是右边的注释，还包含左边的元素
                            # 当上一行的左侧是 section 时，不需要关心 section
                            # 当上一行的左侧是 kv 时，不需要关心当前 section 或者上一个 kv
                            current_entry_object = INIEntryObject()
                            current_entry_object.set_kv_pair(ini_kv_pair)
                        else:
                            current_entry_object = INIEntryObject()
                            current_entry_object.set_kv_pair(ini_kv_pair)
                    elif isinstance(pre_ini_content, INIKVPair):
                        # 把前一个 kv 收尾到 section 中
                        if current_entry_object is not None:
                            current_entry_object.add_comments(comments_cache)
                            comments_cache.clear()
                            if current_section_object is not None:
                                current_section_object.add_entry_object(current_entry_object)
                        current_entry_object = INIEntryObject()
                        current_entry_object.set_kv_pair(ini_kv_pair)

            pre_ini_content = cur_ini_content
        # 最后一个元素
        if current_entry_object is not None:
            current_entry_object.add_comments(comments_cache)
            comments_cache.clear()
        if current_section_object is not None:
            current_section_object.add_comments(comments_cache)
            comments_cache.clear()
            if current_entry_object is not None:
                current_section_object.add_entry_object(current_entry_object)
                current_entry_object = None
            ini_object.add_section(current_section_object)

        return ini_object

    @staticmethod
    def append_line_content_info_line_list(ini_content: INIContent, ini_lines: list):
        ini_lines.append(ini_content)

    @staticmethod
    def check_semicolon(origin_str: str, char_begin, ini_lines, file_location, line_number):
        remain_str = origin_str[char_begin:]
        trimmed_remain_str = remain_str.strip()
        if len(trimmed_remain_str) > 0:
            if trimmed_remain_str.startswith(";"):
                ini_comment = INIComment(trimmed_remain_str,
                                         INIPosition(file_location, line_number, origin_str.find(";"),
                                                     len(origin_str)))
                INIFileParser.append_line_content_info_line_list(ini_comment, ini_lines)
                return ini_comment
            else:
                raise RuntimeError("Need ';' symbol, but find " + trimmed_remain_str[0] + " instead")
        return None

    @staticmethod
    def check_same_line(pre_ini_content: INIContent, cur_ini_content: INIContent):
        if (pre_ini_content is not None) and (cur_ini_content is not None):
            pre_position = pre_ini_content.get_position()
            cur_position = cur_ini_content.get_position()
            return pre_position.line_number == cur_position.line_number
        return False
