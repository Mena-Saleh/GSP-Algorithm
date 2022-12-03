import pandas as pd


#Data is static for now, because it is hard to find sequential datasets
Data = { 
        'Sequence ID': [1,2,3,4,5],
        
         'Sequence': ['AB(FG)CD',
                      'BGD',
                      'BFG(AB)',
                      'F(AB)CD',
                      'A(BC)GF(DE)'
                     ]
        }



#Create dataframe
df = pd.DataFrame(Data);

#print (df)

#To loop over all sequences in the df:
#for i in df.index:
#    print (df.iloc[i].Sequence)
    

#Min support static for now, we can make it a variable later
MinSupport = 2

#Dictionary to store calculated support of sequences as we go (used for pruning)
#Entry example: '<AB(CD)>' : 3 , which means that sequence has a support of three
SequencesSupport = {}

#List that contains frequent sequences, Ex: 'A' or  
FrequentSequences = []




#takes a sequence and splits it into a list a of elements, EX AB(CD)E ==> [A,B,(CD),E]
def splitSequence(Sequence):
    #Split the SubSequence into individual elements (temporal in mind)
    TempElement = ""
    SequenceSplit = []
    i = 0
    while i < len(Sequence):
        TempElement = ""
        if (Sequence[i] != '('):
            SequenceSplit.append(Sequence[i])
        else:
            for j in range (i,len(Sequence)):
                if(Sequence[j] == ')'):
                    TempElement += Sequence[j]
                    i = j
                    break
                else:
                    TempElement += Sequence[j]   
            SequenceSplit.append(TempElement)
        i = i + 1

    return SequenceSplit



#Function that checks if SubSequence is a sub sequence of SuperSequence, and returns true if so
def isSubSequence(SubSequence, SuperSequence):
    
    SubSequenceSplit = splitSequence(SubSequence)
    SuperSequenceSplit = splitSequence(SuperSequence)
    

    
    Flag = True
    TemporalSplit = []
    
    for i in SubSequenceSplit:
        #If temporal element, Ex ==> (AB), first split it in to A , B and then look for them 
        if (i[0] == '('):
            TemporalSplit = [*i[1: len(i) -1]] #Split by items inside the ()
            TemporalFlag = False
            for j in SuperSequenceSplit:
                if(j[0] == '('):
                    TemporalFlag = True
                    for k in TemporalSplit:
                        if(k in j):
                            j.replace(k, '')
                        else:
                            TemporalFlag = False
                            break
                    if(TemporalFlag):
                        break
            if (not TemporalFlag):
                Flag = False
                break
                
         
                        
                        
                        
        else:   #non temporal emlement, check if it exists in the super sequence, if not then check if it exists in the temporal elements of the super sequence
            if (i in SuperSequenceSplit):
                SuperSequenceSplit = SuperSequenceSplit[SuperSequenceSplit.index(i) + 1: len(SuperSequenceSplit)]
                
            else:
                TemporalFlag2 = False
                for j in SuperSequenceSplit:
                    if(j[0] == '('):
                        TemporalFlag2 = True
                        if(i in j):
                            SuperSequenceSplit = SuperSequenceSplit[SuperSequenceSplit.index(j) + 1: len(SuperSequenceSplit)]
                            break
                        else:
                            TemporalFlag2 = False
                    if (TemporalFlag2):
                        break                    
                if (not TemporalFlag2):
                    return False
     
         

    return Flag
    
    


def calculateSupport(SubSequence):
    Support = 0
    for i in df.index:
        if (isSubSequence(SubSequence, df.iloc[i].Sequence)):
            Support = Support + 1

    return Support



#Generate one item candidates based on support, also register them in the Support dictionary and FrequentSequences
def generateOneItemCandidateSequences():
    
    SetOfCandidates = set()
    for i in df.index:
        for j in df.iloc[i].Sequence:
            if(j != "(" and j != ")"):
                SetOfCandidates.add(j)
                
    for i in SetOfCandidates:
        Support = calculateSupport(i)
        SequencesSupport[i] = Support
        if(Support >= MinSupport):
            FrequentSequences.append(i)
    
    
    
#Generate all possible two item candidates in two ways (temporal and non temporal)
#Remove the ones that don't meet support threshold (hint: use the isSubSequence method as a helper function here)
#Add the frequent sequences to the FrequentSequences list.
def generateTwoItemsCandidateSequences():
    ListOfCandidates = []
    #Temporal Joins
    
    for i in FrequentSequences:
        for j in FrequentSequences:
            ListOfCandidates.append(i+j)
    
            
    for i in FrequentSequences:
        for j in FrequentSequences[FrequentSequences.index(i)+1: len(FrequentSequences)]:
            ListOfCandidates.append('('+i+j+')')
    
    
    for i in ListOfCandidates:
        Support = calculateSupport(i)
        SequencesSupport[i] = Support
        if(Support >= MinSupport):
            FrequentSequences.append(i)


    
    
    
    
#Function that takes a sequence and returns a list of all possible subsequences (used for pruning)
def getAllSubSequences(Sequence):
    print("Remove the print and do meeee")
    






#K is >= 3, this function generates k item sequences by joining k-1 sequences, where the join condition is that
#the first sequence's end should match the second sequence's beginning (temporal aspect put into consideration)
#after generating the sequence it should be pruned 
#to prune, get all sub sequences of a sequence (hint: use the getAllSubSequences() function ) 
#If one of the sub sequences of has support less than the minimum, the whole sequence is pruned (discarded), 
#This is known as downward closure property (also used in Apriori)
#After pruning, you need to calculate support for each sequence (you can use the isSubSequence() here)
#Discard sequences that don't meet minimum support
def generateKItemsCandidateSequences(k):
    print("Remove the print and do meeee")
    







#This function runs the algorithm by executing all the previous functions, it also prints all frequent sequences
#in the FrequentSequencesList
def GSPAlgorithm():
    print("Hi there, I am supposed to implement the GSP algorithm, Please implement meeee :D")





sup = calculateSupport('FA')

print (sup)

#generateOneItemCandidateSequences()

#generateTwoItemsCandidateSequences()

#print (FrequentSequences)












