''' Script for gathering lists of (sub-)committee members'''

# TODO:
# * Keep track of pages that can't be parsed (i.e., that may have changed) and
#   don't include them in the data; email the list to someone
# * What if the page times out?

import re
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

    return ', '.join(members) + '\n'

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
        members.append('""') # TODO: Short name
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
        
    return ', '.join(members) + '\n'

def subcomm_appropriations():
    def parse_members(subcomm_name, shortname, url):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = ['"' + subcomm_name + '", "' + shortname + '"']
        memberlist = soup.find('div', id='MembersList')
        paras = memberlist.findAll('p')
        names = str(paras[1]) + str(paras[3])
        names = names.replace('Chair:', '')
        re_names = re.compile(r'([A-Z][a-z]+.*) \([A-Z][A-Z]\).*')
        
        for name in re_names.findall(names):
            members.append('"' + name + '"')
        return members
    
    subcommittees = ''
    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Agriculture, Rural Development, Food and Drug Administration, and Related Agencies', 'HSAP_fda', 'http://appropriations.house.gov/Subcommittees/sub_ardf.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Commerce, Justice, Science, and Related Agencies', 'HSAP_com', 'http://appropriations.house.gov/Subcommittees/sub_cjs.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Defense', 'HSAP_def', 'http://appropriations.house.gov/Subcommittees/sub_def.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Energy and Water Development', 'HSAP_ene', 'http://appropriations.house.gov/Subcommittees/sub_ew.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Financial Services and General Government', 'HSAP_fin', 'http://appropriations.house.gov/Subcommittees/sub_fsdc.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Homeland Security', 'HSAP_dhs', 'http://appropriations.house.gov/Subcommittees/sub_dhs.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Interior, Environment, and Related Agencies', 'HSAP_doi', 'http://appropriations.house.gov/Subcommittees/sub_ienv.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Labor, Health and Human Services, Education, and Related Agencies', 'HSAP_hhs', 'http://appropriations.house.gov/Subcommittees/sub_lhhse.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Legislative Branch', 'HSAP_leg', 'http://appropriations.house.gov/Subcommittees/sub_leg.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Military Construction, Veterans Affairs, and Related Agencies, VA', 'HSAP_dva', 'http://appropriations.house.gov/Subcommittees/sub_mivet.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on State, Foreign Operations, and Related Programs', 'HSAP_sta', 'http://appropriations.house.gov/Subcommittees/sub_sfo.shtml')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Transportation, Housing and Urban Development, and Related Agencies', 'HSAP_hud', 'http://appropriations.house.gov/Subcommittees/sub_tranurb.shtml'))

    return subcommittees + '\n'



tasks = [comm_agriculture, subcomm_agriculture, comm_appropriations, subcomm_appropriations]

for t in tasks:
    print t(),
