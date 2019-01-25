###
### Hi!
### SCROLL DOWN UNTIL IT SAYS 'LOOK AT ME'!
###
###    |
###    |
###    |
###    |
###    V
###
###
import csv
import sys
import os
import json
from pprint import pprint
from datetime import datetime
import argparse
import collections
import helpers
import signal

frames = collections.OrderedDict()


#####################################################################
#####################################################################
# LOOK AT ME!
#####################################################################
#####################################################################

# whew, you found us.

# this is a comment! it means that it's ignored by the computer, and is just humanspeak
# which means we can talk to you in this medium.

# so, we've carefully organized this python code so that
# you can get started immediatelly without having to know everything about python.

# personally, we find it easier to learn while we're doing things and changing/breaking things
# so this will be an exercise in changing the code and playing around with it.

# the following chunks of code illustrate 'Frames' - a nickname for a way to sort and search through your queries.
# (A 'frame' isn't specialized code lingo or Python terminology or anything, just our own nickname )


#################################
##### EXAMPLE 1 : MIDNIGHT SEARCH


def midnight_search(query):                 # 'define' a function called 'midnight_search'.
                                            # (A function is a piece of code that often takes in something,
                                            # does something to it, and often spits it out again, like a pasta maker.)

#    print(query)
                                            # a 'query' object has a bunch of attributes 'attached' to it.
                                            # if you want to see what they are, uncomment the above line
                                            # by removing the '#' at the start of the line.

    if( query['hour'] == 0):                # if the 'hour' attribute of this search query is 0, aka around midnight,
        return True                         # return true -- or say "YES, we do want this query."


frames['midnight_search'] = midnight_search # this is a little hard to explain, but it stores our function in a 'dict', or a table called 'frames'
                                            # so we can look it up later.



#################################
##### EXAMPLE 2 : YEAR END HOLIDAYS

def year_end_holidays(query):
    if( query['weekofyear'] == 52):         # if the week of year is 52, return true
        return True                         # (there are 53 weeks in a year, but most code starts with 0, so 52 is the 53th week of the year)
                                            # AKA around Christmas and New Year's
    if( query['weekofyear'] == 0):          # OR if the week of year is 0, return true
        return True                         # AKA around New Year's
frames['year_end_holidays'] = year_end_holidays

# Notice how you can 'stack' queries as a way to say "OR".
# Could you easily add a third week of the year?



#################################
#### EXAMPLE 3: WEE HOURS

def wee_hours(query):
    if( query['hour'] >= 2 and query['hour'] <= 6 ):    # if the hour is later than 2 (am) *AND* 6 (am), return true.
        return True                                     # you can frame AND statements this way
frames['wee_hours'] = wee_hours




#################################
#### EXAMPLE 4: SEARCH HOW

def search_for_how(query):
    if( "how" in query['data_query'].lower() ):    # if the word "how" is in the data query text, made lowercase, return true
        return True                                # Here's a question: how could you search for both "how" and "why" in a search query,
                                                    # looking at example 2?
frames['search_for_how'] = search_for_how



#################################
#### EXAMPLE 5: PLAY AROUND

def why_at_midnight(query):
    if( query['hour'] == 0 and "why" in query['data_query'] ):
        return True
frames['why_at_midnight'] = why_at_midnight




#################################
#### EXAMPLE 6: ADVANCED

# if you're here, you probably know what you're doing.
# this function is a filter function passed into `filter`.
# go wild!
# some ideas we had:
    # weather api: who am I when it was rainy, and what did I search for?
    # who am I when it was cold, and what did I search for?
    # astrology frame: who was I when Mercury was in retrograde?
    # what are all the music lyrics I searched for?


# def custom(query):
#     pass
# frames['custom'] = custom




#################################
#################################
#################################
#################################
#################################






class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def get_datetime_from_query(q):
    d = datetime.fromtimestamp(float(q['timestamp_usec']) / 1000000.0)
    return d

