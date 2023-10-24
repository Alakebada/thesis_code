import qd.cae.dyna as qd
import pandas as pd
import numpy as np
import os

def add_curve(path, lcid, a1, o1, title="", sidr=0, sfa=1, sfo=1, offa=0, offo=0, dattyp=0, lcint=0, headers=True):
        
    # Checks
    if not len(a1)==len(o1):
        print('Function expects a1 and o1 of same length')
        return
    
    # Initialize line counter
    line=1
    # Initializing keyword
    curve=qd.Keyword("*DEFINE_CURVE_TITLE")
    # Writing Keyword Definition
    #string="*DEFINE_CURVE_TITLE"
    #curve.insert_line(line,string)
    #line=line+1
    
    # Writing curve title
    curve.insert_line(line,title)
    line=line+1
    
    # Inserting headers, if headers=True
    if headers:
        string="$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint"
        curve.insert_line(line,string)
        line=line+1
    
    # Inserting variables
    string="{:10d}".format(lcid)+"{:10d}".format(sidr)+"{:10d}".format(sfa)+"{:10d}".format(sfo)+"{:10d}".format(offa)+"{:10d}".format(offo)+"{:10d}".format(dattyp)+"{:10d}".format(lcint)
    curve.insert_line(line,string)
    line=line+1
    
    # Inserting headers, if headers=True
    if headers:
        string="$#                a1                  o1"
        curve.insert_line(line,string)
        line=line+1
    
    # Inserting curve
    for i in range(len(a1)):
        string="{:20f}".format(a1[i])+"{:20f}".format(o1[i])
        curve.insert_line(line,string)
        line=line+1
    
    # Insert end keyword
    curve.insert_line(line,"*END")
    
    # Read file snd discrding last line
    tmp_file=open(path,'r').readlines()
    file=''
    for i in range(len(tmp_file)-1):
        file=file+tmp_file[i]
    file=file+str(curve)
    open(path,'w').write(file)
    return True

def edit_curve(path, lcid, title=True, sidr=True, sfa=True, sfo=True, offa=True, offo=True, dattyp=True, lcint=True, a1=True, o1=True):
    
    # Find position of curve with specified lcid
    source=open(path,'r')
    file=source.readlines()
    source.close()
    for pos in range(len(file)):
        if file[pos]=="*DEFINE_CURVE_TITLE\n":
            if file[pos+2][0]=="$":
                var=[float(var) for var in file[pos+3].split()]
                if var[0]==lcid:
                    headers=True
                    ln=pos
                    break
            else:
                var=[float(var) for var in file[pos+2].split()]
                if var[0]==lcid:
                    headers=False
                    ln=pos
                    break
    
    #Define keyword
    new_keyword=qd.Keyword("*DEFINE_CURVE_TITLE")
    line=1
    
    #Curve Title
    if isinstance(sidr,bool):
        title=file[ln+1][:-1]
    new_keyword.insert_line(line,title)
    line=line+1
    
    #Curve parameters
    if headers:
        string="$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint"
        new_keyword.insert_line(line,string)
        line=line+1
    if isinstance(sidr,bool):
        sidr=var[1]
    if isinstance(sfa,bool):
        sfa=var[2]
    if isinstance(sfo,bool):
        sfo=var[3]
    if isinstance(offa,bool):
        offa=var[4]
    if isinstance(offo,bool):
        offo=var[5]
    if isinstance(dattyp,bool):
        dattyp=var[6]
    if isinstance(lcint,bool):
        lcint=var[7]
    string="{:10.0f}".format(lcid)+"{:10.0f}".format(sidr)+"{:10.3f}".format(sfa)+"{:10.3f}".format(sfo)+"{:10.3f}".format(offa)+"{:10.3f}".format(offo)+"{:10.0f}".format(dattyp)+"{:10.0f}".format(lcint)
    new_keyword.insert_line(line,string)
    line=line+1
    
    #Curve
    if headers:
        string="$#                a1                  o1"
        new_keyword.insert_line(line,string)
        line=line+1
    
    if isinstance(a1,bool):
        if headers:
            ln=ln+5
        else:
            ln=ln+3
        while file[ln][0]!='*':
            string=file[ln][:-1]
            new_keyword.insert_line(line,string)
            line=line+1
            ln=ln+1
    else:
        for i in range(len(a1)):
            string="{:20f}".format(a1[i])+"{:20f}".format(o1[i])
            new_keyword.insert_line(line,string)
            line=line+1
    
    #Write to file
    tmp_file=''
    for i in range(pos):
        tmp_file=tmp_file+file[i]
    tmp_file=tmp_file+str(new_keyword)
    pos=pos+1
    for i in range(len(file)):
        if file[pos+i][0]=='*':
            break
    pos=pos+i
    for i in range(len(file)-pos):
        tmp_file=tmp_file+file[pos+i]
    dst=open(path,'w')
    dst.write(tmp_file)
    dst.close()
    
    return
# Test add_curve function
if __name__ == '__main__':
    path=os.path.join(os.getcwd(),'02_Material.k')
    lcid=1
    title='Tryout'
    a1=np.linspace(0,10,10)
    o1=np.linspace(10,20,10)
    add_curve(path,lcid,a1,o1,title=title)