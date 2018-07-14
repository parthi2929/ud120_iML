import sys


def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

with open(sys.argv[1], 'rb') as f:
    if b'\x9d' in f.read():
        print('this file has a problem {}'.format(f.tell()))

with open(sys.argv[1]) as f:
    try:
        contents = f.read()
    except Exception as e:
        e = str(e)
        expecting_error = "codec can't decode byte"
        if expecting_error in e:
            index_1 = find_str(e, 'position')
            index_1 = index_1 + len('position ')
            index_2 = find_str(e, ':')            
            byte_pos = e[index_1:index_2]

            index_1 = find_str(e, 'byte')
            index_1 = index_1 + len('byte ')
            index_2 = find_str(e, 'in')            
            byte = e[index_1:index_2]

            print (byte_pos, byte)
            

