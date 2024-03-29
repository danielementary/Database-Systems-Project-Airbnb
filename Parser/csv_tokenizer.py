# this tokenizer is built to read csv files output by the cleaning process,
# it follows our rules so is absolutely not general purpose

def tokenize(filename):
    """
    take a filename, read the csv and outputs a tuple containing in first position
        the list of columns (in string)
    in second position
        the list of list containing each line values as String
    """
    file = open(filename, 'r')

    lines = file.readlines()

    # first extracts columns name:
    columns = tokenize_line(lines[0])
    values_list = []

    for i in range(1, len(lines)):
        values = tokenize_line(lines[i])
        values_list.append(values)

    file.close()

    return (columns, values_list)

def tokenize_line(string):
    string_len = len(string)
    result = []
    in_string = False
    cur_elmt = ""
    i = 0

    while i < string_len:
        c = string[i]
        if (c == "," or c== "\n") and not in_string:
            cur_elmt = cur_elmt.replace("\n", "")
            result.append(cur_elmt)
            cur_elmt = ""
        else:
            if in_string and c == "'" :
                if string[i+1] == "'":
                    cur_elmt += "'"
                    i += 1
                else:
                    in_string = False
            elif not in_string and c == "'":
                in_string = True
            cur_elmt += c
        i += 1

    return result
