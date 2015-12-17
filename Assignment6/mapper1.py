#!/usr/bin/python
import sys
import re
import simplejson as json

def main(argv):
    word_patt = re.compile("[0-9a-zA-Z_\-#@][a-zA-Z0-9_\-@#]+")
   # word_patt = re.compile("[#@a-zA-Z][a-zA-Z0-9]*")
    for line in sys.stdin:
        try:
            jObj = json.loads(line)
            text = jObj['text']
            for match in word_patt.findall(text):
                print "LongValueSum:" + match.lower() + "\t" + str(1)
        except:
            sys.stderr.write("Skipping line!")

if __name__ == "__main__":
    main(sys.argv)
