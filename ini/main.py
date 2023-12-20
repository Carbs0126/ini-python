import os

from ini.ini_file_parser import INIFileParser
from ini.ini_file_generator import INIFileGenerator
from ini.entity.ini_section_object import INISectionObject
from ini.entity.ini_entry_object import INIEntryObject
from ini.atom.ini_section_header import INISectionHeader
from ini.atom.ini_kv_pair import INIKVPair

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    abs_input_ini_file = os.path.join(current_dir, "test-input.ini")
    abs_output_ini_file = os.path.join(current_dir, "test-output.ini")
    iniObject = INIFileParser.parse_file_to_ini_object(abs_input_ini_file)

    iniSectionObject = INISectionObject()
    iniSectionHeader = INISectionHeader("[new_section]", None);
    iniSectionObject.set_section_header(iniSectionHeader)

    iniEntryObject1 = INIEntryObject()
    iniEntryObject1.set_kv_pair(INIKVPair("new_key", "new_value", None))
    iniEntryObject2 = INIEntryObject()
    iniEntryObject2.set_kv_pair(INIKVPair("new_key2", "new_value2", None))

    iniSectionObject.add_entry_object(iniEntryObject1)
    iniSectionObject.add_entry_object(iniEntryObject2)

    iniObject.add_section(iniSectionObject)

    INIFileGenerator.generate_file_from_ini_object(iniObject, abs_output_ini_file)
