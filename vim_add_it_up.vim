python import sys

python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

function! PavelBuffers()
python << endOfPython

from pavel_buffers import *

# TODO  vim.buffers is not updated - for example if the new file is created, it is not loaded in vim.buffers
buffersData = getBuffers(vim.buffers, vim)
printBuffers(buffersData, [])

# allow open one found file imediately, after filtering by string result contains only one file
allowOneMatchChange = True

x = True

while (x):
    newBuffer = changeBufferCmdDialog(vim)

    # TODO better way ,fd ,df  ,f - file name,d - dir path ,b - buffer number ,e - last edit ,o - last open
    # jak na to -> cykluju pres buffer data, vyberu pozadovanou vec ( v pripade  e a o -> to je nekde jinde ulozeny), 
    #  a pak seradim nove vybrany veci (mam jejich id v buffersdata), a znovu projizdim buffersdata podle toho serazenyho id

    # TODO - add sorting by  lenght of filename

    # TODO -> kdyz zadam F -> tak to pri psani filtruje/vyhledava (nebo namapovat na neco jinyho nez PBuf
    # TODO -> barvy pri vyhledavani??
    if (newBuffer.__str__() == 'sortf'):
        printBuffersSortByFilename(buffersData)
    elif (newBuffer.__str__() == 'sortd' or newBuffer.__str__() == 'sortp'):
        printBuffersSortByDir(buffersData)
    elif (newBuffer.__str__() == 'sortb'):
        #tohle by mohlo resit last open??
        printBuffersSortByBufferNumber(buffersData)
    else:
        result = changeBuffer(vim, newBuffer, buffersData)

        if (result == 0):
            x = False
        else:
            # Nothing was found, try to search the input string in buffers data
            result = printBuffersFilteredByString(vim, newBuffer, buffersData, allowOneMatchChange)

            #todo - tfuj - nejak hezcejc
            if (result == 0):
                x = False
            else:
                print "\n+++ Nothing found, try again" + "\n" 


#help(vim.eval)

#TODO GUI
#buffersForGUI = prepareBuffersForGUI(buffersData)

endOfPython
endfunction

command! Pbuf call PavelBuffers()
