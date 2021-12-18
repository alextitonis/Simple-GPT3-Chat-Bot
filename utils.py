def read_file(filename):
    print(filename)
    with open(filename, 'r') as infile:
        text = infile.read()
    return text