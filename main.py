from BandDataBase import bands
from bisect import bisect_left, insort
from distutils.file_util import move_file
from os import mkdir, listdir, rename
from os.path import isdir 
from os.path import splitext as get_file_extension


################################################################################

def __addNewBand__(biglist):
    '''Returns a list("biglist") with bands to add in 'BandDataBase.py'.'''
    name = input("Enter the name of the artist or the band: ")
    ans = input('Is it "'+name+'"?   Yes/No/Cancel\n=> ')
    ans = ans.casefold()
    if ans=='no' or ans=='n':
        return __addNewBand__(biglist)
    elif ans=='cancel' or ans=='c':
        return biglist
    print('\n',name,'!!!',sep='')
    ans = input('Is it "The '+name+'" or not?    Yes/No/Cancel\n=> ')
    ans = ans.casefold()
    dir = name
    if ans=='yes'or ans=='y':
        dir = 'The ' + dir     
    elif ans=='cancel' or ans=='c':
        return biglist
    if '/' in dir:
        dir = dir.replace('/', '_')
    print('#', dir, "'s songs will be placed in a folder called '",
          dir, "'.", sep='', end='\n\n')
    if "'" in dir:
        dir = dir.replace("'", "\\'")
    if "'" in name:
        name = name.replace("'", "\\'")
    temp = [name]
    ans = input("""\
Please add words to associate with the artist or the band:
e.g.  RHCP = Red Hot Chili Peppers or GNR = Guns & Roses
Leave it empty and press enter when you finish.
=> """)
    while 1:
        if "'" in ans:
            ans = ans.replace("'", "\\'")
        elif "\\" in ans:
            ans = ans.replace("\\", "\\\\")
        if ans!='': temp.append(ans)
        else: break
        ans = input('=> ')
    print(temp)
    ans = input('Add '+name+' to the database?    Yes/No/Cancel\n=> ')
    ans = ans.casefold()
    if ans=='yes'or ans=='y':
        for i in temp:
            biglist.append((i.casefold(),dir))
        print("#'",dir,"' will be added to the database.\n",sep='')
    elif ans=='cancel' or ans=='c':
        return []
    else:
        print("#'",dir,"' will not be added to the database.\n",sep='')
    ans = input("Do you want to add an other performer? (Yes/No)\n=> ").casefold()
    if ans=='yes'or ans=='y':
        return __addNewBand__(biglist)
    print(biglist)
    return biglist

def __cleanUpMess(biglist):
    '''Adds the bands from "biglist" in 'BandDataBase.py'.'''
    if biglist==[]:
        return
    bands.extend(biglist)
    bands.sort()
    file = open('BandDataBase.py')
    list = file.readlines()[1:-1]
    for i in biglist:
        text = "', '".join(i)
        text = ''.join(('    (',"'",text,"'",'),\n'))
        insort(list,text)
    list[-1].replace('\n',',\n')
    file = open('BandDataBase.py', 'w')
    file.write('bands = [\n')
    file.writelines(list)
    file.write('    ]\n')
    file.close()
    input('#Database has been updated.')
    
def __deleteEntry__():
    ans = input('Type the number of the entry that you wish to delete or cancel.\n=> ')
    if ans.casefold() in ('c', 'cancel'):
        return
    try:
        key = int(ans)-1
        print('You are about to delete:',bands[key])
        ans = input('Yes/No/Cancel: ').casefold()
    except:
        print('#Invalid value.')
        return __deleteEntry__()
    if ans=='y' or ans=='yes':
        file = open('BandDataBase.py')
        list = file.readlines()[1:-1]
        list[-1].replace('\n',',\n')
        del bands[key]
        del list[key]
        file = open('BandDataBase.py', 'w')
        file.write('bands = [\n')
        file.writelines(list)
        file.write('    ]\n')
        input('#Database has been updated.')
    elif ans=='c' or ans=='cancel': return 
    else:
        for i, j in enumerate(bands):
            print(i+1,'. ',j,sep='')
        __deleteEntry__()
        
