''' Script for gathering lists of (sub-)committee members'''

# TODO:
# * Keep track of pages that can't be parsed (i.e., that may have changed) and
#   don't include them in the data; email the list to someone
# * What if the page times out?

import urllib2
from BeautifulSoup import BeautifulSoup

def comm_agriculture():
    members = ['"House Committee on Agriculture"', '"HSAG"']
    page = urllib2.urlopen("http://agriculture.house.gov/inside/members.html")
    soup = BeautifulSoup(page)
    memberlists = soup.findAll('ul', 'memberlist') # Second arg: class attr val
    for list in memberlists:
        for member in list.findAll('li'):
            href = member.find('a')
            members.append('"' + href.contents[0] + '"')

    return ', '.join(members)

# TODO:
#  * Need to handle/include the short names for these subcommittees
def subcomm_agriculture():
    name_prefix = '"House Committee on Agriculture'
    page = urllib2.urlopen("http://agriculture.house.gov/inside/subcomms.html")
    soup = BeautifulSoup(page)
    committeelists = soup.findAll('table', 'sublist')
    subcommittees = ''

    for list in committeelists:
        members = []
        summary = ''
        if list.has_key('summary'):
            summary = list['summary']
        else:
            # Handle the typo
            if list.has_key('summmary'):
                summary = list['summmary']
            else:
                continue

        shortsummary = summary.replace('members of the ', '')
        members.append(name_prefix + '/' + shortsummary + '"')
        for listitem in list.findAll('li'):
            members.append('"' + listitem.find('a').contents[0] + '"')
        subcommittees += ', '.join(members) + '\n'
    return subcommittees

def comm_appropriations():
    page = urllib2.urlopen("http://appropriations.house.gov/members111th.shtml")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Appropriations"', '"HSAP"']
    memberlist = soup.find('table')
    for member in memberlist.findAll('a'):
        comma_idx = member.contents[0].find(',')
        members.append('"' + member.contents[0][:comma_idx] + '"')
        
    return ', '.join(members)

tasks = [comm_agriculture, subcomm_agriculture, comm_appropriations]

for t in tasks:
    print t()
