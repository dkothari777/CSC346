#!/usr/bin/python
import sys

def main(argv):
    word_dict = {}
    valueList = [0,0,0,0,0,0,0,0,0,0]
    wordList = ["","","", "", "", "", "", "", "", ""]
    uvList = [0,0,0,0,0,0,0,0,0,0]
    userList = ["","","", "", "", "", "", "", "", ""]
    hvList = [0,0,0,0,0,0,0,0,0,0]
    hashList = ["","","", "", "", "", "", "", "", ""]
    for line in sys.stdin:
        word, count= line.split('\t')
        count = int(count)
        if word[0] == '@':
            addToList(userList, uvList, word, count)
        elif word[0] == '#':
            addToList(hashList, hvList, word, count)
        else:
            addToList(wordList, valueList, word, count)
    #need to create top ten dict and print
    topTenList(wordList, valueList)
    topTenList(userList, uvList)
    topTenList(hashList, hvList)

def topTenList(wordList, valueList):
    for index in range(10):
        if wordList[index] == "":
            break
        print wordList[index] + '\t' + str(valueList[index])

def addToList(lst, vallst, word, count):
    for index in range(0, 10):
        if count > vallst[index]:
            lst.insert(index, word)
            vallst.insert(index, count)
            return

if __name__ == "__main__":
    main(sys.argv)
