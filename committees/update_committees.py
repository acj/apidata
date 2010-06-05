''' Script for gathering lists of (sub-)committee members'''

# TODO:
# * Keep track of pages that can't be parsed (i.e., that may have changed) and
#   don't include them in the data; email the list to someone
# * What if the page times out?

import re
import urllib2
from BeautifulSoup import BeautifulSoup, Comment, Tag

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
        if len(lst.contents) < 1:
            continue
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

def comm_financialservices():
    page = urllib2.urlopen("http://financialservices.house.gov/members.html")
    soup = BeautifulSoup(page)
    members = ['"House Committee on on Financial Services"', '"HSBA"']
    lists = soup.find('div', 'bodytext')
    listitems = lists.findAll('a')
    for lst in listitems:
        name = str(lst.contents[0])
        name = name.replace('Rep. ', '').replace('Chairman ', '')
        comma_pos = name.find(',')
        if comma_pos != -1:
            name = name[:comma_pos]
        members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def subcomm_financialservices():
    def extract_names(tag, name, shortname):
        names = [name, shortname]

        listitems = tag.findAll('td')
        for lst in listitems:
            paras = lst.findAll('p')
            for p in paras:
                re_names = re.compile(r'Rep.\s+([^\n]+) \([A-Z][A-Z]\).*')
                for c in tag.contents:
                    for name in re_names.findall(str(c)):
                        names.append('"' + name + '"')
        return names

    page = urllib2.urlopen("http://financialservices.house.gov/subassignments.html")
    soup = BeautifulSoup(page)
    member_string = ''
    members = ['"House Committee on Financial Services"', '"HSBA"']
    tables = soup.findAll('table')

    # Capital Markets, Insurance, and Government Sponsored Enterprises
    member_string += ', '.join(extract_names(tables[4], 'Subcommittee on Capital Markets, Insurance, and Government Sponsored Enterprises', 'HSBA_cap')) + '\n'

    # Financial Institutions and Consumer Credit
    member_string += ', '.join(extract_names(tables[5], 'Subcommittee on Financial Institutions and Consumer Credit', 'HSBA_fic')) + '\n'

    # Housing and Community Opportunity
    member_string += ', '.join(extract_names(tables[6], 'Subcommittee on Housing and Community Opportunity', 'HSBA_hco')) + '\n'

    # Domestic Monetary Policy and Technology
    member_string += ', '.join(extract_names(tables[7], 'Subcommittee on Domestic Monetary Policy and Technology', 'HSBA_dmp')) + '\n'

    # International Monetary Policy and Trade
    member_string += ', '.join(extract_names(tables[8], 'Subcommittee on International Monetary Policy and Trade', 'HSBA_imp')) + '\n'

    # Oversight and Investigations
    member_string += ', '.join(extract_names(tables[9], 'Subcommittee on Oversight and Investigations', 'HSBA_osi')) + '\n'

    return member_string

def comm_foreignaffairs():
    page = urllib2.urlopen("http://foreignaffairs.house.gov/members.asp")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Foreign Affairs"', '"HSFA"']
    # Retrieve chairman first
    member_div = soup.findAll('div', 'member')
    for member in member_div:
        a = member.find('a')
        name = str(a.contents[0]).replace('&nbsp;', ' ')
        members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def subcomm_foreignaffairs():
    def extract_names(url, name, shortname):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = ['"' + name + '"', '"' + shortname + '"']
        # Retrieve chairman first
        member_div = soup.findAll('div', 'member')
        for member in member_div:
            a = member.find('a')
            name = str(a.contents[0]).replace('&nbsp;', ' ')
            members.append('"' + name + '"')
        return members

    member_string = ''

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=2', 'Subcommittee on Africa and Global Health', 'HSFA_afr')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=3', 'Subcommittee on Asia, the Pacific, and the Global Environment', 'HSFA_pac')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=4', 'Subcommittee on Europe', 'HSFA_eur')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=5', 'Subcommittee on Terrorism, Nonproliferation, and Trade', 'HSFA_ter')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=6', 'Subcommittee on International Organizations, Human Rights, and Oversight', 'HSFA_hro')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=7', 'Subcommittee on the Middle East and South Asia', 'HSFA_mde')) + '\n'

    member_string += ', '.join(extract_names('http://foreignaffairs.house.gov/subcommittees.asp?committee=8', 'Subcommittee on the Western Hemisphere', 'HSFA_whe')) + '\n'

    return member_string

