class Quit(Exception):                                                          #CUSTOM ERROR CLASS TO QUIT THREADS
    pass


def get_update_file():                                                          #RETURNS NAME OF UPDATE FILE
    return 'update.txt'


def get_quit_file():                                                            #RETURNS NAME OF QUIT FILE
    return 'quit.txt'


def set_update(text):                                                           #SETS THE TEXT IN THE UPDATE FILE
    check_quit()
    file = open(get_update_file(), 'w')
    file.write(text)                                                            #OVERWRITES THE FILE
    file.close()


def get_update():                                                               #RETURNS TEXT IN UPDATE FILE
    file = open(get_update_file(), 'r')
    text = file.read().replace('\n','')                                         #READ FILE AND RETURN CONTENTS
    file.close()
    return text
 

def set_quitting(quitting):                                                     #SETS THE TEXT IN THE QUIT FILE
    file = open(get_quit_file(), 'w')
    if quitting : file.write('q')                                               #IF QUITTING THEN 'q'
    else : file.write('')                                                       #IF NOT QUITTING THEN EMPTY
    file.close()


def check_quit():                                                               #CHECKS IF PROCESS SHOULD BE QUIT
    status = open(get_quit_file()).read()
    if status == 'q' : raise Quit                                               #RAISE QUIT ERROR IF QUITTING
