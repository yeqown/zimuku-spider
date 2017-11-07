'''
    convert file encoding into utf-8 so processor will deal with file easily
'''
import codecs
import os.path as path
# import sys
import os
import chardet
import fnmatch
# import shutil

look_utf8 = codecs.lookup("utf-8")


def codecs_format_file(file_path):
    '''
    Use codecs to format file in to encoding 'utf-8'
    @parameter file_path [str]
    @return None
    '''
    with open(file_path, "rb") as fd:
        data = fd.read()
    encoding = chardet.detect(data)
    print(encoding)
    if encoding["encoding"] == "utf-8":
        return True

    file = codecs.open(file_path, "r", encoding["encoding"])
    try:
        data = file.read()
    except Exception as e:
        print("while format {} raise {}".format(file_path, str(e)))
        return False
    file.close()
    # print("read done")
    with open(file_path, "w") as fd:
        fd.write(data)
    # print("write done")
    return True


def format_files_in_path(in_path):
    '''
    format files in path with encoding 'utf-8'
    @parameter in_path [str]
    @return None
    '''
    cnt = 0
    err_cnt = 0
    for dirpath, dirname, filenames in os.walk(in_path):
        for filename in fnmatch.filter(filenames, "*.srt"):
            cnt += 1
            file_path = path.join(dirpath, filename)
            # file_paths.append(file_path)
            if not codecs_format_file(file_path):
                err_cnt += 1
                os.remove(file_path)
            print("{} format done".format(file_path))
    print("Total {} files, {} Error".format(cnt, err_cnt))


if __name__ == "__main__":
    # file_path = path.abspath("./srt/姐妹情深.srt")
    # codecs_format_file(file_path)
    dir_path = path.abspath("./srt")
    format_files_in_path(dir_path)
