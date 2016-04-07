def getBuffers(vimBuffers, vim):
    buffers = {}

    # todo svn status = vymyslet jak - asynchonne nacist?

    # cislovani bufferu oproti pismenum
    bufferLetterNumber = 1
    letters = {}
    letters = _getLetters()


    buffersCount = len(vimBuffers) + 2 # todo -> not all buffers are included, if only len is check

    _log (buffersCount.__str__() + ' pocet bufferu')

    for i in range(1, buffersCount):
        bufferData = {}

        # todo -> check that vimBuffers[i] realy exists
        try:
            #_log(vimBuffers[i].name)

            bufNumber = vimBuffers[i].number
        except:
            continue

        vim.command('let vim_buf_listed=getbufvar('+bufNumber.__str__()+', "&buflisted")')
        canBeListed = vim.eval('vim_buf_listed')

        vim.command('let vim_buf_modif=getbufvar('+bufNumber.__str__()+', "&modifiable")')
        canBeModifiable = vim.eval('vim_buf_modif')

        if (canBeListed.__str__() == '0' ):
            _log (bufNumber.__str__() + ' neni listed');
            continue

        if (canBeModifiable.__str__() == '0'):
            _log (bufNumber.__str__() + ' neni modifiable');
            continue

        bufName = vimBuffers[i].name

        #TODO  do it nicer - PROBABLY NOT NECESSARY - because of canBeListed and dcanBeModifiable
        if (bufName.rfind("-MiniBufExplorer-") > -1):
            continue
        if (bufName.rfind("ControlP") > -1):
            continue
        if (bufName.rfind('NERD_tree_') > -1):
            continue

        bufferData['number']        = bufNumber
        bufferData['path']          = bufName
        bufferData['pathParts']     = _parsePath(bufferData['path'])
        bufferData['letter']        = letters.get(bufferLetterNumber)
        bufferLetterNumber          = bufferLetterNumber + 1

        buffers[vimBuffers[i].number] = bufferData
    return buffers;

def prepareBuffersForGUI(buffers):
    print 'a'

def changeBufferCmdDialog(vim):

    vim.command('let vim_str=input("Go buffer: ")')
    newBufferString = vim.eval('vim_str')

    return newBufferString

#TODO support more buffers? - separated with space or something like that
def changeBuffer(vim, newBufferId, buffersData):

    newBufferId = newBufferId.strip()

    if (len(newBufferId) == 0):
        return 0

    if (newBufferId.isalpha()):
        for bufferNum in buffersData:
            if (newBufferId == buffersData[bufferNum].get('letter').__str__()):
                bufId = buffersData[bufferNum].get('number').__str__()
            
                #_log('prejit na' + bufId)
                #_log(newBufferId.__str__())
                vim.command('b ' + bufId)
                return 0

    else:
        if (newBufferId):
            #_log('prechazim na cislo')
            vim.command('b ' + newBufferId)
            return 0

    print "\n+++ Nothing found, try again" + "\n" 
    return 1

def printBuffersSortByFilename(buffersData):
    sortKeys = sorted(buffersData, key=lambda x: buffersData[x].get('pathParts').get('filename'))
    printBuffers(buffersData, sortKeys)

def printBuffersSortByDir(buffersData):
    sortKeys = sorted(buffersData, key=lambda x: buffersData[x].get('pathParts').get('fullpath'))
    printBuffers(buffersData, sortKeys)

def printBuffersSortByBufferNumber(buffersData):
    sortKeys = sorted(buffersData, key=lambda x: x)
    printBuffers(buffersData, sortKeys)

def printBuffersFilteredByString(vim, newBuffer, buffersData):
    newBuffer = newBuffer.lower()

    sortKeys = []

    for bufferNum in buffersData:
        if buffersData[bufferNum].get('pathParts').get('fullpath').lower().find(newBuffer) != -1:
            sortKeys.append(bufferNum)
        if buffersData[bufferNum].get('pathParts').get('filename').lower().find(newBuffer) != -1:
            sortKeys.append(bufferNum)

    sortKeys = list(set(sortKeys)) # get unique values
    printBuffers(buffersData, sortKeys)

