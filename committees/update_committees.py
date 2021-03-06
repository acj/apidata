''' Script for gathering lists of (sub-)committee members'''

# TODO:
# * Keep track of pages that can't be parsed (i.e., that may have changed) and
#   don't include them in the data; email the list to someone
# * What if the page times out?

import re
import urllib2
from BeautifulSoup import BeautifulSoup, Comment, Tag

def fetch_senate_members_list():
    url = 'http://en.wikipedia.org/wiki/List_of_current_United_States_Senators'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent' : user_agent}
    req = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)
    members = {}
    table = soup.find('table', 'sortable wikitable')
    for span in table.findAll('span', 'fn'):
        name = span.find('a').contents[0]
        comma_pos = name.rfind(',')
        space_pos = None
        if comma_pos != -1:
            space_pos = name[:comma_pos].rfind(' ')
            members[name[space_pos:comma_pos]] = name
        else:
            space_pos = name.rfind(' ')
            members[name[space_pos:]] = name

    return members

senators = fetch_senate_members_list()

def comm_agriculture():
    members = ['"House Committee on Agriculture"', '"HSAG"']
    page = urllib2.urlopen("http://agriculture.house.gov/inside/members.html")
    soup = BeautifulSoup(page)
    memberlists = soup.findAll('ul', 'memberlist') # Second arg: class attr val
    for list in memberlists:
        for member in list.findAll('li'):
            href = member.find('a')
            name = href.contents[0]
            members.append('"' + name.rstrip(',') + '"')

    return ', '.join(members) + '\n'

def subcomm_agriculture():
    def parse_members(subcomm_name, shortname, url):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = ['"' + subcomm_name + '", "' + shortname + '"']
        memberlist = soup.find('div', id='twoCol')
        lst = memberlist.findAll('ul')
        for ul in lst:
            for li in ul.findAll('li'):
                a = li.find('a')
                name = a.contents[0]
                members.append('"' + name + '"')
        return members

    name_prefix = '"House Committee on Agriculture'
    page = urllib2.urlopen('http://agriculture.house.gov/singlepages.aspx?NewsID=3&LSBID=44')
    soup = BeautifulSoup(page)

    subcommittees = ''
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on Conservation, Credit, Energy, and Research', 'HSAG_ene', 'http://agriculture.house.gov/singlepages.aspx?NewsID=27&LSBID=44')) + '\n'
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on Department Operations, Oversight, Nutrition, and Forestry', 'HSAG_for', 'http://agriculture.house.gov/singlepages.aspx?NewsID=29&LSBID=44')) + '\n'
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on General Farm Commodities and Risk Management', 'HSAG_gfc', 'http://agriculture.house.gov/singlepages.aspx?NewsID=30&LSBID=44')) + '\n'
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on Horticulture and Organic Agriculture', 'HSAG_bzz', 'http://agriculture.house.gov/singlepages.aspx?NewsID=31&LSBID=44')) + '\n'
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on Livestock, Dairy, and Poultry', 'HSAG_ldp', 'http://agriculture.house.gov/singlepages.aspx?NewsID=32&LSBID=44')) + '\n'
    subcommittees += ', '.join(parse_members('House Committee on Agriculture/Subcommittee on Rural Development, Biotechnology, Specialty Crops, and Foreign Agriculture', 'HSAG_bio', 'http://agriculture.house.gov/singlepages.aspx?NewsID=33&LSBID=44')) + '\n'

    return subcommittees

def comm_appropriations():
    page = urllib2.urlopen("http://appropriations.house.gov/index.php?option=com_content&view=article&id=95&Itemid=138")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Appropriations"', '"HSAP"']
    memberlist = soup.find('table', cellpadding='10', border='0')
    for member in memberlist.findAll('a'):
        comma_idx = member.contents[0].find(',')
        name = member.contents[0][:comma_idx]
        members.append('"' + unicode(name).encode('utf-8') + '"')
        
    return ', '.join(members) + '\n'

