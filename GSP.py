import pandas as pd


#Data is static for now, because it is hard to find sequential datasets
Data = { 
        'Sequence ID': [1,2,3,4,5],
        
         'Sequence': ['<AB(FG)CD>',
                      '<BGD>',
                      '<BFG(AB)>',
                      '<F(AB)CD>',
                      '<A(BC)GF(DE)>'
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
Support = {}

#List that contains frequent sequences, Ex: 'A' or  
FrequentSequences = []

#Function that checks if SubSequence is a sub sequence of SuperSequence, and returns true if so
def isSubSequence(SubSequence, SuperSequence):
    print("Remove the print and do meeee")
        


#Generate one item candidates based on support, also register them in the Support dictionary and FrequentSequences
def generateOneItemCandidateSequences():
    print("Remove the print and do meeee")
    
    
    
#Generate all possible two item candidates in two ways (temporal and non temporal)
#Remove the ones that don't meet support threshold (hint: use the isSubSequence method as a helper function here)
#Add the frequent sequences to the FrequentSequences list.
def generateTwoItemsCandidateSequences():
    print("Remove the print and do meeee")
    
    
    
    
    
#Function that takes a sequence and returns a list of all possible subsequences ()
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



