def printBuffers(buffersData, sortKeys):
    print "\n"
    print  ('----- buffer list -------')
    print "\n"

    if (len(sortKeys) == 0):
        sortKeys = buffersData.keys()

    maxLenghts = _countWordLengths(buffersData);

    space      = '   '
    letter     = 'a'
    separator  = '/' #TODO - use function or constant
    
    for bufferNum in sortKeys:
        line = ''
        line += buffersData[bufferNum].get('letter').__str__()

        line += space
        line += _getFileNameAdjusted(buffersData[bufferNum].get('pathParts').get('filename'), maxLenghts['fileLength'])
        line += space

        pathData = buffersData[bufferNum].get('pathParts').get('path')

        pathData.reverse()

        for pp in pathData:
            line += pp + separator

        line += space
        line += buffersData[bufferNum].get('number').__str__()
        line += "\n"

        print line

def _getFileNameAdjusted(filename, maxLenght):
    fileString = '';
    space      = ' '

    fileL = len(filename)

    if (maxLenght - fileL) % 2 == 0:
        spacesCount = (maxLenght - fileL) #, TODO  / 2 for puting before and after word
    else:
        spacesCount = (maxLenght - fileL)

    return filename + space * spacesCount

def _countWordLengths(buffersData):
    fileLength = 0
    pathLength = 0

    for bufferNum in buffersData:
        fl = len(buffersData[bufferNum].get('pathParts').get('filename'))

        if fileLength < fl:
            fileLength = fl

        pathData = buffersData[bufferNum].get('pathParts').get('path')

        pl = 0
        for pp in pathData:
            pl += len(pp) + 1 # plus 1 for separators

        if pathLength < pl:
            pathLength = pl

    return {'fileLength': fileLength, 'pathLength': pathLength}
   
#assume, that the last part of path is filename
def _parsePath(path):
    pathParts = {}
    separator = '/' #TODO - use function

    pathParts['fullpath'] = path

    pathParts['separator']     = separator 

    path = path.split(separator)

    if len(path) > 0:
        pathParts['filename'] = path.pop(len(path)-1)
        fileParts = pathParts['filename'].split('.')

        pathParts['fileextension'] = ''

        if len(fileParts) > 2:
            pathParts['fileextension'] = fileParts[len(fileParts)-1]

    pathString = ''

    if len(path) > 0:
        pathStrings = []

        for pathPart in path:
            if len(pathPart) > 0:
                pathStrings.append(pathPart)

        pathParts['path'] = pathStrings
    else:
        pathParts['path'] = 'does not have path'

    return pathParts;

# Get letters: note: 65-90 A-Z  a 97-122 a-z
def _getLetters():

    #TODO better way
    letters = {}

    letters[1] = 'a';
    letters[2] = 'b';
    letters[3] = 'c';
    letters[4] = 'd';
    letters[5] = 'e';
    letters[6] = 'f';
    letters[7] = 'g';
    letters[8] = 'h';
    letters[9] = 'i';
    letters[10] = 'j';
    letters[11] = 'k';
    letters[12] = 'l';
    letters[13] = 'm';
    letters[14] = 'n';
    letters[15] = 'o';
    letters[16] = 'p';
    letters[17] = 'q';
    letters[18] = 'r';
    letters[19] = 's';
    letters[20] = 't';
    letters[21] = 'u';
    letters[22] = 'v';
    letters[23] = 'w';
    letters[24] = 'x';
    letters[25] = 'y';
    letters[26] = 'z';
    letters[27] = 'A';
    letters[28] = 'B';
    letters[29] = 'C';
    letters[30] = 'D';
    letters[31] = 'E';
    letters[32] = 'F';
    letters[33] = 'G';
    letters[34] = 'H';
    letters[35] = 'I';
    letters[36] = 'J';
    letters[37] = 'K';
    letters[38] = 'L';
    letters[39] = 'M';
    letters[41] = 'N';
    letters[42] = 'O';
    letters[43] = 'P';
    letters[44] = 'Q';
    letters[45] = 'R';
    letters[46] = 'S';
    letters[47] = 'T';
    letters[48] = 'U';
    letters[49] = 'V';
    letters[51] = 'W';
    letters[52] = 'X';
    letters[53] = 'Y';
    letters[54] = 'Z';

    return letters;

def _log(a):
    print a

