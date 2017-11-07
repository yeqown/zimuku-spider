import os
import os.path as path
# import sys
import re
import codecs
# import chardet
import fnmatch
import shutil


def filter_line(line):
    '''
    A filter to choose one line is a needed line or not
    @parameter line str
    @return bool: True means need to pass, False means no need to pass this line
    '''
    line = line.strip("\n")
    # rule0: 长度<=1
    if len(line) <= 1:
        return True
    # # rule1: 数字，过滤掉
    if line.isdigit():
        # if re.search(r"^[0-9]$", line):
        return True
    # rule2: 时间进度控制，过滤掉
    if re.search(r"-->", line):
        return True
    # rule3: 含有英文，过滤掉
    if re.search(r"[a-zA-Z]+", line):
        return True
    # rule4：含有[], 过滤掉
    if re.search(r"^\[", line):
        return True
    # rule5 "{....}" passed:
    if line.startswith("{") and line.endswith("}"):
        return True
    # rule6 "♪" passed
    if re.search(r"♪+", line):
        return True
    # rule7 "：" passed
    if re.search(r"：", line):
        return True
    if re.search(r"（+）+", line):
        return True
    # print(line, len(line))
    return False


def format_line(line):
    # 替换句子中的符号‘-’
    line = line.replace("-", "").replace(
        "<i>", "").replace("(", "").replace(
        ")", "").replace("\"", "").replace("”", "").replace("“", "")
    # 去掉头尾的空格
    line = line.strip()
    line += "\n"
    return line


def extract_file(in_filename, out_filename):
    '''
    file encoding is `utf-8`
    @parameter in_filename [str]
    @parameter out_filename [str]
    @return None
    '''
    with open(in_filename, "r") as fd:
        lines = []
        for line in fd.readlines():
            if filter_line(line):
                continue
            # filter_line retruns False
            line = format_line(line)
            if line not in lines:
                lines.append(line)
    with open(out_filename, "w") as fd_out:
        fd_out.writelines(lines)
    print("saved extract lines into [{}] finished".format(out_filename))


def loop_dir_to_extract_file(in_path):
    '''
    os.walk path to extract file in [*.srt file]
    @parameter in_path [str]
    @return None
    '''
    for dirpath, dirname, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.srt"):
            in_file_path = path.join(dirpath, filename)

            out_file_path = path.join(path.abspath(
                path.join(dirpath, "../origin_corpus")), filename)
            out_file_path += "extract"
            extract_file(in_file_path, out_file_path)


def extract_files_dontneeds_anymore(in_path):
    for dirpath, dirname, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.srt"):
            file_path = path.join(dirpath, filename)
            # do extract action
            shutil.remove(file_path)
            print("{} removed".format(file_path))

if __name__ == "__main__":
    dirpath = path.abspath("./srt")
    # file_path = path.abspath("./srt/师任堂：光的日记.사임당 빛의 일기.E07.170215.720p-NEXT.chs.srt")
    # extract_file(file_path, "./origin_corpus/师任堂：光的日记.사임당 빛의 일기.E07.170215.720p-NEXT.chs.srt.extract")
    #===== 找到目录下所有需要过滤的文件
    loop_dir_to_extract_file(dirpath)
