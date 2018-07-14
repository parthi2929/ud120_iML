"""
convert dos linefeeds (crlf) to unix (lf)
usage: dos2unix.py 
link: https://github.com/udacity/ud120-projects/issues/46
"""
original = "../tools/word_data.pkl"
destination = "word_data_UNIX.pkl"

content = ''
outsize = 0
with open(original, 'rb') as infile:
    content = infile.read()
with open(destination, 'wb') as output:
    for line in content.splitlines():
        outsize += len(line) + 1
        output.write(line + str.encode('\n'))

print("Done. Saved %s bytes." % (len(content)-outsize))