def subcomm_appropriations():
    def parse_members(subcomm_name, shortname, url):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = ['"' + subcomm_name + '", "' + shortname + '"']
        memberlist = soup.find('div', 'moduletable_members')
        paras = memberlist.findAll('li')
        
        #names = str(paras[1]) + str(paras[3])
        #names = names.replace('Chair:', '')
        #re_names = re.compile(r'([A-Z][a-z]+.*) \([A-Z][A-Z]\).*')
        
        #for name in re_names.findall(names):
        #    members.append('"' + name + '"')

        for p in paras:
            name = p.contents[0]
            name = name.replace('Chair:', '')
            parenpos = name.find(' (')
            name = name[:parenpos]
            members.append('"' + unicode(name).encode('utf-8') + '"')
        return members
    
    subcommittees = ''
    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Agriculture, Rural Development, Food and Drug Administration, and Related Agencies', 'HSAP_fda', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=85&Itemid=16')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Commerce, Justice, Science, and Related Agencies', 'HSAP_com', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=84&Itemid=17')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Defense', 'HSAP_def', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=83&Itemid=18')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Energy and Water Development', 'HSAP_ene', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=82&Itemid=19')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Financial Services and General Government', 'HSAP_fin', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=15&Itemid=20')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Homeland Security', 'HSAP_dhs', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=88&Itemid=21')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Interior, Environment, and Related Agencies', 'HSAP_doi', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=86&Itemid=22')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Labor, Health and Human Services, Education, and Related Agencies', 'HSAP_hhs', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=87&Itemid=23')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Legislative Branch', 'HSAP_leg', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=79&Itemid=24')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Military Construction, Veterans Affairs, and Related Agencies, VA', 'HSAP_dva', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=78&Itemid=25')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on State, Foreign Operations, and Related Programs', 'HSAP_sta', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=77&Itemid=26')) + '\n'

    subcommittees += ', '.join(parse_members('House Committee on Appropriations/Subcommittee on Transportation, Housing and Urban Development, and Related Agencies', 'HSAP_hud', 'http://appropriations.house.gov/index.php?option=com_content&view=article&id=81&Itemid=27'))

    return subcommittees + '\n'

def comm_armedservices():
    page = urllib2.urlopen("http://armedservices.house.gov/list_of_members.shtml")
    soup = BeautifulSoup(page)
    members = ['"House Committee on Armed Services"', '"HSAS"']
    for memberlist in soup.findAll('td'):
        for p in memberlist.findAll('p'):
            member = p.find('a')
            if member == None:
                break
            atag = member.find('span')
            if atag == None:
                atag = member.find('font') # Correct for html error
                if atag == None:
                    break
            comma_idx = atag.contents[0].find(',')
            name = atag.contents[0][:comma_idx]
            name = name.replace('&ldquo;', '\\"').replace('&rdquo;', '\\"')
            members.append('"' + name + '"')
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
    for list in soup.findAll('ul', style='margin-top: 0px;'): 
        for lst in list.findAll('li'):
            a_tag = lst.find('a')
            if a_tag == None:
                continue
            name = a_tag.contents[0]
            name = name.replace('"', '\\"')
            name = name.replace(', Chairman', '')
            members.append('"' + unicode(name).encode('utf-8') + '"')
    return ', '.join(members) + '\n'