def comm_energygw():
    page = urllib2.urlopen("http://globalwarming.house.gov/about?id=0002")
    soup = BeautifulSoup(page)
    members = ['"House Select Committee on Energy Independence and Global Warming"', '"HSGW"']
    member_div = soup.findAll('div', 'pad')
    for lst in member_div:
        for a in lst.findAll('a'):
            if len(a.contents) < 1:
                continue
            name = str(a.contents[0])
            # Ignore links that do not refer to a member of congress
            if name.find('Congress') == -1:
                continue
            # Filter title and state
            name = name.replace('Congressman ', '').replace('Congresswoman ', '')
            name = name[:name.find(' of ')]
            members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def comm_permanentintel():
    page = urllib2.urlopen("http://intelligence.house.gov/MemberList.aspx")
    soup = BeautifulSoup(page)
    members = ['"House Permanent Select Committee on Intelligence"', '"HSIG"']
    member_div = soup.find('table', cellpadding='1')
    for a in member_div.findAll('a'):
        if len(a.contents) < 1:
            continue
        name = str(a.contents[0])
        commapos = name.find(',')
        if commapos != -1:
            name = name[:commapos]
        members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def comm_rules():
    title = 'House Committee on Rules'
    def extract_names(tag, name, shortname):
        full_name = title
        if name != '':
            full_name += '/' + name
        members = ['"' + full_name + '"', '"' + shortname + '"']
        member_container = tag
        for a in member_container.findAll('a'):
            name = ''
            font_tag = a.find('font')
            if font_tag != None:
                name = font_tag.contents[0]
            else:
                name = str(a.contents[0])
            
            name = name.replace('\n', '').replace('\r', '').replace('         ', '')
            name = name.replace('Chairwoman ', '').replace('Chairman ', '')
            name = name.replace(',', '')
            commapos = name.find('<')
            if commapos != -1:
                name = name[:commapos]
            name = name.rstrip()
            if name == '':
                continue
            members.append('"' + name + '"')
        return members

    member_string = ''
    page = urllib2.urlopen("http://www.rules.house.gov/rules_members.htm")
    soup = BeautifulSoup(page)
    member_container = soup.find('table', cellspacing='4')
    members = extract_names(member_container, '', 'HSRU')
    member_string += ', '.join(members) + '\n'

    subcommittees = soup.findAll('table', width='100%', border='0')

    # Subcommittee on Legislative and Budget Process
    member_div = subcommittees[0]
    members = extract_names(member_container, 'Subcommittee on Legislative and Budget Process', 'HSRU_lbp')
    member_string += ', '.join(members) + '\n'

    # Subcommittee on Organization of the House
    member_container = subcommittees[1]
    members = extract_names(member_container, 'Subcommittee on Rules and Organization of the House', 'HSRU_roh')
    member_string += ', '.join(members) + '\n'

    return member_string

# TODO: Committee on the Judiciary
# - First names are not available
# - html is ugly

def comm_veterans():
    title = 'House Committee on Veterans\' Affairs'
    def extract_names(url, name, shortname):
        full_name = title
        if name != '':
            full_name += '/' + name
        members = ['"' + full_name + '"', '"' + shortname + '"']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_tbody = soup.find('tbody')
        for a in member_tbody.findAll('a'):
            name = str(a.contents[0])
            statepos = name.find(' (')
            if statepos != -1:
                name = name[:statepos]
                members.append('"' + name + '"')
        return members

    member_string = ''
    
    member_string += ', '.join(extract_names('http://veterans.house.gov/about/members.shtml', '', 'HSVR')) + '\n'

    member_string += ', '.join(extract_names('http://veterans.house.gov/disability/', 'Subcommittee on Disability Assistance and Memorial', 'HSVR_dam')) + '\n'

    member_string += ', '.join(extract_names('http://veterans.house.gov/economic/', 'Subcommittee on Economic Opportunity', 'HSVR_eop')) + '\n'

    member_string += ', '.join(extract_names('http://veterans.house.gov/health/', 'Subcommittee on Health', 'HSVR_hea')) + '\n'

    member_string += ', '.join(extract_names('http://veterans.house.gov/oversight/', 'Subcommittee on Oversight and Investigations', 'HSVR_osi')) + '\n'

    return member_string

def comm_waysandmeans():
    page = urllib2.urlopen('http://waysandmeans.house.gov/singlepages.aspx?newsid=10462')
    soup = BeautifulSoup(page)
    members = ['"House Committee on Ways and Means"', '"HSWM"']
    member_container = soup.find('tbody')
    for tag in member_container.findAll('font', color='#0000ff'):
        name = tag.contents[0]
        members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def subcomm_waysandmeans():
    title = 'House Committee on Ways and Means'
    def extract_names(url, name, shortname):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        full_name = title
        if name != '':
            full_name += '/' + name
        members = ['"' + full_name + '"', '"' + shortname + '"']
        member_container = soup.find('tbody')
        for tag in member_container.findAll('a'):
            name = str(tag.contents[0])
            members.append('"' + name.strip() + '"')

        return members

    member_string = ''

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/health', 'Subcommittee on Health', 'HSWM_hea')) + '\n'

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/incomeSecurity', 'Subcommittee on Income Security and Family Support', 'HSWM_fam')) + '\n'

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/oversight', 'Subcommittee on Oversight', 'HSWM_osi')) + '\n'

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/selectrevenue', 'Subcommittee on Select Revenue Measures', 'HSWM_srm')) + '\n'

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/socialsecurity', 'Subcommittee on Social Security', 'HSWM_ssc')) + '\n'

    member_string += ', '.join(extract_names('http://waysandmeans.house.gov/subcommittees/Default.aspx/trade', 'Subcommittee on Trade', 'HSWM_trd')) + '\n'

    return member_string

