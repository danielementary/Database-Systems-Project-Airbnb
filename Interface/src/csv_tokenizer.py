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