def subcomm_edlabor():
    page = urllib2.urlopen("http://edlabor.house.gov/about/members/")
    soup = BeautifulSoup(page)
    tables = soup.findAll('table', width='100%')
    member_string = ''

    def parse_names(subcomm, shortname, table):
        members = ['"' + 'House Committee on Education and Labor/' + subcomm + '"', '"' + shortname + '"']    
        names = table.findAll('td')
        for name in names:
            nametext = name.findAll(text=True)
            if nametext == None or len(nametext) == 0:
                continue
            n = nametext[0]
            n = n.replace('"', '\\"')
            if n.find('Democrats') != -1 or n.find('Republicans') != -1:
                continue
            if n.find('Ranking Member') != -1:
                continue
            if n == '<br />':
                continue
            n = n.replace(',', '').strip()
            members.append('"' + unicode(n).encode('utf-8') + '"')
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
        ptag = lst.find('p')
        if ptag == None:
            continue
        name = str(ptag.contents[0])
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
    page = urllib2.urlopen('http://financialservices.house.gov/singlepages.aspx?NewsID=397')
    soup = BeautifulSoup(page)
    members = ['"House Committee on on Financial Services"', '"HSBA"']
    lists = soup.find('tbody')
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
            re_names = re.compile(r'Rep.\s+([^\n]+) \([A-Z][A-Z]\).*')
            for c in tag.contents:
                for name in re_names.findall(str(c)):
                    names.append('"' + name + '"')
        return names

    page = urllib2.urlopen('http://financialservices.house.gov/singlepages.aspx?NewsID=400')
    soup = BeautifulSoup(page)
    member_string = ''
    members = ['"House Committee on Financial Services"', '"HSBA"']
    tables = soup.findAll('table')

    # Capital Markets, Insurance, and Government Sponsored Enterprises
    member_string += ', '.join(extract_names(tables[0], 'Subcommittee on Capital Markets, Insurance, and Government Sponsored Enterprises', 'HSBA_cap')) + '\n'

    # Financial Institutions and Consumer Credit
    member_string += ', '.join(extract_names(tables[1], 'Subcommittee on Financial Institutions and Consumer Credit', 'HSBA_fic')) + '\n'

    # Housing and Community Opportunity
    member_string += ', '.join(extract_names(tables[2], 'Subcommittee on Housing and Community Opportunity', 'HSBA_hco')) + '\n'

    # Domestic Monetary Policy and Technology
    member_string += ', '.join(extract_names(tables[3], 'Subcommittee on Domestic Monetary Policy and Technology', 'HSBA_dmp')) + '\n'

    # International Monetary Policy and Trade
    member_string += ', '.join(extract_names(tables[4], 'Subcommittee on International Monetary Policy and Trade', 'HSBA_imp')) + '\n'

    # Oversight and Investigations
    member_string += ', '.join(extract_names(tables[5], 'Subcommittee on Oversight and Investigations', 'HSBA_osi')) + '\n'

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
    page = urllib2.urlopen('http://transportation.house.gov/singlepages/singlepages.aspx/about')
    soup = BeautifulSoup(page)
    members = ['"House Committee on Transportation and Infrastructure"', '"HSPW"']
    # Pull the chairperson first
    name = str(soup.findAll('h5')[1].contents[0])
    members.append('"' + name[:name.find(',')] + '"')

    div = soup.find('div', 'aboutLeft')
    for tag in div.findAll('li'):
        name = tag.contents[0]
        commapos = name.find(',')
        name = name[:commapos].replace('"', '\\"')
        if name == 'Vacancy':
            continue
        members.append('"' + name + '"')

    div = soup.find('div', 'aboutRight')
    for tag in div.findAll('li'):
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
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/aviation.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Aviation"', '"HSPW_air"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

    member_container = soup.find('div', 'left')
    for tag in member_container.findAll('p'):
        protoname = tag.contents[0]
        commapos = protoname.find(',')
        if commapos == -1:
            continue
        name = protoname[:commapos]
        members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Coast Guard and Maritime Transportation
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/maritime_transportation.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Coast Guard and Maritime Transportation"', '"HSPW_sea"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

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
            members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Economic Development, Public Buildings, and
    # Emergency Management
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/economic.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Economic Development, Public Buildings, and Emergency Management"', '"HSPW_ecn"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

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
            members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Highways and Transit
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/highways_transit.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Highways and Transit"', '"HSPW_hwy"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

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
            members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Railroads, Pipelines, and Hazardous Materials
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/railroads_pipelines.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Railroads, Pipelines, and Hazardous Materials"', '"HSPW_rrd"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

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
            members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

    member_string += ', '.join(members) + '\n'

    # Subcommittee on Water Resources and Environment
    page = urllib2.urlopen('http://transportation.house.gov/subcommittees/WaterResources.aspx')
    soup = BeautifulSoup(page)
    members = ['"' + title + '/Subcommittee on Water Resources and Environment"', '"HSPW_wre"']
    # Pull the chairperson first
    name = str(soup.find('h3', 'boxName').contents[0])
    members.append('"' + name[:name.find(',')].replace('&quot;', '\\"') + '"')

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
            members.append('"' + name.strip().replace('&quot;', '\\"') + '"')

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

