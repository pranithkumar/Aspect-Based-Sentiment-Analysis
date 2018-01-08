import omsFunctions

def printResultChoice():

    #userChoice = str(input('\nDo you want to print the result on output window? (Y/N) :'))
    userChoice = 'Y'
    if(userChoice=='Y' or userChoice=='y'):

        return True

    else:

        return False

#_FolderName='Data\\OppoF1\\'

#_FolderName='Data\\MotoXPlay\\'

_ReviewDataset='reviews.txt'

_PreProcessedData='1.PreProcessedData.txt'

_TokenizedReviews='2.TokenizedReviews.txt'

_PosTaggedReviews='3.PosTaggedReviews.txt'

_Aspects='4.Aspects.txt'

_Opinions='5.Opinions.txt'

print("\nWELCOME TO OPINION MINING SYSTEM  ")

print("-------------------------------------------------------------")

#input("Please Enter any key to continue...")

print("\n\n\n\n\n\nPREPROCESSING DATA")

omsFunctions.preProcessing(_ReviewDataset,_PreProcessedData,printResultChoice())

print("\n\n\n\n\n\nREADING REVIEW COLLECTION...")

omsFunctions.tokenizeReviews(_ReviewDataset,_TokenizedReviews,printResultChoice())

print("\n\n\n\n\n\nPART OF SPEECH TAGGING...")

omsFunctions.posTagging(_TokenizedReviews,_PosTaggedReviews,printResultChoice())

print("\nThis function will list all the nouns as aspect")

omsFunctions.aspectExtraction(_PosTaggedReviews,_Aspects,printResultChoice())

print("\n\n\n\n\n\nIDENTIFYING OPINION WORDS...")

omsFunctions.identifyOpinionWords(_PosTaggedReviews,_Aspects,_Opinions,printResultChoice())


