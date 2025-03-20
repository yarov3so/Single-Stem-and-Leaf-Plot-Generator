#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import steamlit as st

st.title("Stem and Leaf Plot Generator ")

def comprehend(mystring):
    
    mystring=mystring.replace(" ", "")
    data_list=mystring.split(",")
    data =[]
    for el in data_list:
        try:
            data.append(float(el))
        except: 
            for i in range(int(re.findall(r'\d+', el)[0])):
                data.append(None)
    return data

def magnitude(num):
    
    num=str(num)
    if num[0]!="0":
        if "." in num:
            return num.find(".") - 1
        else:
            return len(num) -1 
    else:
        num=num[2:]
        for i in range(len(num)):
            if num[i]!="0":
                return -i-1 
        return 0

def add_zeros(numstr,numchar):

    while len(numstr[:numstr.index(".")])<numchar:
        numstr="0"+numstr
    return numstr
    
def stempos(numlist):
    
    magnitudes=[magnitude(num) for num in numlist]

   # if all(mag==magnitudes[0] for mag in magnitudes)==False:
   #     raise ValueError("The values in your data set must have similar scale!")

    #mag=magnitudes[0]
    mag=max(magnitudes)


    if mag>=0:
        stemposition=mag
        maxlen_whole=max([len(str(num)[0:str(num).index(".")]) for num in numlist])
        #numlist=[str(num).replace(".","") for num in numlist]
        #maxlen=max([len(num) for num in numlist])
        
        #numlist=[num for num in numlist if len(num)==maxlen] # to be changed 
        numlist=[str(num).replace(".","") for num in numlist if len(str(num)[0:str(num).index(".")])==maxlen_whole]
        
        try:
            all((num[0]==numlist[0][0] for num in numlist))
        except:
            return stemposition
            
        while all((num[0]==numlist[0][0] for num in numlist)):
            stemposition-=1
            numlist=[num[1:] for num in numlist]
            try:
                all((num[0]==numlist[0][0] for num in numlist))
            except:
                return stemposition
    else:
        
        stemposition=mag
        numlist=[str(num).replace(".","")[-mag:] for num in numlist]

        try:
            all((num[0]==numlist[0][0] for num in numlist))
        except:
            return stemposition
        
        while all((num[0]==numlist[0][0] for num in numlist)):
            
            stemposition-=1
            numlist=[num[1:] for num in numlist]

            try:
                all((num[0]==numlist[0][0] for num in numlist))
            except:
                return stemposition
                
    return stemposition

def sl_range(numlist,pos):
    
    digits=[]
    for num in numlist:
        try:
            digits.append(int(str(num)[pos]))
        except:
            digits.append(0)

    return [i for i in range(min(digits),max(digits)+1)]

def try_int(num):
    
    num_int=None
    try:
        num_int=int(num)
    except:
        None
    if num==num_int:
        return num_int
    else:
        return float(num)

def pos_rep(pos):

    if pos==0:
        return "unit"

    if pos>0:
        return "1"+"0"*pos

    if pos<0:
        return "0."+"0"*(-pos-1)+"1"

def truncate(num,pos):

    num=float(num)
        
    if pos >= 0:
        try:
            return int(str(num)[:str(num).index(".")-pos-1]) #str(num)
        except:
            return 0

    if pos ==-1:
        return int(str(num)[:str(num).index(".")-pos-1])

    if pos < -1:
        return float(str(num)[:str(num).index(".")-pos])
        

