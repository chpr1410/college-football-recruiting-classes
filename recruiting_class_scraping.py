import pandas as pd
from bs4 import BeautifulSoup
import statistics
import requests

team = 'alabama'
year = '2022'
ceiling = 10

# Add the `user-agent` otherwise we will get blocked when sending the request
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

def get_power_five_schools(url):
    response = requests.get(url, headers = headers).content
    soup = BeautifulSoup(response, "html.parser")
    power_conferences = soup.find('ul',{'class': 'team-index college'})
    schools_by_conference = power_conferences.find_all('ul',{'class': 'division-team_lst'})

    conferences = []
    schools = []

    conferences.append('ACC')
    schools.append('notre-dame')

    for conference in schools_by_conference:
        conference_name = conference.find('li',{'class': 'conference-name'})['id']
        school_list = conference.find_all('li')
        for x in range(len(school_list)):
            if x > 0:
                school_name = school_list[x].find('a')['href'].split('/college/')[1].split('/')[0]
                conferences.append(conference_name)
                schools.append(school_name)

    power_five = pd.DataFrame()
    power_five['School'] = schools
    power_five['Conference'] = conferences

    power_five.to_csv('power_five_schools.csv',index=False)
    
    return

def get_offer_list(url):
    response = requests.get(url, headers = headers).content
    soup = BeautifulSoup(response, "html.parser")

    try:
        as_a_prospect = soup.find('section',{'class': 'as-a-prospect'})
        prospect_link = as_a_prospect.find('a',{'class': 'view-profile-link'})['href']

        response2 = requests.get(prospect_link, headers = headers).content
        soup2 = BeautifulSoup(response2, "html.parser")
        
    except:
        soup2 = soup
    
    college_options_link = soup2.find('a',{'class': 'college-comp__view-all'})['href']

    response3 = requests.get(college_options_link, headers = headers).content
    soup3 = BeautifulSoup(response3, "html.parser")

    team_section = soup3.find('section',{'class': 'main-content list-content'})

    teams_and_offers = team_section.find_all('div',{'class': 'left'})

    team_names = []
    offers = []
    for team in teams_and_offers:
        team_name_section = team.find('div',{'class': 'first_blk'})
        team_name = team_name_section.find('a')['href']
        try:
            team_name = team_name.split('/college/')[1].split('/Season')[0]
            team_names.append(team_name)

            offer_section = team.find('div',{'class': 'secondary_blk'})
            offer = offer_section.find('span',{'class': 'offer'})
            offer = offer.text.split('\n')[3].split(' ')[-1]
            offers.append(offer)
        except:
            pass

    offer_list = pd.DataFrame()
    offer_list['Team'] = team_names
    offer_list['Offer'] = offers
    offer_list = offer_list.loc[(offer_list['Offer']=='Yes')]
    
    return offer_list

def get_power_five_offer_list(offer_list):
    p5_offer = []
    for school in list(offer_list['Team']):
        if school in list(power_five['School']):
            p5_offer.append('Yes')
        else:
            p5_offer.append('No')
    df = pd.DataFrame()
    df['Team'] = offer_list['Team']
    df['Offer'] = offer_list['Offer']
    df['P5 Offer'] = p5_offer

    df = df.loc[(df['P5 Offer']=='Yes')]
    
    return df

def evaluate_class(team, year, ceiling):
    url = 'https://247sports.com/college/'+team+'/Season/'+year+'-Football/Commits/'
    response = requests.get(url, headers = headers).content
    soup = BeautifulSoup(response, "html.parser")

    recruit_names = []
    recruit_p5_offers = []

    recruit_list = soup.find_all('div',{'class': 'recruit'})
    for recruit in recruit_list:
        recruit_name = recruit.find('a',{'class': "ri-page__name-link"}).text
        recruit_profile_url = 'http:' + recruit.find('a',href=True)['href']
        offer_list = get_offer_list(recruit_profile_url)
        p5_offers = get_power_five_offer_list(offer_list)

        recruit_names.append(recruit_name)
        recruit_p5_offers.append(len(p5_offers))
    
    p5_offers_with_ceiling = []
    
    for offers in recruit_p5_offers:
        if offers > ceiling:
            p5_offers_with_ceiling.append(ceiling)
        else:
            p5_offers_with_ceiling.append(offers)
            
    avg = round(statistics.mean(p5_offers_with_ceiling),4)

    many_offers = []
    for x in range(len(recruit_names)):
        if p5_offers_with_ceiling[x] >= 10:
            many_offers.append(recruit_names[x])

    print("Team:",team)
    print("Year:",year)
    print('Avg Offers: ', avg)
    print('# of Players in class: ', len(recruit_names))
    print('# of Players with 10 or more: ', len(many_offers))
    print('Players with 10 or more: ', many_offers)
    
    return

try:
    power_five = pd.read_csv('power_five_schools.csv')
except:
    url = 'https://247sports.com/League/NCAA-FB/Teams/'
    get_power_five_schools(url)
    power_five = pd.read_csv('power_five_schools.csv')

evaluate_class(team, year,ceiling)