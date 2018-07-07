# -*- coding: utf-8 -*-
''' split large csv file into small ones
* how to use
-- in terminal, run the script with terminal arguments as follows:
    $python split_large_csv.py -name TARGET_FILE -size SHARD_SIZE
-- TARGET_FILE is the name of the file you want to split
-- SHARD_SIZE is number of lines in each small file

* assumption(s) on csv file format:
** assuming that csv file has a header line (the first line) which
    contains the labels of each column

* author: Yao

* maintenance history:
- July 7, 2018, initial release
'''

if __name__ == '__main__':
    ## default chunk size is 4000 (lines)
    fileName = None
    chunkSize = 4000

    ## try to read chunk size and file name from terminal arguments
    try:
        import sys, os, os.path
        args = sys.argv
        for i, arg in enumerate(args):
            if arg == '-name':
                if len(args) < i + 2:
                    raise ValueError('insufficient args')
                fileName = args[i+1]
            if arg == '-size':
                if len(args) < i + 2:
                    raise ValueError('insufficient args')
                chunkSize = int(args[i+1])
        
        assert(not fileName is None)
        assert(chunkSize != 0)
        assert(os.path.isfile(fileName))
    except (ValueError, AssertionError):
        import traceback
        traceback.print_exc()
        sys.exit(1)

    ## try to split large csv file into small parts
    try:
        fileHdl = open(fileName, 'r')
        firstLine = fileHdl.readline()
        cache = ""
        fileId = 1

        for i, line in enumerate(fileHdl, start=1):
            cache += line
            if i % chunkSize == 0:
                if len(cache) == 0:
                    continue
                tmpFile = open(fileName + '.part' + str(fileId), 'w')
                tmpFile.write(firstLine)
                tmpFile.write(cache)
                tmpFile.close()
                cache = ""
                fileId += 1
        fileHdl.close()

        ### handle the remaining shard that is smaller than chunkSize
        if len(cache) != 0:
            tmpFile = open(fileName + '.part' + str(fileId), 'w')
            tmpFile.write(firstLine)
            tmpFile.write(cache)
            tmpFile.close()
    except IOError:
        import traceback
        traceback.print_exc()
        sys.exit(1)