def stemandleaf():

    st.markdown("*by yarov3so*")
    st.text("Generates a compact and a full stem and leaf plot for a (reasonably well-behaved) set of values.")

    print("\nStem and Leaf Plot Generator by yarov3so\n")
    data=st.text_input("Enter all the values from the data set, separated by commas: ")

    if data="":
        st.stop()
    
    data=comprehend(data)
    stem_pos=stempos(data)

    ml=max([len(str(num)[:str(num).index(".")]) for num in data])

    data_ml=data[0]
    for i in range(len(data)):
        if len(str(data[i])[:str(data[i]).index(".")]) == ml:
            data_ml=data[i]

    st.text("\nYou have entered:")
    st.code(f"\n{[try_int(num) for num in data]}")

    st.text(f"\nThe stem and leaf plot will represent variation in your data set at the {pos_rep(stem_pos)}s position and lower, since, at each higher magnitude position, every data value has the same digit.")
    st.text(f"Indeed, truncating each value in your data set right before the {pos_rep(stem_pos)}s position results in a data set with identical values (and possibly zeros when truncation eats up the entire number):\n")
    st.code([truncate(num,stem_pos) for num in data])

    if len(set([truncate(num,stem_pos) for num in data])-{0})>=2:
        st.text("ERROR: The data set has inconsistent spread or sharp jumps in magnitude - did you forget to exclude outliers? This can happen if removing one or more data points drastically (by orders of magnitude) reduces the overall spread of your data set.")
        return "ERROR: The data set has inconsistent spread or sharp jumps in magnitude - did you forget to exclude outliers? This can happen if removing one or more data points drastically (by orders of magnitude) reduces the overall spread of your data set."
                          
    #print("\nNOTE: If above list has more several distinct non-zero values, then the stem-and-leaf plots below will be incorrect! This can happen if you forgot to exclude outliers from your data set.")
    
    if stem_pos==0:
        st.text(f"\nAs such, to reconstruct the data values from the compact stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left) with any stem-leaf combination (on the right). Remember to add a dot (decimal point) betweem stems and leaves!")
    elif stem_pos==-1:
        st.text(f"\nAs such, to reconstruct the data values from the compact stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left), \'.\' (decimal point) and any stem-leaf combination (on the right).")
    else:
        st.text(f"\nAs such, to reconstruct the data values from the compact stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left) with any stem-leaf combination (on the right), except when the number is preceded by an apostrophe ('). In the latter case, the leaf itself is the original number.")

    if stem_pos>=0:
        stem_pos_py=ml - stem_pos-1
    else:
        stem_pos_py=str(data_ml).index(".") - stem_pos
    
    st.markdown(" #### Compact Stem and Leaf Plot:")

    stems=sl_range([add_zeros(str(num),ml) for num in data],stem_pos_py)

    if (any([len(str(num)[:str(num).index(".")])!=ml for num in data])==True) and (0 not in stems):
        stems.append(0)
        stems=sorted(stems)
        
    output=""
    
    for stem in stems:

        leaves=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves)):
            if leaves[i]=="":
                leaves[i]=0

        leaves=sorted([try_int(float(leaf)) for leaf in leaves])
        leaves=[str(leaf) for leaf in leaves]
        
        if len(leaves)!=0:
            maxlenleaves=max([len(leaf) for leaf in leaves])
            for i in range(len(leaves)):
                if leaves[i]=="0":
                    while len(leaves[i]) < maxlenleaves:
                        leaves[i]=leaves[i] + "0"
                else:
                    while len(leaves[i]) < maxlenleaves:
                        leaves[i]="0"+leaves[i]

        if stem==0:
            smallerleaves=[add_zeros(str(num),ml)[stem_pos_py:] for num in data if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            if len(smallerleaves)!=0:
                for i in range(len(smallerleaves)):
                    if smallerleaves[i]=="":
                        smallerleaves[i]=0
                smallerleaves=sorted([try_int(float(leaf)) for leaf in smallerleaves])
                smallerleaves=["'"+str(leaf) for leaf in smallerleaves]
                #maxlensmleaves=max([len(leaf) for leaf in smallerleaves])
                # for i in range(len(smallerleaves)):
                #     while len(smallerleaves[i]) < maxlensmleaves:
                #         smallerleaves[i]=smallerleaves[i] + "0"
                leaves=smallerleaves+leaves[:]
        
        leaves_pretty=" "    

        for leaf in leaves:
            if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                leaves_pretty+=str(leaf)[1:]+"  "
            elif stem_pos==0 and leaf==0:
                leaves_pretty+=".0  "
            else:
                leaves_pretty+=str(leaf)+"  "

        output+="   "+stem+"  | "+leaves_pretty+"\n\n"
        
    st.code(f"```\n{output}```",language="")

    st.text("\nIn the full stem and leaf plot below, the 'L' row, if present, contains data values of magnitudes lower than the ones represented on the remainder of the plot. Their stem L does not contribute any digits, so their original values are precisely their leaf values.")
    
    st.markdown("#### Full Stem and Leaf Plot:")

    stems=sl_range([add_zeros(str(num),ml) for num in data],stem_pos_py)
    

    if (any([len(str(num)[:str(num).index(".")])!=ml for num in data])==True) and (0 not in stems):
        stems.append(0)
        stems=sorted(stems)

    output=""
    
    for stem in stems:

        leaves=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves)):
            if leaves[i]=="":
                leaves[i]=0


        leaves=sorted([try_int(float(leaf)) for leaf in leaves])
        leaves=[str(leaf) for leaf in leaves]
        
        if len(leaves)!=0:
            maxlenleaves=max([len(leaf) for leaf in leaves])
            for i in range(len(leaves)):
                if leaves[i]=="0":
                    while len(leaves[i]) < maxlenleaves:
                        leaves[i]=leaves[i] + "0"
                else:
                    while len(leaves[i]) < maxlenleaves:
                        leaves[i]="0"+leaves[i]
        
        if stem==0:
            smallerleaves=[add_zeros(str(num),ml)[stem_pos_py:] for num in data if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            if len(smallerleaves)!=0:
                for i in range(len(smallerleaves)):
                    if smallerleaves[i]=="":
                        smallerleaves[i]=0
                smallerleaves=sorted([try_int(float(leaf)) for leaf in smallerleaves])
                smallerleaves=[str(leaf) for leaf in smallerleaves]
                # maxlensmleaves=max([len(leaf) for leaf in smallerleaves])
                # for i in range(len(smallerleaves)):
                #     while len(smallerleaves[i]) < maxlensmleaves:
                #         smallerleaves[i]=smallerleaves[i] + "0"
                        
                smallerleaves_copy=[str(leaf) for leaf in smallerleaves]
                smallerleaves=["'"+str(leaf) for leaf in smallerleaves]
                
                #leaves=smallerleaves+leaves[:]

                smallerleaves_pretty=" "
                for leaf in smallerleaves_copy:
                    if stem_pos==0 and leaf!="0" :
                        smallerleaves_pretty+=str(leaf)[0:]+"  " #0 or 1
                    elif stem_pos==0 and leaf=="0":
                        smallerleaves_pretty+=".0  "
                    else:
                        smallerleaves_pretty+=str(leaf)+"  "

                if stem_pos==-1:
                    fullstem=str(truncate(data_ml,stem_pos))+"."+str(stem)
                elif truncate(data_ml,stem_pos)!=0:
                    fullstem=str(truncate(data_ml,stem_pos))+str(stem)
                else:
                    fullstem=str(stem)

                Lpad=len(fullstem)

                output+="  "+" L"+" "*(Lpad-1)+"  |"+smallerleaves_pretty+"\n\n"
                    
        
        leaves_pretty=" "    
        
        if stem_pos==-1:
            stem=str(truncate(data_ml,stem_pos))+"."+str(stem)
        elif truncate(data_ml,stem_pos)!=0:
            stem=str(truncate(data_ml,stem_pos))+str(stem)
            
        
        for leaf in leaves:
            if stem_pos==0 and leaf!="0" :
                leaves_pretty+=str(leaf)[1:]+"  "
            elif stem_pos==0 and leaf==0:
                leaves_pretty+=".0  "
            else:
                leaves_pretty+=str(leaf)+"  "
        
        output+="   "+stem"  | "+leaves_pretty+"\n\n"
        
    st.code(f"```\n{output}```",language="")

stemandleaf()
