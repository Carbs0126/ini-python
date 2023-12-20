# ini文件解析
## ini文件格式说明
https://zh.wikipedia.org/wiki/INI%E6%96%87%E4%BB%B6

``` java
; last modified 1 April 2001 by John Doe
[owner]
name=John Doe
organization=Acme Products

[database]
server=192.0.2.42 ; use IP address in case network name resolution is not working
port=143
file="acme payroll.dat"
```

## 附加说明
1. 键值对中，允许值中存在空格；
2. section 没有做嵌套处理

## 使用
```python
# 将一个文件中的内容解析为一个object
iniObject = INIFileParser.parse_file_to_ini_object(abs_input_ini_file)

# 为这个 iniobject 添加 section
iniSectionObject = INISectionObject()
iniSectionHeader = INISectionHeader("[new_section]", None);
iniSectionObject.set_section_header(iniSectionHeader)

# 新建键值对对象
iniEntryObject1 = INIEntryObject()
iniEntryObject1.set_kv_pair(INIKVPair("new_key", "new_value", None))
iniEntryObject2 = INIEntryObject()
iniEntryObject2.set_kv_pair(INIKVPair("new_key2", "new_value2", None))

# 把键值对添加到 section 中
iniSectionObject.add_entry_object(iniEntryObject1)
iniSectionObject.add_entry_object(iniEntryObject2)

# 添加section
iniObject.add_section(iniSectionObject)

# 将这个对象写入到ini文件中
INIFileGenerator.generate_file_from_ini_object(iniObject, abs_output_ini_file)
```
