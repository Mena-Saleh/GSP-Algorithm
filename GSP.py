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




df = pd.DataFrame(Data);


#Should be at least 2, (1 or 0 doesn't function because it is logically incorrect)
MinSupport = 2

#Dictionary to store calculated support of sequences as we go (used for pruning)
#Ex: 'AB(CD)' : 3 , which means that sequence has a support of three
SequencesSupport = {}

#List that contains frequent sequences, Ex: 'A' or 'BC(DF)' 
FrequentSequences = []


##    <<--  HELPER FUNCTIONS  -->>




#Takes a sequence and splits it into a list a of elements, EX AB(CD)E ==> [A,B,(CD),E]
def splitSequence(Sequence):
    #Split the SubSequence into individual elements (non temporal in mind)
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



#Function that checks if SubSequence is a sub sequence of SuperSequence, and returns true if so.
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
                    ElemValueToCutFrom = j
                    TemporalFlag = True
                    for k in TemporalSplit:
                        if(k in j):
                            j = j.replace(k, '')
                        else:
                            TemporalFlag = False
                            break
                    if(TemporalFlag):
                        SuperSequenceSplit = SuperSequenceSplit[SuperSequenceSplit.index(ElemValueToCutFrom) + 1: len(SuperSequenceSplit)]
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
    
    

#Function that calculates the support of a given sequence
def calculateSupport(Sequence):
    Support = 0
    for i in df.index:
        if (isSubSequence(Sequence, df.iloc[i].Sequence)):
            Support = Support + 1

    return Support


#Function that inserts given string into source string at given position
def insertStringAtPosition (SourceString, InsertString, Position):
    if(Position == -1):
        return SourceString + InsertString
    else:
        return SourceString[:Position] + InsertString + SourceString[Position:]





##      <<-- MAIN FUNCTIONS  -->>

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
    
    FrequentSequences.sort()
    
#Generate all possible two item candidates in two ways (temporal and non temporal) and remove infrequent ones.
def generateTwoItemsCandidateSequences():
    ListOfCandidates = []
    
    #Temporal Joins:
    for i in FrequentSequences:
        for j in FrequentSequences:
            ListOfCandidates.append(i+j)
    
    #Non Temporal Joins:     
    for i in FrequentSequences:
        for j in FrequentSequences[FrequentSequences.index(i)+1: len(FrequentSequences)]:
            ListOfCandidates.append('('+i+j+')')
    
    #Add only the frequent ones to the FrequentSequences list:
    for i in ListOfCandidates:
        Support = calculateSupport(i)
        SequencesSupport[i] = Support
        if(Support >= MinSupport):
            FrequentSequences.append(i)


    
    
    




#Function thag generates K item sequences, where k >= 3, sequences are then pruned according to downward closure property
#, finally the infrequent ones are removed. Returns false if it is not possible to generate, otherwise true
def generateKItemsCandidateSequences(k):
    
    #Get all k-1 frequent sequences first:
    FrequentKMinus1Sequences = []
        
    #Loop over all frequent sequences to get the sequences of length k-1 (excluding brackets):
    for i in FrequentSequences:
        ToCheckLengthOf = i
        if(len(ToCheckLengthOf.replace('(', '').replace(')', '')) == k-1):
            FrequentKMinus1Sequences.append(i)
    
    
    #Get the beginnings and ends, EX:   ABC -> MinusFirst is BC and MinusLast is AB
    #Also record the removed elements from end and beginning at what indices as well.
    
    #Stores the sections without first and last elements
    MinusFirst = []
    MinusLast = []
    
    #Stores first and last elements
    FirstElements = [] 
    LastElements = [] 
    
    #Stores indices if element is non temporal, 0 or -1 if temporal(first and last)
    FirstElementsIndices = []
    LastElementsIndices = []
    
    for i in FrequentKMinus1Sequences:
        for j in range(0, len(i)):
            if(i[j] != '('):
                FirstElements.append(i[j])
                FirstElementsIndices.append(j)
                MinusFirst.append(i.replace(i[j], ''))
                break
        
        for j in range(len(i)-1, 0, -1):
            
            if(i[j] != ')'):
                #Store the index if it is not the last, and -1 if it is the last
                if(j!= len(i)-1):
                    LastElementsIndices.append(j)
                else:
                    LastElementsIndices.append(-1)
                    
                LastElements.append(i[j])
                MinusLast.append(i.replace(i[j], ''))
                break


    #Generate k-Item candidates by matching MinusFirsts and MinusLasts (using isSubSequence to handle non temporal elements)
    KItemCandidates = []
    
    for i in range(0, len(FrequentKMinus1Sequences)):
        for j in range(0, len(FrequentKMinus1Sequences)):
            if (i != j and (isSubSequence(MinusFirst[i], MinusLast[j])  or isSubSequence(MinusLast[j], MinusFirst[i]) ) ): #If matching and not the same element
                MatchingSection = MinusFirst[i] if (len(MinusFirst[i]) >= len(MinusLast[j])) else MinusLast[j]
                
                #Append first and last elements at the right place:
    
                Candidate = insertStringAtPosition(MatchingSection, FirstElements[i], FirstElementsIndices[i])
                
                ##If last element then just insert at end, else increase index by one because firstElement was added so the indices are shifted by one
                if(LastElementsIndices[j] == -1):
                    Candidate = insertStringAtPosition(Candidate, LastElements[j], LastElementsIndices[j])
                else:
                    Candidate = insertStringAtPosition(Candidate, LastElements[j], LastElementsIndices[j] + 1)

                KItemCandidates.append(Candidate) #Add the matched item
    
    
    #Return false if no candidates where generated
    if(len(KItemCandidates) == 0):
        return False


    #Pruning according to downward closure principle
    #Loop over all pre-recorded supports in the dicitonary, and if there is an infrequent subset in the candidates, then exclude the whole candidate
    KItemCandidatesPruned = []
    KItemCandidatesPruned.extend(KItemCandidates)

    for i in KItemCandidates:
        for j in SequencesSupport.keys():
            if(isSubSequence(j, i) and SequencesSupport[j] < MinSupport):
                #If a subsequence of the candidate is infrequent, remove the candidate (downward closure property)
                KItemCandidatesPruned.remove(i)
                break
    

    #Calculating support for pruned candidates and removing infrequent ones:
    for i in KItemCandidatesPruned:
        Support = calculateSupport(i)
        SequencesSupport[i] = Support
        if(Support >= MinSupport):
            FrequentSequences.append(i)
            
    return True


#This function runs the algorithm by executing all the previous functions, it also prints all frequent sequences
#in the FrequentSequencesList
def GSPAlgorithm():
    
    #Generate one-item frequent sequences:
    generateOneItemCandidateSequences()
    
    #Generate two-item frequent sequences:
    generateTwoItemsCandidateSequences()
    
    #Generate K-item frequenct sequences untill there is no more to generate(the generate function returns false if it is not possible to generate more)
    i = 3
    while generateKItemsCandidateSequences(i):
        i = i + 1

    print(FrequentSequences)






#Algorithm Run:
    
GSPAlgorithm()