def comm_science():
    title = 'House Committee on Science and Technology'
    name_dict = {}
    def extract_names(container, name, shortname):
        build_dict = False
        if len(name_dict) == 0:
            build_dict = True
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
            # Change salutation to first name
            shortname = name
            if shortname[-4:] == ' Jr.':
                shortname = shortname[:-4]
            space_pos = shortname.rfind(' ') + 1
            lname = shortname[space_pos:].title()
            if name.find('Mr.') != -1 or name.find('Ms.') != -1 or name.find('Mrs.') != -1:
                name = name_dict[lname]
            if build_dict:
                name_dict[lname.title()] = name.title()

            members.append('"' + name.title() + '"')
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

        txt = str(container)
        names = txt.split('<br />')
        
        for n in names:
            name = str(n)
            name = name.replace('<strong>', '').replace('</strong>', '')
            name = name.replace(', Chairman', '')
            name = name.replace('u\'', '').replace('\\r', '')
            name = name.replace('\'', '')
            name = name.replace('\\n', '').replace('[', '').replace(']', '')
            name = name.replace('<p>Majority', '')
            name = name.replace('<p>Minority', '')
            name = name.replace('<p>', '').replace('</p>', '')
            name = name.replace('<div>', '').replace('</div>', '')
            if name == '<br />' or name == ' ' or name == '':
                continue
            elif name == 'Majority' or name == 'Minority':
                continue
            if name[0:2] == ', ':
                name = name[2:]
            comma_pos = name.find(',')
            if comma_pos > 1:
                name = name[:comma_pos]
            name = name.replace('"', '\\"')
            members.append('"' + name.strip(' ') + '"')

        return members

    page = urllib2.urlopen('http://oversight.house.gov/index.php?option=com_content&view=article&id=4445&Itemid=19')
    soup = BeautifulSoup(page)

    member_string = ''

    table = soup.findAll('table', 'contentpaneopen')[1]
    divs = table.findAll('div')
    paras = table.findAll('p')

    combined = BeautifulSoup(str(paras[1]) + '<br />' + str(divs[2]) + '<br />' + str(divs[3].contents[0]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Domestic Policy', 'HSGO_dom')) + '\n'

    combined = BeautifulSoup(str(paras[4]) + str(paras[5]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Federal Workforce, Postal Services, and the District of Columbia', 'HSGO_fed')) + '\n'

    combined = BeautifulSoup(str(paras[6]) + str(paras[7]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Government Management, Organization, and Procurement', 'HSGO_gpo')) + '\n'

    combined = BeautifulSoup(str(paras[8]) + str(paras[9]))
    member_string += ', '.join(extract_names(combined, 'Subcommittee on Information Policy, Census, and National Archives', 'HSGO_icn')) + '\n'

    combined = BeautifulSoup(str(paras[10]) + '<br /> <div>' + str(table.find('td').contents[-21:]) + '</div>')
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

    member_container = soup.find('div', id='majority-party')
    for m in member_container.findAll('div'):
        name = m.find('a').contents[0]
        name = name.replace('&nbsp;', ' ')
        members.append('"' + name + '"')
    member_container = soup.find('div', id='minority-party')
    for m in member_container.findAll('div'):
        name = m.find('a').contents[0]
        name = name.replace('&nbsp;', ' ')
        members.append('"' + name + '"')

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

def comm_senate_epw():
    members = ['"Senate Committee on Environment and Public Works"', '"SSEV"']
    page = urllib2.urlopen('http://epw.senate.gov/public/index.cfm?FuseAction=Members.Home')
    soup = BeautifulSoup(page)

    member_containers = soup.findAll('div', style='float:left; margin:20px 10px;')

    for m in member_containers:
        for a in m.findAll('a'):
            name = str(a.contents[0])
            name = name.lstrip().rstrip()
            members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_epw():
    member_string = ''
    title = 'Senate Committee on Environment and Public Works'

    def parse_members(url, name, shortname):
        members = [name, shortname]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        for td in soup.findAll('td', 'vblack11'):
            for a in td.findAll('a'):
                name = a.contents[0]
                if name == 'view':
                    continue
                members.append('"' + name + '"')

        return ', '.join(members) + '\n'

    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=1b27ff3f-4144-4365-b79c-dccdc4fc8824', '"' + title + '/Subcommittee on Children\'s Health"', '"SSEV_kid"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=d14466c0-a1b6-4c11-b87b-63700f7c3952', '"' + title + '/Subcommittee on Clean Air and Public Works"', '"SSEV_air"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=61c82caf-9dca-46c0-93b3-c7f602cc2e48', '"' + title + '/Subcommittee on Green Jobs and the New Economy"', '"SSEV_grn"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=b138d617-0770-4f37-bbef-f98847de0743', '"' + title + '/Subcommittee on Oversight"', '"SSEV_osi"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=01dbc44f-664e-493f-a883-13b89b0f5cc3', '"' + title + '/Subcommittee on Superfund, Toxics and Environmental Health"', '"SSEV_tox"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=de065f92-7614-40a9-8e6f-190182ac174f', '"' + title + '/Subcommittee on Transportation and Infrastructure"', '"SSEV_trn"')
    member_string += parse_members('http://epw.senate.gov/public/index.cfm?FuseAction=Subcommittees.Subcommittee&Subcommittee_id=47af17cb-6eeb-4fdc-b02d-0abb49d2eacb', '"' + title + '/Subcommittee on Water and Wildlife"', '"SSEV_wwf"')

    return member_string

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

def subcomm_senate_energy():
    member_string = ''
    title = 'Senate Committee on Energy and Natural Resources'

    def parse_members(url, name, shortname):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        members = [name, shortname]

        member_containers = soup.findAll('td', 'vblack8', width='50%')
        for c in member_containers:
            mlist = c.findAll(text=True)
            for m in mlist:
                name = m.lstrip().rstrip()
                name = name.replace(' (Chairman)', '')
                name = name.replace(' (I)', '')
                if name == 'Democratic Subcommittee Members':
                    continue
                elif name == 'Republican Subcommittee Members':
                    continue
                elif name != '':
                    members.append('"' + name + '"')

        return ', '.join(members) + '\n'

    member_string += parse_members('http://energy.senate.gov/public/index.cfm?FuseAction=About.Subcommittee&Subcommittee_id=ce189d44-42c8-4565-b062-b72410945a6b', '"' + title + '/Subcommittee on Energy"', '"SSEG_ene"')

    member_string += parse_members('http://energy.senate.gov/public/index.cfm?FuseAction=About.Subcommittee&Subcommittee_id=dadc9cc7-6579-4b44-bc3e-d560e0fbe1b9', '"' + title + '/Subcommittee on National Parks"', '"SSEG_nps"')

    member_string += parse_members('http://energy.senate.gov/public/index.cfm?FuseAction=About.Subcommittee&Subcommittee_id=f69427d2-cada-496b-8c3c-e53556c8e07b', '"' + title + '/Subcommittee on Public Lands and Forests"', '"SSEG_plf"')

    member_string += parse_members('http://energy.senate.gov/public/index.cfm?FuseAction=About.Subcommittee&Subcommittee_id=0ee9d4b8-cb23-42ee-ac0f-fc7c6897855f', '"' + title + '/Subcommittee on Water and Power"', '"SSEG_wpw"')

    return member_string

def comm_senate_ag():
    members = ['"Senate Committee on Agriculture, Nutrition and Forestry"', '"SSAF"']
    page = urllib2.urlopen('http://ag.senate.gov/site/cmtemembers.html')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('tr')
    for m in member_containers:
        a = m.find('a')
        if a == None:
            continue
        name = str(a.contents[0])
        name = name.replace('\n', '').replace('\r', '').replace('  ', '')
        comma_pos = name.find(',')
        name = name[:comma_pos]
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'    

#def subcomm_senate_ag():
# TODO
#
# This subcommittee page has very poorly structured html.

def comm_senate_appropriations():
    members = ['"Senate Committee on Appropriations"', '"SSAP"']
    page = urllib2.urlopen('http://appropriations.senate.gov/about-members.cfm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('td', 'member-list-content')
    for m in member_containers:
        strong = m.find('strong')
        if strong == None:
            continue
        name = str(strong.contents[0])
        members.append('"' + name.title() + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_appropriations():
    def parse_members(url, title, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_containers = soup.findAll('div', 'CS_Textblock_Text')

        container = member_containers[1]
        for m in container.findAll('a'):
            name = str(m.contents[0])
            name = name.replace('Senator ', '')
            paren_pos = name.find(' (')
            name = name[:paren_pos]
            members.append('"' + name + '"')
        return ', '.join(members)

    title = 'Senate Committee on Appropriations'
    member_string = ''

    member_string += parse_members('http://appropriations.senate.gov/sc-agriculture.cfm', title, 'Subcommittee on Agriculture, Rural Development, Food and Drug Administration, and Related Agencies', 'SSAP_agr') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-commerce.cfm', title, 'Subcommittee on Commerce, Justice, and Science', 'SSAP_cjs') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-defense.cfm', title, 'Subcommittee on Defense', 'SSAP_def') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-financial.cfm', title, 'Subcommittee on Financial Services and General Government', 'SSAP_fin') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-energy.cfm', title, 'Subcommittee on Energy and Water Development', 'SSAP_ewd') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-homeland-security.cfm', title, 'Subcommittee on Homeland Security', 'SSAP_dhs') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-interior.cfm', title, 'Subcommittee on Interior and Related Agencies', 'SSAP_doi') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-labor.cfm', title, 'Subcommittee on Labor, Health and Human Services, and Education', 'SSAP_hhs') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-legislative.cfm', title, 'Subcommittee on Legislative Branch', 'SSAP_leg') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-military.cfm', title, 'Subcommittee on Military Construction and Veterans Affairs', 'SSAP_dva') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-state.cfm', title, 'Subcommittee on State, Foreign Operations, and Related Programs', 'SSAP_sta') + '\n'

    member_string += parse_members('http://appropriations.senate.gov/sc-transportation.cfm', title, 'Subcommittee on Transportation, Treasury, the Judiciary, Housing and Urban Development', 'SSAP_jud') + '\n'
    
    return member_string

def comm_senate_armedservices():
    members = ['"Senate Committee on Armed Services"', '"SSAS"']
    page = urllib2.urlopen('http://armed-services.senate.gov/members.htm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('p')
    for m in member_containers:
        for a in m.findAll('a'):
            name = str(a.contents[0])
            paren_pos = name.find(' (')
            if paren_pos == -1:
                continue
            name = name[:paren_pos]
            members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_armedservices():
    def parse_members(table, title, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']
        tr = table.findAll('tr')[1]
        for td in tr.findAll('td')[1:]:
            names_text = [str(c) for c in td.contents]
            names_text = ''.join(names_text)
            names = names_text.split('<br />')
            for n in names:
                space_pos = n.find(' (')
                if n[:space_pos] != '':
                    members.append('"' + n[:space_pos] + '"')
        return members

    title = 'Senate Committee on Armed Services'
    page = urllib2.urlopen('http://www.senate.gov/general/committee_membership/committee_memberships_SSAS.htm')
    soup = BeautifulSoup(page)
    tables = soup.findAll('table', 'contenttext', width='100%')

    member_string = ''

    member_string += ', '.join(parse_members(tables[3], title, 'Subcommittee on Airland', 'SSAS_air')) + '\n'
    member_string += ', '.join(parse_members(tables[5], title, 'Subcommittee on Emerging Threats and Capabilities', 'SSAS_thr')) + '\n'
    member_string += ', '.join(parse_members(tables[7], title, 'Subcommittee on Personnel', 'SSAS_per')) + '\n'
    member_string += ', '.join(parse_members(tables[9], title, 'Subcommittee on Readiness and Management Support', 'SSAS_rdi')) + '\n'
    member_string += ', '.join(parse_members(tables[3], title, 'Subcommittee on Seapower', 'SSAS_sea')) + '\n'
    member_string += ', '.join(parse_members(tables[3], title, 'Subcommittee on Strategic Forces', 'SSAS_sfs')) + '\n'

    return member_string

def comm_senate_banking():
    members = ['"Senate Committee on Banking, Housing, and Urban Affairs"', '"SSBK"']
    page = urllib2.urlopen('http://banking.senate.gov/public/index.cfm?FuseAction=CommitteeInformation.Membership')
    soup = BeautifulSoup(page)
    member_containers = soup.find('tbody')
    for m in member_containers.findAll('a', 'blueunder'):
        name = str(m.contents[0])
        members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_banking():
    def parse_members(url, title, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_containers = soup.findAll('td', 'vblack8', valign='top')

        for m in member_containers:
            plaintext = ''.join(m.findAll(text=True))
            names = plaintext.split('\n')
            names = [n.replace('\t', '') for n in names]
            for n in names:
                if n.find('Republic') != -1 or n.find('Democrat') != -1:
                    continue
                if n == '':
                    continue
                paren_pos = n.find(' (')
                if paren_pos != -1:
                    n = n[:paren_pos]
                members.append('"' + n.strip() + '"')

        return ', '.join(members)

    title = 'Senate Committee on Banking, Housing, and Urban Affairs'
    member_string = ''

    member_string += parse_members('http://banking.senate.gov/public/index.cfm?Fuseaction=CommitteeInformation.Subcommittee&Subcommittee_ID=d2141d98-ccd0-439b-a59e-1967939d9679', title, 'Subcommittee on Economic Policy', 'SSBK_ecp') + '\n'

    member_string += parse_members('http://banking.senate.gov/public/index.cfm?Fuseaction=CommitteeInformation.Subcommittee&Subcommittee_ID=e08628bc-d809-46c9-99f1-5bb8bead82bc', title, 'Subcommittee on Housing, Transportation, and Community Development', 'SSBK_htc') + '\n'

    member_string += parse_members('http://banking.senate.gov/public/index.cfm?Fuseaction=CommitteeInformation.Subcommittee&Subcommittee_ID=d7d38747-f226-46f4-8aaa-c06fae94bf41', title, 'Subcommittee on Financial Institutions', 'SSBK_fin') + '\n'

    member_string += parse_members('http://banking.senate.gov/public/index.cfm?Fuseaction=CommitteeInformation.Subcommittee&Subcommittee_ID=cc2adfc2-d906-4355-8c46-cf47138ee005', title, 'Subcommittee on Security and International Trade and Finance', 'SSAP_fin') + '\n'

    member_string += parse_members('http://banking.senate.gov/public/index.cfm?Fuseaction=CommitteeInformation.Subcommittee&Subcommittee_ID=decb3c3c-2f60-49ae-ac2a-d82e1b912c9c', title, 'Subcommittee on Securities, Insurance, and Investment', 'SSBK_sii') + '\n'

    return member_string

def comm_senate_commerce():
    members = ['"Senate Committee on Commerce, Science, and Transportation"', '"SSCM"']
    page = urllib2.urlopen('http://commerce.senate.gov/public/index.cfm?p=CommitteeMembers')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('div', id='committeeMembers')
    for m in member_containers:
        alist = m.findAll('a', 'title')
        for n in alist:
            name = str(n.contents[0]).replace('Senator ', '')
            members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_commerce():
    def parse_members(url, title, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_container = soup.find('table', border='0')
        tds = member_container.findAll('td', valign='top')
        for td in tds:
            names = None
            ul = td.find('ul')
            if ul != None:
                names = []
                for li in ul.findAll('li'):
                    names.append(li.contents[0])
            else:
                plaintext = ''.join(td.findAll(text=True))
                if plaintext.find('Republicans') != -1:
                    continue
                if plaintext.find('Democrats') != -1:
                    continue
                names = plaintext.split('&bull;')
            for n in names:
                n = n.replace('&nbsp;', ' ')
                n = n.strip()
                if n != '':
                    n = n.replace(' - Ranking Member', '')
                    n = n.replace(' - Chairman', '')
                    n = n.replace(' - Chairwoman', '')
                    members.append('"' + n + '"')

        return ', '.join(members)

    title = 'Senate Committee on Commerce, Science, and Transportation'
    member_string = ''

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=AviationOperationsSafetyandSecurity', title, 'Subcommittee on Aviation Operations, Safety, and Security', 'SSCM_avi') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=CommunicationsTechnologyandtheInternet', title, 'Subcommittee on Communications, Technology, and the Internet', 'SSCM_cti') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=CompetitivenessInnovationandExportPromotion', title, 'Subcommittee on Competitiveness, Innovation, and Export Promotion', 'SSCM_cie') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=ConsumerProtectionProductSafetyandInsurance', title, 'Subcommittee on Consumer Protection, Product Safety, and Insurance', 'SSCM_cpi') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=OceansAtmosphereFisheriesandCoastGuard', title, 'Subcommittee on Oceans, Atmosphere, Fisheries, and Coast Guard', 'SSCM_oaf') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=ScienceandSpace', title, 'Subcommittee on Space and Science', 'SSCM_sas') + '\n'

    member_string += parse_members('http://commerce.senate.gov/public/index.cfm?p=SurfaceTransportationandMerchantMarineInfrastructureSafetyandSecurity', title, 'Subcommittee on Surface Transportation and Merchant Marine Infrastructure, Safety, and Security', 'SSCM_stm') + '\n'

    return member_string

def comm_senate_budget():
    members = ['"Senate Committee on the Budget"', '"SSBU"']
    page = urllib2.urlopen('http://budget.senate.gov/democratic/democrats.html')
    soup = BeautifulSoup(page)
    member_container = soup.find('td', width='470', valign='top')
    for m in member_container.findAll('a'):
        name = m.contents[0]
        members.append('"' + name.strip() + '"')

    page = urllib2.urlopen('http://budget.senate.gov/democratic/republican.html')
    soup = BeautifulSoup(page)
    member_container = soup.find('td', width='470', valign='top')
    for m in member_container.findAll('a'):
        name = m.contents[0]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_judiciary():
    members = ['"Senate Committee on the Judiciary"', '"SSJU"']
    page = urllib2.urlopen('http://judiciary.senate.gov/about/members.cfm')
    soup = BeautifulSoup(page)
    div = soup.find('div', 'content')
    member_containers = div.findAll('td')
    for td in member_containers:
        name = str(''.join(td.findAll(text=True)))
        name = name.replace('Biography', '')
        name = name.replace('Chairman,', '')
        name = name.replace('Ranking Member,', '')
        name = name.replace('\n', ' ').replace('\r', '').replace('&nbsp;', ' ')
        party_pos = name.find(' D-')
        if party_pos == -1:
            party_pos = name.find(' R-')
        name = name[:party_pos]
        name = name.strip()

        if name != '' and name.find('Committee membership') == -1:
            members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def subcomm_senate_judiciary():
    def parse_members(url, title, name, shortname):
        members = ['"' + title + '/' + name + '"', '"' + shortname + '"']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        member_container = soup.find('tbody')
        tds = member_container.findAll('td')
        for td in tds:
            #plaintext = ''.join(td.findAll(text=True))
            alist = td.findAll('a')
            for a in alist:
                if a == None:
                    continue
                name = str(a.contents[0])
                if name == '<br />':
                    continue
                members.append('"' + name + '"')

        return ', '.join(members)

    title = 'Senate Committee on the Judiciary'
    member_string = ''

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/oversight.cfm', title, 'Subcommittee on Administrative Oversight and the Courts', 'SSJU_osi') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/antitrust.cfm', title, 'Subcommittee on Antitrust, Competition Policy and Consumer Rights', 'SSJU_acc') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/constitution.cfm', title, 'Subcommittee on the Constitution', 'SSJU_con') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/constitution.cfm', title, 'Subcommittee on Crime and Drugs', 'SSCM_cri') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/humanrights.cfm', title, 'Subcommittee on Human Rights and the Law', 'SSJU_hrl') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/immigration.cfm', title, 'Subcommittee on Immigration, Refugees and Border Security', 'SSJU_imi') + '\n'

    member_string += parse_members('http://judiciary.senate.gov/about/subcommittees/terrorism.cfm', title, 'Subcommittee on Terrorism and Homeland Security', 'SSJU_ter') + '\n'

    return member_string

def comm_senate_rules():
    members = ['"Senate Committee on Rules and Administration"', '"SSRA"']
    page = urllib2.urlopen('http://rules.senate.gov/public/index.cfm?p=CommitteeMembers')
    soup = BeautifulSoup(page)
    div = soup.find('div', 'committeeMembers')
    member_containers = div.findAll('div', 'title')
    for m in member_containers:
        a = m.find('a').contents[0]
        commapos = a.find(', ')
        name = a[:commapos]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_sbc():
    members = ['"Senate Committee on Small Business and Entrepreneurship"', '"SSRA"']
    page = urllib2.urlopen('http://sbc.senate.gov/public/index.cfm?p=CommitteeMembers')
    soup = BeautifulSoup(page)
    div = soup.find('tbody')
    member_containers = div.findAll('a')
    for m in member_containers:
        name = m.contents[0]
        parenpos = name.find(' (')
        name = name[:parenpos]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_veterans():
    members = ['"Senate Committee on Veterans\' Affairs"', '"SSVA"']
    page = urllib2.urlopen('http://veterans.senate.gov/committee-members.cfm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('font', color='#006600')
    for m in member_containers:
        name = m.contents[0]
        commapos = name.find(', ')
        name = name[:commapos]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_intel():
    members = ['"Senate Committee on Intelligence"', '"SLIN"']
    page = urllib2.urlopen('http://intelligence.senate.gov/memberscurrent.html')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('a', 'bodyLink')
    for m in member_containers:
        if len(m.contents) == 0:
            continue
        name = m.contents[0]
        name = name[:-1]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_aging():
    members = ['"Senate Special Committee on Aging"', '"SPAG"']
    page = urllib2.urlopen('http://aging.senate.gov/about/members.cfm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('ul', type='circle')
    for m in member_containers:
        for li in m.findAll('li'):
            a = li.find('a')
            if a == None:
                continue
            else:
                name = a.contents[0]
            members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_joint_econ():
    members = ['"Joint Economic Committee"', '"JSEC"']
    # Senate Members
    page = urllib2.urlopen('http://jec.senate.gov/public/index.cfm?p=SenateMembers')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('h5', 'title')
    for m in member_containers:
        name = m.contents[0]
        name = name.replace('Senator ', '')
        commapos = name.find(', ')
        name = name[:commapos]
        members.append('"' + name.strip() + '"')

    # House Members
    page = urllib2.urlopen('http://jec.senate.gov/public/index.cfm?p=HouseMembers')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('h5', 'title')
    for m in member_containers:
        name = m.contents[0]
        name = name.replace('Congressman ', '')
        name = name.replace('Congresswoman', '')
        commapos = name.find(', ')
        if commapos != -1:
            name = name[:commapos]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_joint_library():
    members = ['"Joint Economic Committee"', '"JSEC"']
    page = urllib2.urlopen('http://www.senate.gov/general/committee_membership/committee_memberships_JSLC.htm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('pub_last')
    for m_lname in member_containers:
        lname = m_lname.contents[0]
        m_fname = m_lname.nextSibling.nextSibling
        fname = m_fname.contents[0]
        members.append('"' + fname + ' ' + lname + '"')

    return ', '.join(members) + '\n'

def comm_joint_taxation():
    members = ['"Joint Committee on Taxation"', '"JSTX"']
    page = urllib2.urlopen('http://www.jct.gov/')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('td', align='center', valign='top')
    for m in member_containers:
        for a in m.findAll('a'):
            name = str(a.contents[0])
            name = name.replace('<br />', '')
            members.append('"' + name + '"')

    return ', '.join(members) + '\n'

def comm_joint_printing():
    members = ['"Joint Committee on Printing"', '"JSPR"']
    page = urllib2.urlopen('http://www.house.gov/jcp/1memjcptest.htm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('strong')
    for m in member_containers:
        for a in m.findAll('a'):
            if a == None:
                continue
            name = a.contents[0]
            if name.find('Senator') == -1 and name.find('Rep.') == -1:
                continue
            name = name.replace('Senator ', '').replace('Rep. ', '')
            if name.find(',') != -1:
                name = name[:-1]
            members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'

def comm_senate_indian():
    members = ['"Senate Committee on Indian Affairs"', '"SLIA"']
    page = urllib2.urlopen('http://indian.senate.gov/about/committeemembers.cfm')
    soup = BeautifulSoup(page)
    member_containers = soup.findAll('a', target='_blank')
    for a in member_containers:
        if a == None:
            continue
        name = a.contents[0]
        members.append('"' + name.strip() + '"')

    return ', '.join(members) + '\n'


tasks = [comm_agriculture, subcomm_agriculture, comm_appropriations, subcomm_appropriations, comm_armedservices, subcomm_armedservices, comm_budget, comm_edlabor, subcomm_edlabor, comm_energycommerce, subcomm_energycommerce, comm_financialservices, subcomm_financialservices, comm_foreignaffairs, subcomm_foreignaffairs, comm_energygw, comm_permanentintel, comm_rules, comm_veterans, comm_waysandmeans, subcomm_waysandmeans, comm_transportation, subcomm_transportation, comm_smallbusiness, subcomm_smallbusiness, comm_science, subcomm_hsc, comm_cha, comm_natres, comm_oversight, subcomm_oversight, comm_homelandsecurity, comm_help, comm_foreign, subcomm_foreign, comm_senate_finance, subcomm_senate_finance, comm_senate_epw, comm_senate_ethics, comm_senate_energy, subcomm_senate_energy, comm_senate_ag, comm_senate_appropriations, subcomm_senate_appropriations, comm_senate_armedservices, subcomm_senate_armedservices, comm_senate_banking, subcomm_senate_banking, comm_senate_commerce, subcomm_senate_commerce, comm_senate_budget, comm_senate_judiciary, subcomm_senate_judiciary, comm_senate_rules, comm_senate_sbc, comm_senate_veterans, comm_senate_aging, comm_senate_intel, comm_joint_econ, comm_joint_library, comm_joint_taxation, comm_joint_printing, comm_senate_indian]

FILE = open('committees.csv', 'w')

for t in tasks:
    try:
        comm = t()
        FILE.write(comm)
    except Exception, e:
        print 'Problem with ' + str(t)
        #print e

FILE.close()