def simpleprint(q):
    if type(q) == dict:
        print(q['datetime']), " --- ",
        print(q['data_query'])
    if type(q) == list:
        for thisq in q:
            simpleprint(thisq) # funky recursion print

def get_frame_user_input(opts):
    num = -1
    while num == -1: #
        print(" ===== Choose how you want to reframe your data:")
        print(" ===== Select one of our premade frames (e.g. 2)")
        print(" ===== Or type in text to search.")
        print("       Text separated by vertical bars '|' will searched as an OR query, ANYthing matching all terms (e.g. data|cindy): ")
        print("       Text separated by plus symbols  '+' will searched as an AND query, EVERYthing matching all terms (e.g. when+why): ")
        print(" ")
        print(" ===== Or to exit, hit control-C. ")
        print(" ")
        for i, k in enumerate(opts):
            print(" (", i, ") :",  k)
        print(" ")
        inp = input(" ---> ")
        try:
            num = int(inp) # triggers exception on non-integer input
            if(num < 0 or num >= len(opts)):
                print("Choose a valid number!")
                num = -1
            else:
                logstring = " === Searching with frame: "+ opts[num]
                return ("int", num, logstring)
        except:
            if("+" in inp):
                strs = inp.lower().split("+") #TODO: better non-string handling
                logstring = " === Searching with : "+ " AND ".join(strs)
                print(logstring)
                return ("str-and", strs, logstring)
            else:
                strs = inp.lower().split("|") #TODO: better non-string handling
                logstring = " === Searching with : "+ " OR ".join(strs)
                return ("str-or", strs, logstring)


def exit_handler(signal, frame):
	print("")
	print(" *** Exiting! ***")
	sys.exit(0)

def parseargs():
    global allqueries, args, jsonfilename

    parser = DefaultHelpParser(description='Help pickout google queries')
    parser.add_argument('-j','--json', help='Input JSON file')
    parser.add_argument('-o','--output', help='Output filename for .csv and .json files')
    args = vars(parser.parse_args())

    if(args['json'] == None):
        jsonfilename = "all_google_queries_simplified.json"
    else:
        jsonfilename = args['json']

    signal.signal(signal.SIGINT, exit_handler)


def queryrun():

    global allqueries, args, jsonfilename

    typ, inp, logstring = get_frame_user_input(frames.keys())

    # run frame
    if(typ == "int"):
        framename = frames.keys()[inp]
        frameprint = "--FRAME-" + framename
        result = filter(frames[framename], allqueries)

    # AND search
    if(typ == "str-and"):
        frameprint = "--SEARCH-" + "+".join(inp)
        result = []
        for q in allqueries:
            if(all(searchterm in q['data_query'].lower() for searchterm in inp)):
                result.append(q)

    # OR search
    if(typ == "str-or"):
        frameprint = "--SEARCH-" + "-".join(inp)
        result = []
        for q in allqueries:
            if(any(searchterm in q['data_query'].lower() for searchterm in inp)):
                result.append(q)


    if(len(result) == 0):
        print(" === NO RESULTS!")
    else:
        ###### PRINT AND WRITE FILES!
        simpleprint(result)

        if(args['output'] != None):
            filebase = args['output']
        else:
            filebase = os.path.splitext(jsonfilename)[0] + frameprint

        helpers.csvsave(helpers.outputdir + filebase + ".csv", result)
#        helpers.jsonsave(helpers.outputdir + filebase + ".json", result)

        print("\n")
        print(logstring)
        print(" ===  " + frameprint)
        print(" ===  # of results:", len(result))
        print(" ===  Frame was saved at '" + helpers.outputdir + filebase + ".csv'")
#        print("                  and at '" helpers.outputdir + filebase + ".json'")
        print(" ")



def main():
    global allqueries, args, jsonfilename

    parseargs()
    with open(helpers.outputdir + jsonfilename) as data:
        allqueries = json.load(data)

    print(" ")
    print(" ===== Loaded JSON file called " + jsonfilename + " !")
    print(" ")

    while True:
        queryrun()


if __name__ == "__main__":
    main()
