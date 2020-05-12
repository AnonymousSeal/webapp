def comment(text, logfile='log.txt'):
    f = open(logfile,'a')
    f.write(str(text) + '\n')
    f.close()
