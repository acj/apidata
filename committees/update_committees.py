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

def comm_armedservices():
    page = urllib2.urlopen("http://armedservices.house.gov/list_of_members.shtml")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Armed Services"', '"HSAS"']
    memberlist = soup.find('div', align='center')
    for member in memberlist.findAll('a'):
        atag = member.find('span')
        if atag == None:
            atag = member.find('font') # Correct for html error
        comma_idx = atag.contents[0].find(',')
        members.append('"' + atag.contents[0][:comma_idx] + '"')
    return ', '.join(members) + '\n'

def subcomm_armedservices():
    def parse_members(name, shortname, tbody):
        name_prefix = '"House Committee on Armed Services/'
        members = [name_prefix + name + '"', '"' + shortname + '"']
        names = tbody.findAll('span')
        for name in names:
            # Two common errors: an extra font tag, and an extra span tag
            font_tag = name.find('font')
            span_tag = name.find('span')
            if font_tag != None:
                name = font_tag
            elif span_tag != None:
                name = span_tag
            if len(name.contents) == 0:
                continue
            clean_name = str(name.contents[0]).replace('Chairman ', '').replace('Ranking Member ', '')
            commapos = clean_name.find(',')
            if commapos == -1:
                continue
            members.append('"' + clean_name[:commapos] + '"')
        return members

    page = urllib2.urlopen("http://armedservices.house.gov/subcommittee.shtml")
    soup = BeautifulSoup(page)
    all_members = ''
    subcomms = soup.findAll('tbody')
    all_members += ', '.join(parse_members('Subcommittee on Readiness', 'HSAS_rdi', subcomms[1])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Seapower and Expeditionary Forces', 'HSAS_sea', subcomms[2])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Air and Land Forces', 'HSAS_alf', subcomms[3])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Oversight and Investigations', 'HSAS_osi', subcomms[4])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Terrorism, Unconventional Threats and Capabilities', 'HSAS_ter', subcomms[5])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Strategic Forces', 'HSAS_stf', subcomms[6])) + '\n'
    all_members += ', '.join(parse_members('Subcommittee on Military Personnel', 'HSAS_mip', subcomms[7])) + '\n'

    return all_members

def comm_budget():
    page = urllib2.urlopen("http://budget.house.gov/members.shtml")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Budget"', '"HSBU"']
    lists = soup.findAll('ol')
    for lst in lists:
        for member in lst.findAll('a'):
            name = str(member.contents[0]).strip()
            members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def comm_edlabor():
    page = urllib2.urlopen("http://edlabor.house.gov/about/members/")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Education and Labor"', '"HSED"']
    lists = soup.find('div', 'page-asset asset')
    listitems = lists.findAll('li')
    for lst in listitems:
        name = lst.find('a').contents[0]
        name = name.replace('"', '\\"')
        members.append('"' + name.replace(', Chairman', '') + '"')
    return ', '.join(members) + '\n'

def subcomm_edlabor():
    page = urllib2.urlopen("http://edlabor.house.gov/about/members/")
    soup = BeautifulSoup(page)
    tables = soup.findAll('table', width='100%')
    member_string = ''

    def parse_names(subcomm, shortname, table):
        members = ['"' + subcomm + '"', '"' + shortname + '"']    
        names = table.findAll('td')
        for name in names:
            n = str(name.contents[0]).replace('"', '\\"')
            if n.find('Democrats') != -1 or n.find('Republicans') != -1:
                continue
            if n == '<br />':
                continue
            members.append('"' + n.replace(',', '').strip() + '"')
        return members

    # Early Childhood, Elementary, Secondary Ed
    member_string += ', '.join(parse_names('Subcommittee on Early Childhood, Elementary and Secondary Education', 'HSED_kid', tables[0])) + '\n'

    # Healthy Families and Communities
    member_string += ', '.join(parse_names('Subcommittee on Healthy Families and Communities', 'HSED_hfc', tables[1])) + '\n'

    # Higher Education, Lifelong Learning and Competitiveness
    member_string += ', '.join(parse_names('Subcommittee on Higher Education, Lifelong Learning and Competitiveness', 'HSED_hed', tables[2])) + '\n'

    # Health, Employment, Labor, and Pensions
    member_string += ', '.join(parse_names('Subcommittee on Health, Employment, Labor, and Pensions', 'HSED_hel', tables[3])) + '\n'

    # Workforce Protections
    member_string += ', '.join(parse_names('Subcommittee on Workforce Protections', 'HSED_wfp', tables[4])) + '\n'

    return member_string

def comm_energycommerce():
    page = urllib2.urlopen("http://energycommerce.house.gov/index.php?option=com_content&view=category&layout=blog&id=160&Itemid=61")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Energy and Commerce"', '"HSIF"']
    lists = soup.find('tbody')
    listitems = lists.findAll('td')
    for lst in listitems:
        name = str(lst.contents[0])
        if name == ' ':
            continue
        comma_pos = name.find(',')
        if comma_pos == -1:
            continue
        else:
            members.append('"' + name[:comma_pos] + '"')
    return ', '.join(members) + '\n'

def subcomm_energycommerce():
    def parse_names(url, subcomm, shortname):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = ['"' + subcomm + '"', '"' + shortname + '"']    
        tbody = soup.find('tbody')
        listitems = tbody.findAll('td')
        for lst in listitems:
            if len(lst.contents) == 0:
                continue
            name = str(lst.contents[0])
            if name == ' ':
                continue
            comma_pos = name.find(',')
            if comma_pos == -1:
                continue
            else:
                members.append('"' + name[:comma_pos] + '"')

        return members

    member_string = ''

    # Energy and the Environment
    member_string += ', '.join(parse_names('http://energycommerce.house.gov/index.php?option=com_content&view=article&id=1569&catid=160&Itemid=61', 'Subcommittee on Energy and the Environment', 'HSIF_env')) + '\n'

    # Commerce, Trade, and Consumer Protection
    member_string += ', '.join(parse_names('http://energycommerce.house.gov/index.php?option=com_content&view=article&id=1572&catid=160&Itemid=61', 'Subcommittee on Commerce, Trade, and Consumer Protection', 'HSIF_ctc')) + '\n'

    # Communications, Technology, and the Internet
    member_string += ', '.join(parse_names('http://energycommerce.house.gov/index.php?option=com_content&view=article&id=1570&catid=160&Itemid=61', 'Subcommittee on Communications, Technology, and the Internet', 'HSIF_cti')) + '\n'

    # Health
    member_string += ', '.join(parse_names('http://energycommerce.house.gov/index.php?option=com_content&view=article&id=1571&catid=160&Itemid=61', 'Subcommittee on Health', 'HSIF_hth')) + '\n'

    # Oversight and Investigations
    member_string += ', '.join(parse_names('http://energycommerce.house.gov/index.php?option=com_content&view=article&id=1573&catid=160&Itemid=61', 'Subcommittee on Oversight and Investigations', 'HSIF_osi')) + '\n'

    return member_string

tasks = [comm_agriculture, subcomm_agriculture, comm_appropriations, subcomm_appropriations, comm_armedservices, subcomm_armedservices, comm_budget, comm_edlabor, subcomm_edlabor, comm_energycommerce, subcomm_energycommerce]

for t in tasks:
    print t(),
