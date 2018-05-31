#! python3
# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard.

import pyperclip, re , os , sys , pprint

def searchWord(myFile1):
    searchfile = open(myFile1, "r")
    myWord = str(input('what word to search:'))
    for line in searchfile:
        if myWord in line:
            print(line)
    searchfile.close()
    return


phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?                # area code
    (\s|-|\.)?                        # separator
    (\d{3})                           # first 3 digits
    (\s|-|\.)                         # separator
    (\d{4})                           # last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))?    # extension
    )''', re.VERBOSE)

# Create email regex.
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+      # username
    @                      # @ symbol
    [a-zA-Z0-9.-]+         # domain name
    (\.[a-zA-Z]{2,4})      # dot-something
    )''', re.VERBOSE)

# Find matches in clipboard text.
text = str(pyperclip.paste())
matches = []
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1], groups[3], groups[5]])
    if groups[8] != '':
        phoneNum += ' x' + groups[8]
    matches.append(phoneNum)
for groups in emailRegex.findall(text):
    matches.append(groups[0])

# Copy results to the clipboard.
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard:\n')
    print('\n'.join(matches))
    print('\n')
    saveToFile = pyperclip.paste()#To write the contents into a file.
    print('Enter the file name to save the contents(email and phone number)\n')
    myFile = str(input())
    with open(myFile,'a')as gotFile:
        gotFile.write(saveToFile)
        print('\n')
else:
    print('No phone numbers or email addresses found.\n')

print('\n')

#To search for a particular email in the file.
print('To perform search operation on a file,print (y/Y)\n')
flag = input()
if((flag == "Y") or ("y" == flag)):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f)
    print('Name of the file on with Search has to be done:\n')
    myFile1 = str(input())
    searchw = searchWord(myFile1)

else:
    print('exits program')
    sys.exit()



## TO PRINT THE LINES THAT COMES AFTER THE KEYWORD.
##with open("new.txt", "r") as f:
##    searchlines = f.readlines()
##myWord = str(input('what word to search:')) 
##for i, line in enumerate(searchlines):
##    if myWord in line: 
##        for l in searchlines[i:i+3]: print(l)
##        print
    
