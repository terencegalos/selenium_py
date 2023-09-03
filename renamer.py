import shutil,os,sys

def main(txt,src,dest):
    
    os.chdir(src) #go to 
    # print os.getcwd()

    infile = open(txt,mode="rb")
    content = infile.readlines()
    # print os.listdir(".")
    for x in range(2,len(content)):
        line = "".join(content[x].split("\x00")).strip('\r\n')
        # line = content[x].split()

        # os.chdir("\\".join(line.split("\\")[:-1])+"\\")
        print "\\".join(line.split("\\")[:-1])+"\\".replace("\\","/")
        # print line
        # print dest+line.split("\\")[-1]
        # shutil.copyfile(line,dest+line.split("\\")[-1])



if __name__ == "__main__":
    s,t,d = sys.argv[1:]
    main(s,t,d)