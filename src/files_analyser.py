"""
--------------
FILES ANALYSER
--------------

* Counts no. of files in the given extension.
* Counts no. of source lines in the given extension.
* Path name of the folder should be given.

"""


import os



def get_file_list(Dir, SkipDir_disabled, dir_filt):
    """Gets the path as the argument and,
    Returns the list of file names in it, whatever the folder structure maybe"""
    
    lst_contents = os.scandir(Dir)
    lst_files = []
    #lst_f_h = []

    for item in lst_contents:
        if item.is_file():
            lst_files.append(Dir + '/' + item.name)
            #lst_f_h.append(item)
        elif (item.is_dir()) and ((SkipDir_disabled) or (item.name not in dir_filt)):
            #lst_files_temp, lst_f_h_temp = get_file_list(Dir + "\\" + item.name, SkipDir_disabled, dir_filt)
            lst_files_temp = get_file_list(Dir + "/" + item.name, SkipDir_disabled, dir_filt)
            lst_files.extend(lst_files_temp)
            #lst_f_h.extend(lst_f_h_temp)
    
    return lst_files#, lst_f_h


def fetch_str_result(info):
    """Gets the result of the analysis as a dictionary and,
    Returns it in a good structured string"""

    result = ""
    for ext in info:
        result += "\n"
        #result += "Number of " + ext[1:] + " files = " + str(info[ext][0]) + "\n"
        #result += "Number of " + ext[1:] + " source lines = " + str(info[ext][1]) + "\n\n"
        result += "Number of " + ext[1:] + " files = " + str(len(info[ext])) + "\n"
        sum_lines = 0
        for file_name in info[ext]: sum_lines += info[ext][file_name]
        result += "Number of " + ext[1:] + " source lines = " + str(sum_lines) + "\n"

    result += "\n" + "-" * 90

    for ext in info:
        result += "\n\n"
        result += ext[1:] + " Files:\n\n"
        for file_name in info[ext]: result += file_name + " --- " + str(info[ext][file_name]) + "\n"

    result += "-" * 90

    return result


def fetch_metrics(path, filters, skip_Dirs_disabled = True, dirFilt = ""):
    """Analyses the given path and collects the data 
    And returns the metrics result as a dictionary"""

    '''
    print("\n\n", "Given Path: " + path, "\n", sep = "\n")

    for item in os.scandir(path):
        print(item.is_file(),item.is_dir(),item.name)
    print("\n\n\n")

    '''

    dirFilt_temp = dirFilt.split(",")
    dir_filters = []
    for dir_temp in dirFilt_temp:
        Dir = dir_temp.strip()
        if Dir not in dir_filters: dir_filters.append(Dir)


    #file_lst, f_h_lst = get_file_list(path, skip_Dirs_disabled, dir_filters)
    file_lst = get_file_list(path, skip_Dirs_disabled, dir_filters)
    '''
    print("List of files:")
    print("-------------\n")
    for file_name in file_lst:
        print("*",file_name)


    f_h = f_h_lst[0]
    print(open(f_h).read())
    '''


    ext_lst_temp = filters.split(",")
    ext_lst = []
    for ext_temp in ext_lst_temp:
        ext = ext_temp.strip()
        ext = ext.lstrip('*.')
        ext = "." + ext
        if ext not in ext_lst: ext_lst.append(ext)
    # print("\n\n", ext_lst, sep = "\n")

    result = {}
    for ext in ext_lst:
        result[ext] = {}
        for file_name in file_lst:
            if file_name.endswith(ext):
                with open(file_name, 'r', encoding = 'utf-8') as f_handle:
                    n_lines = len(f_handle.readlines())
                    result[ext]["." + file_name[len(path):]] = n_lines

    #details = {}
    #result = {}
    #for ext in ext_lst:
    #    details[ext] = []
    #    result[ext] = [0, 0]
    #    for ind in range(len(file_lst)):
    #        if file_lst[ind].endswith(ext): details[ext].append(f_h_lst[ind])
    
    #for ext in details:
    #    result[ext][0] = len(details[ext])
    #    for file_h in details[ext]:
    #        with open(file_h, 'r', encoding = 'utf-8') as f_handle:
    #            n_lines = len(f_handle.readlines())
    #            result[ext][1] += n_lines
    
    return result


def validate_path(path):
    """Returns True if the given path is valid and False otherwise"""

    valid = True

    try: os.scandir(path)
    except: valid = False

    return valid


if __name__ == "__main__":

    print("\n")
    print("-" * 66)
    print("NOTE: Run 'code_metrics.py' to start the complete GUI application.")
    print("-" * 66)
    print("\n")

    print('''
CODE METRICS V:1.x.x
--------------------
''')

    path = input("PATH : ")
    filters = input("FILTERS : ")

    data = fetch_metrics(path, filters)
    result = fetch_str_result(data)

    print("\n\nResult :")
    print("-------")
    print(result)





# END