################################################################################

################################################################################       

def __savePathsInFile__(tobeused, pathOut):
    if pathOut==None: pathOut = 'None\n'
    else: pathOut = ''.join(("'",pathOut,"'",'\n'))
    tobesaved = []
    print()
    for i in enumerate(tobeused):
        print(i[0]+1,i[1],sep='. ')
    print("""\
Pick the numbers of the paths that you wish to save for later use.
~Leave the line empty and press enter when you finish selecting paths.\n""")
    while 1:
        ans = input('=> ')
        if ans=='': break
        else:
            try:
                if tobeused[int(ans)-1] in tobesaved:
                    print('#Path already added.')
                else:
                    tobesaved.append(tobeused[int(ans)-1])
            except: print('#Invalid value.')
    file = open('SavedPaths.py')
    list = file.readlines()[2:-1]
    for i in tobesaved:
        i=i.replace('\\','\\\\')
        list.append(''.join(("    '",i,"',\n")))
    file = open('SavedPaths.py','w')
    file.write('pathOut = '+pathOut)
    file.write('pathsIn = [\n')
    for i in list:
        file.write(i)
    file.write('    ]\n')
               
def __SavedPathsProcesser__():
    '''Returns the paths where the music files to be sorted are.'''
    from SavedPaths import pathOut, pathsIn
    tobeused=[]
    if pathsIn==[]:
        print("""\
Please add the path(s) of the folder where the music files you want to sort are.
~You can add multiple folders.
~Leave the line empty and press enter when you're done adding folders.\n""")
        while 1:
            ans = input('=> ')
            if 1-isdir(ans) and ans!='':
                print('#Invalid path.')
                continue
            if ans=='':
                if tobeused!=[]: break
            else:
                tobeused.append(ans)   
    else:
        print("Saved paths of folders with music:")
        for i in enumerate(pathsIn):
            print(i[0]+1,i[1],sep='. ')
        print("""\
Pick the numbers of the paths that you want to use.
~Leave the line empty and press enter when you finish selecting paths.\n""")
        while 1:
            ans = input('=> ')
            if ans=='': break
            else:
                try:
                    tobeused.append(pathsIn[int(ans)-1])
                except:
                    print('#Invalid input.')
    while 1:
        print('\nPaths to be used:')
        for i in enumerate(tobeused):
            print(i[0]+1,i[1],sep='. ')
        print('\nMENU: \
1.Remove a path.    2.Add a new path.    3.Cancel\nPress ENTER to continue.')
        ans = input('=> ')
        while ans not in ('1','2','3',''):
            ans = input('#Invalid input.\n=> ')
        if ans=='1':
            ans = input('Which path do you wish to remove?\n=> ')
            try: del tobeused[int(ans)-1]
            except: print('#Invalid value.')
        elif ans=='2':
            ans = input('Add path: ')
            if 1-isdir(ans):
                print('#Invalid path.')
            tobeused.append(ans)
        elif ans=='3':
            return []
        elif ans=='':
            print('Paths that are going to be used:\n',tobeused)
            break
    if pathOut!=None:
        print('\
Do you want to save the sorted music files in', pathOut, '?   Yes/No\n')
        ans = None
        while ans not in ('y','yes','n','no'):
            ans = input('=> ').casefold()
    temp = None
    if pathOut==None or ans=='n' or ans=='no':
        while 1:
            print("""
Add path where the sorted music files should be saved or leave it blank in order
for the sorted files to be saved in their current directories.""")
            pathOut = input('=> ')
            if 1-isdir(pathOut) and pathOut!='':
                print('#Invalid path.')
                continue
            if pathOut!='':
                ans = input('Should the sorted files be saved in '+pathOut+'?    Yes/No\n=> ').casefold()
            else:
                ans = input('Should the sorted files be saved in their current folders?    Yes/No\n=> ').casefold()
            if ans=='y' or ans=='yes': break
    #if pathOut!='':
    #    if pathOut[-1]!='\\': pathOut = ''.join((pathOut,'\\'))
    #    ans = input('Do you want to save this path for later use?   Yes/No\n=> ').casefold()
    #    if ans=='y' or ans=='y':
    #        temp = pathOut
    #__savePathsInFile__(tobeused, temp)
    return tobeused, pathOut

