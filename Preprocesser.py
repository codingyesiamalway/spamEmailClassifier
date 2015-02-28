__author__ = 'Yu Zhao'

def createEmailList(spamFile, nonSpamFile):
    spamEmailList = []
    with open(spamFile, 'r') as file :
        curEmail = ''
        for curLine in file:
            line = curLine.strip()
            if line == '----':
                spamEmailList = spamEmailList + [curEmail]
                curEmail = ''
            else:
                curEmail = curEmail + ' ' + line

    return spamEmailList


x = createEmailList("D:\\projects\\spamEmailClassifier\\spam.txt", '')
print x