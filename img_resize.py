from PIL import Image
import os,sys,shutil,time
import destination

vendor = sys.argv[1] # specify vendor

sizes = [160,400,800]

#navigate directory relative to which PC is used
def goto_lastmod_dir():

    os.chdir(destination.imgdir+"/"+vendor) #go to dir

    all = [d for d in os.listdir(".") if os.path.isdir(d)]

    latest = max(all, key=os.path.getmtime) # get latest modified folder

    os.chdir(latest)
    return destination.imgdir+"/"+vendor+"/"+latest

def resize_w_ar(img,s):
    w,h = img.size
    if w > h:    
        wpercent = (s / float(img.size[0]))
        hsize = int(float(img.size[1]) * float(wpercent))
        img = img.resize((s,hsize))
    else:
        hpercent = (s / float(img.size[1]))
        wsize = int(float(img.size[0]) * float(hpercent))
        img = img.resize((wsize,s))
    return img
    
#make dirs for 3 sizes
# for s in sizes:
    # try:
        # os.makedirs(repr(s))
    # except:
        # shutil.rmtree(repr(s))
        # os.makedirs(repr(s))

path = goto_lastmod_dir()
images = [i for i in os.listdir(".") if os.path.isfile(i)]        
# print images
# print path

for s in sizes:
    for im in images:
        img = Image.open(im).convert("RGB")
        img = resize_w_ar(img,s)
        base,ext = os.path.splitext(im)
        while True:
            try:
				print path+"/{}/{}".format(s,base+".jpg")
				img.save(path+"/{}/{}".format(s,base+".jpg"))
				break
            except Exception as e:
                print e
                time.sleep(1)
                os.makedirs(repr(s))
                continue