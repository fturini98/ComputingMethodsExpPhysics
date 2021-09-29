import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import timeit

start=timeit.timeit()#start for calculating the total enlapsed time


##############define parser###################

parser=argparse.ArgumentParser(description="Return the relative Frequencies of the letters in the input flie") 
parser.add_argument("file_path", type=str, help="the path of imput file")
parser.add_argument("letter",type=str,help="the letter that you want to count")
parser.add_argument("-i","--histo",action="store_true", help="Show the istogram of the relative frequencies of all letters")
parser.add_argument("-k","--KeyInSensitive", action="store_true", help="Deactivate the key sensitive mode")
parser.add_argument("-t","--TimeEnlapsed",action="store_true", help="Show the total enlapsed time of the program")
parser.add_argument("-v", "--verbosity", action="count",help="increase output verbosity")


args=parser.parse_args()


####################open file##########################
linux_path=os.path.normcase(args.file_path) #convert the path in the correct form for the "open file" function

file_in=open(linux_path,"r")

lines=file_in.readlines()




####################first dictionary with all letter##################
all_freq={}

for line in lines:
    
    for vocab_letter in line:
        
    #########controll if the charater is a letter  using ASCII code############
        if ord(vocab_letter) >= 65 and ord(vocab_letter) <= 90:
            letter_control=True
        elif ord(vocab_letter) >= 97 and ord(vocab_letter) <= 122:
            letter_control=True
        else:
            letter_control=False
    #####################add the letter to dictionary##########  
        
        if letter_control:
            if vocab_letter in all_freq:
                all_freq[vocab_letter] +=1
            else:
                all_freq[vocab_letter] =1
        
   
        
##########################Key Insensitive option######################
if args.KeyInSensitive:
    
    all_freq_insensitive={}
    
    for vocab_letter in all_freq.keys():
        
        
        if vocab_letter.upper() in all_freq_insensitive:
            all_freq_insensitive[vocab_letter.upper()] +=all_freq[vocab_letter]
        else:
            all_freq_insensitive[vocab_letter.upper()] = all_freq[vocab_letter]
    final_voc=all_freq_insensitive 
    
    
    if args.letter.upper() in final_voc:#take the value of occurences of the searched letter
        letter_count=final_voc[args.letter.upper()]  
    else:
        letter_count=0.
    
else:
    final_voc=all_freq 
    if args.letter in final_voc:#take the value of occurences of the searched letter
        letter_count=final_voc[args.letter]  
    else:
        letter_count=0.
#####################count of all letters##########################
values=final_voc.values()

letter_count=float(letter_count)
n_letters=sum(values)

##################covertion of type for rescaling in order to obtain frequences############
values=list(values) #change from dict_value to list of int
values=[float(val) for val in values]#change list of int in a list of float
freq=np.divide(values,n_letters)#dividing a list for a int



#######################Output with Verbosity####################


if args.verbosity >=2:
    print(f"The relative frequence of {args.letter} is {letter_count/n_letters} and it was found in the text {letter_count} times over {n_letters} letters")
elif args.verbosity >=1:
    print(f"letter:{args.letter} frequence: {letter_count/n_letters}")
else:
    print(f"{letter_count/n_letters}")


###################option for plotting histogram################    
if args.histo:
    width=1.0
    plt.bar(final_voc.keys(),freq, width, color='g')
    plt.xlabel("Letter")
    plt.ylabel("Relative Frequences")
    plt.title("Letter frequences on the text")
    plt.show()

#########################Enlapsed Time###########################
stop=timeit.timeit()

if args.TimeEnlapsed:
    Enlapsed_Time=stop-start
    if args.verbosity >=2:
        print(f"The time of program is {Enlapsed_Time} seconds")
    elif args.verbosity >=1:
        print(f"time:{Enlapsed_Time} [s]")
    else:
        print(f"{Enlapsed_Time}")