################################################################################

################################################################################

def __isItMusic__(z):
    y, x = get_file_extension(z)
    if 'cover' in y.casefold(): return 0
    if '.mp3'==x: return 1
    elif '.mp4'==x: return 1
    elif '.wav'==x: return 1
    return 0

def __find__(name, l):
    list = name.split()
    for i in list:
        key = bisect_left(l, i)
        try:
            end = ord(bands[key][0][0])+1
            while end > ord(bands[key][0][0]):
                if bands[key][0] in name:
                    return bands[key][1]
                else:
                    key+=1
        except IndexError:
            pass
                    
def sortSongs(path,pathOut):
    try:
        filesInFolder = listdir(path)
        print(path,end='\n..............................................   ') 
    except FileNotFoundError:
        print('#Invalid path.')
    l = [i[0] for i in bands]
    musicFiles = filter(__isItMusic__, filesInFolder)
    for file in musicFiles:
        t = get_file_extension(file)
        try:
            dir = pathOut + __find__(t[0].casefold(), l)
        except TypeError:
            continue
        if 1 - isdir(dir):
            mkdir(dir)
        else:
            cont2 = listdir(dir)
            cont = [i.casefold() for i in cont2]
            c = 0
            newfile = file
            while newfile in cont:
                c += 1
                newfile = t[0]+str(c)+t[1]
            if c:
                rename(pathOut+file, pathOut+newfile)
                file = newfile
        move_file(pathOut+file, dir)
    print('  Done!')
    input()
        
################################################################################



def __main__():
    version="0.0.2.6"
    about = """
This programme arranges your music according to the artist or the band who
performed each song. If a performer is not found in the database, you can
add it.

    MENU:
    1. Sort Songs!
    2. See and edit database.
    3. Help/About.
    4. Quit.   :'(
"""
    ans = input(about+'\n=> ')
    while 1:
        if ans=='1':
            l = __SavedPathsProcesser__()
            if l==[]: return __main__()
            pathOut = l[1]                  
            pathsIn = l[0]
            print()
            if pathOut=='':
                for path in pathsIn:
                    if path[-1]!='\\': path = ''.join((path,'\\'))
                    sortSongs(path,path)             
            else:
                if pathOut[-1]!='\\': pathOut = ''.join((pathOut,'\\'))
                for path in pathsIn:
                    if path[-1]!='\\': path = ''.join((path,'\\'))
                    sortSongs(path,pathOut)
            print(about)
        elif ans=='2':
            while 1:
                print('FileNo. (Keyword, Folder)')
                for i, j in enumerate(bands):
                    print(i+1,'. ', j, sep='')
                print('\nMENU: \
1.Remove an entry.    2.Add a performer in the database.    3.Go back.')
                ans=input('=> ')
                while ans not in ('1','2','3'):
                    ans = input('#Choose 1, 2 or 3.\n=> ')
                if ans=='1': __deleteEntry__()
                elif ans=='2':
                    __cleanUpMess(__addNewBand__([]))
                    #import BandDataBase
                    #bands = BandDataBase.bands
                elif ans=='3': break
            print(about)
        elif ans=='3':
            print(about)
        elif ans=='4':
            print("#Thanks for using me.(in a good way) \n#Bye!\n")
            print("        Version",version)
            input("=> ")
            print("""\
$|There are still some bugs to be fixed|$
$|and some new feutures to be added.   |$
$|                              Steve  |$""")
            break
        else: print("Invalid input.")
        ans = input("=> ")


        
if __name__=="__main__":
    __main__()
    pass