def comm_transportation():
    page = urllib2.urlopen('http://transportation.house.gov/about.aspx')
    soup = BeautifulSoup(page)
    members = ['"House Committee on Transportation and Infrastructure"', '"HSPW"']
    # Pull the chairperson first
    name = str(soup.findAll('p', align='center')[1].find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.find('tbody')
    for tag in member_container.findAll('li'):
        name = tag.contents[0]
        commapos = name.find(',')
        name = name[:commapos].replace('"', '\\"')
        if name == 'Vacancy':
            continue
        members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def subcomm_transportation():
    member_string = ''
    title = 'House Committee on Transportation and Infrastructure'

    # Subcommittee on Aviation
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/aviation_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Aviation"', '"HSPW_air"']
    # Pull the chairperson first
    name = str(soup.find('p', align='center').find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.find('tbody')
    for tag in member_container.findAll('td'):
        subtag = str(tag.contents[1])
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Coast Guard and Maritime Transportation
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/maritime_transportation_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Coast Guard and Maritime Transportation"', '"HSPW_sea"']
    # Pull the chairperson first
    name = str(soup.findAll('p', align='left')[1].find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.findAll('td', valign='top')
    for tag in member_container:
        subtag = str(tag.find('p'))
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Economic Development, Public Buildings, and
    # Emergency Management
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/economic_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Economic Development, Public Buildings, and Emergency Management"', '"HSPW_ecn"']
    # Pull the chairperson first
    name = str(soup.find('div', id='content').find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.findAll('td', valign='top')
    for tag in member_container:
        subtag = str(tag.find('p'))
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            name = name.replace('"', '\\"')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Highways and Transit
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/highways_transit_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Highways and Transit"', '"HSPW_hwy"']
    # Pull the chairperson first
    name = str(soup.find('p', align='center').find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.findAll('td', valign='top')
    for tag in member_container:
        subtag = str(tag.find('p'))
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            name = name.replace('"', '\\"')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Railroads, Pipelines, and Hazardous Materials
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/railroads_pipelines_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Railroads, Pipelines, and Hazardous Materials"', '"HSPW_rrd"']
    # Pull the chairperson first
    name = str(soup.find('p', align='center').find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.findAll('td', valign='top')
    for tag in member_container:
        subtag = str(tag.find('p'))
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            name = name.replace('"', '\\"')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Water Resources and Environment
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/WaterResources_members.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Water Resources and Environment"', '"HSPW_wre"']
    # Pull the chairperson first
    name = str(soup.find('p', align='center').find('strong').contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    member_container = soup.findAll('td', valign='top')
    for tag in member_container:
        subtag = str(tag.find('p'))
        for protoname in subtag.split('<br />'):
            commapos = protoname.find(',')
            if commapos == -1:
                continue
            name = protoname[:commapos]
            name = name.replace('<em>', '').replace('</em>', '')
            name = name.replace('<br />', '').replace('<p>', '')
            name = name.replace('"', '\\"')
            members.append('"' + name.strip() + '"')

    member_string += ', '.join(members) + '\n'

    return member_string

def comm_smallbusiness():
    page = urllib2.urlopen('http://www.house.gov/smbiz/democrats/members.htm')
    soup = BeautifulSoup(page)
    members = ['"House Committee on Small Business"', '"HSSM"']

    member_container = soup.findAll('p', 'style8')
    for container in member_container:
        for protoname in container.findAll('a'):
            name = protoname.contents[0]
            name = name.replace('Chairman', '').replace('Chairwoman', '')
            name = name.replace('Congressman', '').replace('Congresswoman', '')
            name = name.replace('Ranking Member', '')
            of_pos = name.find(' of ')
            name = name[:of_pos]
            name = name.strip()
            members.append('"' + name + '"')
    return ', '.join(members) + '\n'

def subcomm_smallbusiness():
    title = 'House Committee on Small Business'
    def extract_names(container, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']

        for item in combined:
            name = str(item).strip()
            if name == '<br />':
                continue

            name = name.replace('Congressman', '').replace('Congresswoman', '')
            comma_pos = name.find(',')
            if comma_pos != -1:
                name = name[:comma_pos]

            members.append('"' + name.strip() + '"')

        return members

    page = urllib2.urlopen('http://www.house.gov/smbiz/democrats/subcommittees.htm')
    soup = BeautifulSoup(page)


    member_string = ''
    member_container = soup.findAll('div', align='center')[5]

    paras = member_container.findAll('p', align='left')
    
    # Finance and Tax
    combined = paras[0].contents + paras[1].contents
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Finance and Tax', 'HSSM_tax')) + '\n'

    # Contracting and Technology
    combined = paras[3].contents + paras[4].contents
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Contracting and Technology', 'HSSM_tec')) + '\n'

    # Regulations and Healthcare
    combined = paras[6].contents + paras[7].contents
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Regulations and Healthcare', 'HSSM_rhc')) + '\n'

    # Rural Development, Entrepreneurship and Trade
    combined = paras[9].contents + paras[10].contents
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Rural Development, Entrepreneurship and Trade', 'HSSM_ret')) + '\n'

    # Investigations and Oversight
    combined = paras[12].contents + paras[13].contents
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Investigations and Oversight', 'HSSM_osi')) + '\n'

    return member_string

# TODO: Need to replace 'Mr.' and 'Ms.' with appropriate first names in
#       subcommittee lists.
def comm_science():
    title = 'House Committee on Science and Technology'
    def extract_names(container, name, shortname):
        full_title = '"' + title
        if name != '':
            full_title += '/' + name + '"'
        members = [full_title, '"' + shortname + '"']
        for protoname in container.findAll('a'):
            name = protoname.contents[0]
            name = name.replace('\n', '').replace('\r', '')
            name = name.replace('                     ', '')
            # Skip the list of resolutions
            if name.find('Res.') != -1:
                continue
            name = name.rstrip(' ')
            members.append('"' + name + '"')

        return members

    page = urllib2.urlopen('http://science.house.gov/about/members.shtml')
    soup = BeautifulSoup(page)

    # Remove HTML comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    member_container = soup.findAll('table', width='100%', align='center')

    member_string = ''
    member_string += ', '.join(extract_names(member_container[0], '', 'HSSY')) + '\n'

    member_string += ', '.join(extract_names(BeautifulSoup(''.join(str(member_container[1].contents) + str(member_container[2].contents))), 'Subcommittee on Technology and Innovation', 'HSSY_tec')) + '\n'

    member_string += ', '.join(extract_names(BeautifulSoup(''.join(str(member_container[3].contents) + str(member_container[4].contents))), 'Subcommittee on Energy and Environment', 'HSSY_ene')) + '\n'

    member_string += ', '.join(extract_names(BeautifulSoup(''.join(str(member_container[5].contents) + str(member_container[6].contents))), 'Subcommittee on Investigations and Oversight', 'HSSY_osi')) + '\n'

    member_string += ', '.join(extract_names(BeautifulSoup(''.join(str(member_container[7].contents) + str(member_container[8].contents))), 'Subcommittee on Research and Science Education', 'HSSY_res')) + '\n'

    member_string += ', '.join(extract_names(BeautifulSoup(''.join(str(member_container[9].contents) + str(member_container[10].contents))), 'Subcommittee on Space and Aeronautics', 'HSSY_spc')) + '\n'

    return member_string

def comm_hsc():
    members = ['"House Committee on Homeland Security"', '"HSHM"']
    # Democrat site
    page = urllib2.urlopen('http://hsc.house.gov/about/members.asp')
    soup = BeautifulSoup(page)

    member_container = soup.find('div', id='middlecolumn')
    for protoname in member_container.findAll('a')[6:]:
        if len(protoname.contents) == 0:
            continue
        name = protoname.contents[0]
        print name
        members.append('"' + name + '"')

    # Republican site
    page = urllib2.urlopen('http://chs-republicans.house.gov/committee.shtml')
    soup = BeautifulSoup(page)

    member_container = soup.find('table', width='542')
    for protoname in member_container.findAll('a'):
        members.append('"' + protoname.contents[0] + '"')

    return ', '.join(members) + '\n'

def subcomm_hsc():
    title = 'House Committee on Homeland Security'
    def extract_names(url, name, shortname):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        full_title = '"' + title
        if name != '':
            full_title += '/' + name
        full_title += '"'
        members = [full_title, '"' + shortname + '"']
        para = soup.find('p')

        # Chairperson first
        strong = para.findAll('strong')[1]
        chairperson = str(strong.contents[0])
        comma_pos = chairperson.find(',')
        chairperson = chairperson[:comma_pos]
        members.append('"' + chairperson + '"')

        for protoname in para.findAll('td')[3:]:
            name = str(protoname.contents[0]).rstrip(' ')
            if name == 'Vacancy' or name == 'vacancy' or name == '':
                continue

            comma_pos = name.find(',')
            if comma_pos != -1:
                name = name[:comma_pos]
            members.append('"' + name + '"')

        return members

    member_string = ''

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=8', 'Subcommittee on Border, Maritime and Global Counterterrorism', 'HSHM_bor')) + '\n'

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=11', 'Subcommittee on Intelligence, Information Sharing and Terrorism Risk Assessment', 'HSHM_int')) + '\n'

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=10', 'Subcommittee on Transportation Security and Infrastructure Protection', 'HSHM_tra')) + '\n'

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=12', 'Subcommittee on Emerging Threats, Cybersecurity, and Science and Technology', 'HSHM_cyb')) + '\n'

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=9', 'Subcommittee on Emergency Communications, Preparedness, and Response', 'HSHM_cpr')) + '\n'

    member_string += ', '.join(extract_names('http://hsc.house.gov/about/subcommittees.asp?subcommittee=13', 'Subcommittee on Management, Investigations, and Oversight', 'HSHM_osm')) + '\n'

    return member_string

def comm_cha():
    title = 'House Committee on House Administration'

    def extract_names(url, name, shortname):
        full_title = '"' + title
        if name != '':
            full_title += '/' + name
        full_title += '"'
        members = [full_title, shortname]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_container = soup.find('table', width='446')
        for a in member_container.findAll('a'):
            # Ignore linked images and other objects
            if type(a.contents[0]) == Tag:
                continue
            members.append('"' + a.contents[0] + '"')
        return members

    member_string = ''

    member_string += ', '.join(extract_names('http://cha.house.gov/committee_membership.aspx', '', 'HSHA')) + '\n'

    member_string += ', '.join(extract_names('http://cha.house.gov/elections.aspx', 'Subcommittee on Elections', 'HSHA_ele')) + '\n'

    member_string += ', '.join(extract_names('http://cha.house.gov/security.aspx', 'Subcommittee on Capitol Security', 'HSHA_csc')) + '\n'
    
    return member_string

def comm_natres():
    title = 'House Committee on Natural Resources'
    member_string = ''
    members = ['"' + title + '"', '"HSII"']
    page = urllib2.urlopen('http://resourcescommittee.house.gov/index.php?option=com_content&task=view&id=96&Itemid=27')
    soup = BeautifulSoup(page)

    member_container = soup.findAll('div', align='center')[1]

    # Chairperson first
    strong = member_container.find('strong')
    name = str(strong.contents[0])
    comma_pos = name.find(',')
    members.append('"' + name[4:comma_pos] + '"')

    # Main committee
    member_container = member_container.find('table', border='0', cellpadding='0')
    rows = member_container.findAll('td')
    name_list = []
    for row in rows:
        names = str(row.contents[0])
        names = names.replace('\r', '').replace('\n', '').replace('\t', '')
        names = names.replace('<em>', '').replace('</em>', '')
        names = names.split('<br />')
        cleaned_names = []
        for n in names:
            comma_pos = n.find(',')
            if comma_pos != -1:
                n = n[:comma_pos]
            cleaned_names.append(n)
        name_list += cleaned_names

    members += name_list
    member_string += ', '.join(members) + '\n'

    # Energy and Mineral Resources
    members = ['"' + title + '/Subcommittee on Energy and Mineral Resources"', '"HSII_ene"']
    member_container = soup.findAll('div', align='center')[2]
    strong = member_container.findAll('strong')[2]
    name = str(strong.contents[0])
    comma_pos = name.find(',')
    members.append('"' + name[4:comma_pos] + '"')

    member_container = soup.findAll('div', align='center')[3]
    member_container = member_container.find('table', border='0')
    rows = member_container.findAll('td', align='left')
    name_list = []
    for row in rows:
        names = ''.join(str(row.contents))
        names = names.replace('\r', '').replace('\n', '').replace('\t', '')
        names = names.replace('<em>', '').replace('</em>', '')
        names = names.replace('[u\'\\n\', ', '')
        names = names.replace('<div align="left">', '').replace('</div>', '')
        names = names.split('<br />')
        cleaned_names = []
        for n in names:
            comma_pos = n.find(',')
            if comma_pos != -1:
                n = n[:comma_pos]
            cleaned_names.append('"' + n + '"')
        name_list += cleaned_names

    members += name_list
    member_string += ', '.join(members) + '\n'

    # Subcommittee on Insular Affairs, Oceans and Wildlife
    members = ['"' + title + '/Subcommittee on Insular Affairs, Oceans and Wildlife"', '"HSII_iow"']
    member_container = soup.findAll('p', align='center')[6]
    strong = member_container.findAll('strong')[2]
    name = str(strong.contents[0])
    comma_pos = name.find(',')
    members.append('"' + name[5:comma_pos] + '"')

    # Ranking member
    em = member_container.find('em')
    name = str(em.contents[0])
    comma_pos = name.find(',')
    name = name[4:comma_pos]
    members.append('"' + name + '"')

    member_container = soup.findAll('div', align='center')[4]
    member_container = member_container.find('table', border='0')
    rows = member_container.findAll('td', align='left')
    name_list = []
    for row in rows:
        names = str(row.contents[0])
        names = names.replace('\r', '').replace('\n', '').replace('\t', '')
        names = names.replace('<em>', '').replace('</em>', '')
        names = names.replace('[u\'\\n\', ', '')
        names = names.replace('<div align="left">', '').replace('</div>', '')
        names = names.split('<br />')
        cleaned_names = []
        for n in names:
            comma_pos = n.find(',')
            if comma_pos != -1:
                n = n[:comma_pos]
            cleaned_names.append('"' + n + '"')
        name_list += cleaned_names

    members += name_list
    member_string += ', '.join(members) + '\n'

    # Subcommittee on National Parks, Forests and Public Lands
    members = ['"' + title + '/Subcommittee on National Parks, Forests and Public Lands"', '"HSII_nps"']
    member_container = soup.findAll('div', align='center')[5]
    strong = member_container.findAll('strong')[1]
    name = str(strong.contents[0])
    comma_pos = name.find(',')
    members.append('"' + name[5:comma_pos] + '"')

    # Ranking member
    em = member_container.find('em')
    name = str(em.contents[0])
    comma_pos = name.find(',')
    name = name[4:comma_pos]
    members.append('"' + name + '"')

    member_container = soup.findAll('div', align='center')[6]
    member_container = member_container.find('table', border='0')
    rows = member_container.findAll('td', align='left')
    name_list = []
    for row in rows:
        names = str(row.contents)
        names = names.replace('\r', '').replace('\n', '').replace('\t', '')
        names = names.replace('\\r', '').replace('\\n', '').replace('\\t', '')
        names = names.replace('<em>', '').replace('</em>', '')
        names = names.replace('u\'', '').replace('[', '')
        names = names.replace('<div align="left">', '').replace('</div>', '')
        names = names.split('<br />')
        cleaned_names = []
        for n in names:
            if n[0:2] == ', ':
                n = n[2:]
            comma_pos = n.find(',')
            if comma_pos != -1:
                n = n[:comma_pos]
            cleaned_names.append('"' + n + '"')
        name_list += cleaned_names

    members += name_list
    member_string += ', '.join(members) + '\n'

    # Subcommittee on Water and Power
    members = ['"' + title + '/Subcommittee on Water and Power"', '"HSII_wat"']
    member_container = soup.findAll('div', align='center')[6]

    strong = member_container.findAll('strong')[1]
    name = str(strong.contents[0])
    comma_pos = name.find(',')
    members.append('"' + name[5:comma_pos] + '"')

    # Ranking member
    em = member_container.findAll('em')[1]
    name = str(em.contents[0])
    comma_pos = name.find(',')
    name = name[4:comma_pos]
    members.append('"' + name + '"')

    table = member_container.findAll('table', border='0')[1]
    
    rows = table.findAll('td', align='left')
    name_list = []
    for row in rows:
        names = ''.join(str(row.contents))
        names = names.replace('\\r', '').replace('\\n', '').replace('\\t', '')
        names = names.replace('\r', '').replace('\n', '').replace('\t', '')
        names = names.replace('<em>', '').replace('</em>', '')
        names = names.replace('u\'', '').replace('[', '')
        names = names.replace('<div align="left">', '').replace('</div>', '')
        names = names.split('<br />')
        cleaned_names = []
        for n in names:
            if n[0:2] == ', ':
                n = n[2:]
            comma_pos = n.find(',')
            if comma_pos != -1:
                n = n[:comma_pos]
            cleaned_names.append('"' + n + '"')
        name_list += cleaned_names

    members += name_list
    member_string += ', '.join(members) + '\n'

    return member_string

def comm_oversight():
    title = 'House Committee on Oversight and Government Reform'
    members = ['"' + title + '"', '"HSGO"']
    page = urllib2.urlopen('http://oversight.house.gov/index.php?option=com_content&view=article&id=2229:membership&catid=37&Itemid=20')
    soup = BeautifulSoup(page)

    member_container = soup.find('div', id='members')
    lists = member_container.findAll('li')

    for lst in lists:
        link_tag = lst.find('a')
        name = ''
        if link_tag == None:
            name = lst.contents[0]
        else:
            name = link_tag.contents[0]

        name = name.replace('Chairman, ', '')
        name = name.replace('Rep. ', '')
        comma_pos = name.find(',')
        if comma_pos != -1:
            name = name[:comma_pos]
        name = name.replace('"', '\\"')
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_oversight():
    title = 'House Committee on Oversight and Government Reform'
    
    def extract_names(container, name, shortname):
        full_title = '"' + title
        if name != '':
            full_title += '/' + name
        full_title += '"'
        members = [full_title, '"' + shortname + '"']

        divs = container.findAll('div')
        
        for div in divs:
            inner_container = div
            para = div.find('p')
            if para != None:
                inner_container = para
            names = []
            for n in inner_container:
                name = str(n)
                name = name.replace('<strong>', '').replace('</strong>', '')
                name = name.replace(', Chairman', '')
                name = name.replace('u\'', '').replace('\\r', '')
                name = name.replace('\'', '')
                name = name.replace('\\n', '').replace('[', '').replace(']', '')
                if name == '<br />' or name == ' ':
                    continue
                elif name == 'Majority' or name == 'Minority':
                    continue
                if name[0:2] == ', ':
                    name = name[3:]
                comma_pos = name.find(',')
                if comma_pos > 1:
                    name = name[:comma_pos]
                members.append('"' + name.strip(' ') + '"')

        return members

    page = urllib2.urlopen('http://oversight.house.gov/index.php?option=com_content&view=article&id=4445&Itemid=19')
    soup = BeautifulSoup(page)

    member_string = ''

    table = soup.findAll('table', 'contentpaneopen')[1]
    divs = table.findAll('div')

    combined = BeautifulSoup(str(divs[1]) + str(divs[2]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Domestic Policy', 'HSGO_dom')) + '\n'

    combined = BeautifulSoup(str(divs[4]) + str(divs[5]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Federal Workforce, Postal Services, and the District of Columbia', 'HSGO_fed')) + '\n'

    combined = BeautifulSoup(str(divs[7]) + str(divs[8]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Government Management, Organization, and Procurement', 'HSGO_gpo')) + '\n'

    combined = BeautifulSoup(str(divs[10]) + str(divs[11]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Information Policy, Census, and National Archives', 'HSGO_icn')) + '\n'

    combined = BeautifulSoup(str(divs[12]) + '<div>' + str(table.find('td').contents[-19:]) + '</div>')
    member_string += ', '.join(extract_names(combined, 'Subcommittee on National Security and Foreign Affairs', 'HSGO_nsc')) + '\n'

    return member_string

def comm_homelandsecurity():
    title = 'Senate Committee on Homeland Security and Governmental Affairs'
    members = ['"' + title + '"', '"SSGA"']
    page = urllib2.urlopen('http://hsgac.senate.gov/public/index.cfm?FuseAction=AboutCommittee.Membership')
    soup = BeautifulSoup(page)

    member_container = soup.find('table', border='0', cellspacing='0')
    tds = member_container.findAll('td', 'vblack10')

    for member in tds:
        a = member.find('a')
        if a == None:
            continue
        spans = a.findAll('span')
        name = str(a.contents[0])
        for span in spans:
            if len(span.contents) > 0:
                name = str(span.contents[0])
        if name == '<br />':
            continue
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def comm_help():
    members = ['"Senate Committee on Health, Education, Labor and Pensions"', '"SSHR"']
    page = urllib2.urlopen('http://help.senate.gov/about/')
    soup = BeautifulSoup(page)

    member_string = ''
    member_container = soup.find('div', id='member-list')
    a_lst = member_container.findAll('a')
    for a in a_lst:
        member = str(a.contents[0]).strip()
        paren_pos = member.find(' (') 
        members.append('"' + member[:paren_pos] + '"')
    member_string += ', '.join(members) + '\n'

    subcomms = soup.find('div', id='subcommittees')
    subcomms_ul = subcomms.findAll('ul')

    members = ['"Subcommittee on Children and Families"', '"SSHR_cfm"']
    member_container = subcomms_ul[0]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_container = subcomms_ul[1]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"Subcommittee on Employment and Workplace Safety"', '"SSHR_cfm"']
    member_container = subcomms_ul[2]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_container = subcomms_ul[3]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"Subcommittee on Retirement and Aging"', '"SSHR_age"']
    member_container = subcomms_ul[4]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_container = subcomms_ul[5]
    for a in member_container.findAll('a'):
        member = a.contents[0]
        paren_pos = member.find(' (')
        members.append('"' + member[:paren_pos] + '"')
    member_string += ', '.join(members) + '\n'

    return member_string

def comm_foreign():
    members = ['"Senate Committee on Foreign Relations"', '"SSFR"']
    page = urllib2.urlopen('http://foreign.senate.gov')
    soup = BeautifulSoup(page)

    member_container = soup.find('div', id='democrats')
    for m in member_container.findAll('div'):
        members.append('"' + m.contents[0] + '"')
    member_container = soup.find('div', id='republicans')
    for m in member_container.findAll('div'):
        members.append('"' + m.contents[0] + '"')

    return ', '.join(members) + '\n'

def subcomm_foreign():
    member_string = ''
    title = 'Senate Committee on Foreign Relations'
    page = urllib2.urlopen('http://foreign.senate.gov/about/')
    soup = BeautifulSoup(page)
    # NOTE: subcomms seems to pick up the contents of subcomms_last as well
    subcomms = soup.findAll('ul', 'side-column-2')
    subcomms_last = soup.findAll('ul', 'side-column-2 last')
    members = ['"' + title + '/Subcommittee on Western Hemisphere, Peace Corps, and Global Narcotics Affairs"', '"SSFR_whe"']
    for m in subcomms[0].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[0].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on African Affairs"', '"SSFR_afr"']
    for m in subcomms[2].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[1].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on International Operations and Organizations, Human Rights, Democracy, and Global Women\'s Issues"', '"SSFR_hrd"']
    for m in subcomms[4].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[2].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on International Development and Foreign Assistance, Economic Affairs and International Development Protection"', '"SSFR_aid"']
    for m in subcomms[6].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[3].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on Near East and South and Central Asian Affairs"', '"SSFR_asi"']
    for m in subcomms[8].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[4].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on East Asian and Pacific Affairs"', '"SSFR_pac"']
    for m in subcomms[10].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[5].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    members = ['"' + title + '/Subcommittee on European Affairs"', '"SSFR_eur"']
    for m in subcomms[12].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    for m in subcomms_last[6].findAll('li'):
        if len(m.contents) > 0:
            name = m.contents[0]
            if name[-2:] == ', ':
                name = name[:len(name)-2]
            members.append('"' + name + '"')
    member_string += ', '.join(members) + '\n'

    return member_string

def comm_senate_finance():
    members = ['"Senate Committee on Finance"', '"SSFI"']
    page = urllib2.urlopen('http://finance.senate.gov/about/')
    soup = BeautifulSoup(page)

    member_containers = soup.findAll('div', 'column-3')
    for m in member_containers:
        a = m.find('a')
        name = str(a.contents[2])
        name = name.replace('&nbsp;', ' ').replace('&raquo;', '')
        name = name.lstrip().rstrip()
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_finance():
    member_string = ''
    title = 'Senate Committee on Finance'
    page = urllib2.urlopen('http://finance.senate.gov/about/subcommittees/')
    soup = BeautifulSoup(page)

    def parse_members(div_dem, div_rep, name, shortname):
        members = [name, shortname]
        para = [str(x) for x in div_dem]
        strpara = ''.join(para)
        strpara = strpara.replace('<p>', '').replace('</p>', '')
        memberlist = strpara.split('<br />')
        for m in memberlist:
            if m.find('<strong>') == -1:
                commapos = m.find(',')
                name = m[:commapos].lstrip().rstrip()
                if name != '':
                    members.append('"' + name + '"')

        para = [str(x) for x in div_rep]
        strpara = ''.join(para)
        strpara = strpara.replace('<p>', '').replace('</p>', '')
        memberlist = strpara.split('<br />')
        for m in memberlist:
            if m.find('<strong>') == -1:
                commapos = m.find(',')
                name = m[:commapos].lstrip().rstrip()
                if name != '':
                    members.append('"' + name + '"')

        return ', '.join(members) + '\n'

    subcomms = soup.findAll('div', 'column-2')

    member_string += parse_members(subcomms[0].contents, subcomms[1].contents, '"' + title + '/Subcommittee on Health Care"', '"SSFI_hcr"')

    member_string += parse_members(subcomms[2].contents, subcomms[3].contents, '"' + title + '/Subcommittee on Taxation, IRS Oversight, and Long-Term Growth"', '"SSFI_tax"')

    member_string += parse_members(subcomms[4].contents, subcomms[5].contents, '"' + title + '/Subcommittee on Energy, Natural Resources, and Infrastructure"', '"SSFI_ene"')

    member_string += parse_members(subcomms[6].contents, subcomms[7].contents, '"' + title + '/Subcommittee on Social Security, Pensions, and Family Policy"', '"SSFI_ssp"')

    member_string += parse_members(subcomms[8].contents, subcomms[9].contents, '"' + title + '/Subcommittee on International Trade, Customs, and Global Competitiveness"', '"SSFI_tra"')

    return member_string

def comm_senate_ethics():
    members = ['"Senate Select Committee on Ethics"', '"SLET"']
    page = urllib2.urlopen('http://ethics.senate.gov/')
    soup = BeautifulSoup(page)

    # Democrats
    member_containers = soup.findAll('font', size='1', face='Verdana, Arial, Helvetica, sans-serif')
    for a in member_containers[9].findAll('a'):
        name = str(a.contents[0])
        name = name.lstrip().rstrip()
        members.append('"' + name + '"')
    # Republicans
    for a in member_containers[10].findAll('a'):
        name = str(a.contents[0])
        name = name.lstrip().rstrip()
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

# Senate Committee on Environment and Public Works
# TODO

def comm_senate_energy():
    members = ['"Senate Committee on Energy and Natural Resources"', '"SSEG"']
    page = urllib2.urlopen('http://energy.senate.gov/public/index.cfm?FuseAction=About.Members')
    soup = BeautifulSoup(page)

    member_containers = soup.findAll('td', 'vblack11')[4:]

    for m in member_containers:
        a = m.find('a')
        name = str(a.contents[0])
        name = name.replace('Chairman ', '')
        name = name.replace(' (I)', '')
        name = name.lstrip().rstrip()
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

#tasks = [comm_agriculture, subcomm_agriculture, comm_appropriations, subcomm_appropriations, comm_armedservices, subcomm_armedservices, comm_budget, comm_edlabor, subcomm_edlabor, comm_energycommerce, subcomm_energycommerce, comm_financialservices, subcomm_financialservices, comm_foreignaffairs, subcomm_foreignaffairs, comm_energygw, comm_permanentintel, comm_rules, comm_veterans, comm_waysandmeans, subcomm_waysandmeans, comm_transportation, subcomm_transportation, comm_smallbusiness, subcomm_smallbusiness, comm_science, subcomm_hsc, comm_cha, comm_natres, comm_oversight, subcomm_oversight, comm_homelandsecurity, comm_help, comm_foreign, subcomm_foreign, comm_senate_finance, subcomm_senate_finance, comm_senate_ethics, comm_senate_energy]

for t in tasks:
    print t(),
