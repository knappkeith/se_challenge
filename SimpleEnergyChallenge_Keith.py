from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

__author__ = 'Keith Knapp'

def Open_Firefox_Browser(InputStr):

    #Settings
    WebAddress = 'http://www.google.com'

    #String for searching
    SearchBoxTag = 'q'

    #Open a Browser and goto Web Address
    NewBrowser = webdriver.Firefox()
    NewBrowser.get(WebAddress)

    #Search for Search String
    SearchBox = NewBrowser.find_element_by_name(SearchBoxTag)
    SearchBox.send_keys(InputStr + Keys.RETURN)

    #Wait to make sure Page Loads all the way
    #Was found that the title is the last thing to change so wait for it to contain the search string
    WebDriverWait(NewBrowser, 10).until(EC.title_contains(InputStr))

    #Return the Browser object
    return NewBrowser

def Find_Search_Results(Browser, QuitWhenDone, DebugPrinting):

    #String for searching
    ElementTag_1 = 'div'
    ElementTag_2 = 'li'
    ElementTag_3 = 'a'
    ElementAtt_1 = 'id'
    ElementAtt_1_Value = 'ires'

    #Get the first list of Elements
    ElemArray = Browser.find_elements_by_tag_name(ElementTag_1)

    #Go Through each element
    for x in range(len(ElemArray)):
        try:
            #Make sure element has the correct attribute
            if ElemArray[x].get_attribute(ElementAtt_1) == ElementAtt_1_Value:
                if DebugPrinting:
                    print('Found Results')

                #Get the next list of elements
                HeaderArray = ElemArray[x].find_elements_by_tag_name(ElementTag_2)
        except:
            if DebugPrinting:
                print('Error')

    #Print number of links found
    if DebugPrinting:
        print(format(len(HeaderArray))+' Links in the results field were found!')

    MyResults = []
    for y in range(len(HeaderArray)):
        if HeaderArray[y].get_attribute(ElementAtt_1) == "":
            LinkArray = HeaderArray[y].find_elements_by_tag_name(ElementTag_3)

            for x in range(1):
                try:
                    if LinkArray[x].text != "":
                        MyResults.append(LinkArray[x].text)
                        if DebugPrinting:
                            print('...'+format(len(LinkArray)))
                        if DebugPrinting:
                            print(LinkArray[x].text)
                        if DebugPrinting:
                            print(LinkArray[x].get_attribute('href'))
                except:
                    if DebugPrinting:
                        print('No Links in List')
    if QuitWhenDone:
        Browser.quit()
    return MyResults

def Search_Search_Results(TheResults, NumInterested, Input_Str, ResultIsCaseSensitive, DoNotPrint):
    if len(TheResults) == 0:
        if not DoNotPrint:
            print('There were no results returned for: '+Input_Str)
    else:
        if NumInterested > len(TheResults):
            if not DoNotPrint:
                print('There are less than '+format(NumInterested)+' search results. Only ')
            NumInterested = len(TheResults)
        for x in range(NumInterested):
            if Input_Str in TheResults[x]:
                if not DoNotPrint:
                    print('')
                    print(Input_Str+' was found in Search result #'+format(x+1)+':')
                    print('    '+TheResults[x])
                    print('Exiting...')
                return True
            if not ResultIsCaseSensitive:
                if Input_Str.upper() in TheResults[x].upper():
                    if not DoNotPrint:
                        print('')
                        print(Input_Str+' was found in Search result #'+format(x+1)+', but not exactly:')
                        print('    '+TheResults[x])
                        print('Exiting...')
                    return True
    return False

#Define the Main Proceedure if this is called on it's own
if __name__ == "__main__":

    #Number of Results to search in
    Num_Interested = 4

    #Set to True to have the results be case sensitive
    Result_Is_Case_Sensitive = False

    #Booleans for behavior
    DebugPrinting = False   #Lots of printed stuff
    QuitWhenDone = True     #Closes Browser window when the results have been pulled
    DoNotPrint = True       #TRUE means some printing, FALSE means none except final output and required input

    #Determine Input String
    UserInput = ""
    if len(sys.argv) != 2:

        #Uncomment here to have Input be hard coded.
        #UserInput = "Recursion"
        #UserInput = "seleniumhq"
        #UserInput = "Best Buy"
        #UserInput = "ds;lkjfhasdjkfghkjhgkjhds"

        #Check if Input String is blank and ask for Input
        print('')
        if UserInput == "":
            UserInput = input('Enter your Query, Please: ')
        else:
            if not DoNotPrint:
                print('Query was HARDCODED to: '+UserInput)
    else:

        #Set Input to Argument
        UserInput = sys.argv[1]

    #Make sure that the search query is a string
    if not UserInput.isprintable():
        print('')
        print('The search Query needs to be a string!')
        raise SystemExit

    #Open Browser and Search
    User_Browser = Open_Firefox_Browser(UserInput)

    #Get the Link Text for the search Results
    User_Results = Find_Search_Results(User_Browser, QuitWhenDone, DebugPrinting)

    #Search the Search Results and Print if it was a success or not
    print('')
    if Search_Search_Results(User_Results, Num_Interested, UserInput, Result_Is_Case_Sensitive, DoNotPrint):
        print('SUCCESS, '+UserInput+' was found in the first '+format(Num_Interested)+' results!')
    else:
        print('FAILED, '+UserInput+' WAS NOT found in the first '+format(Num_Interested)+' results!')