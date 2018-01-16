import mediawiki
from mediawiki import MediaWiki
from . import get_airport_info
from bs4 import BeautifulSoup

wikipedia = MediaWiki()
'''Returns the content of a corresponding Wikipedia page, 
given the iata code of the airport.'''
def get_summary(iata_code):
    page = get_page(iata_code)
    return page.summary


'''Returns the corresponding Wikipedia page according to the 
municipality of the airport. If an exception is thrown, then
the first page option is returned.'''
def get_page(iata_code):
    airport = get_airport_info.get_airport(iata_code)
    region = get_airport_info.get_region(airport)
    if airport:
        try:
            try:
                page = wikipedia.page(wikipedia.opensearch(airport['municipality']  + ", " + region['name'])[0][0])
                return page
            except IndexError:
                results = wikipedia.opensearch(region['name'])
                if results == []:
                    results = wikipedia.opensearch(airport['municipality'])

                return wikipedia.page(results[0][0])
        except mediawiki.exceptions.DisambiguationError as e:
            return wikipedia.page(e.options[0])
    else:
        return None

'''Returns the first image URL of the Wikipedia page of the
city that corresponds to the iata code.'''
def get_img_url(iata_code):
    page = get_page(iata_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    vcards = soup.find_all("table", class_="infobox geography vcard")

    if vcards == []:
        if page.images == []:
            return ""
        else:
            return page.images[0]
    elif len(vcards) == 1:
        return vcards[0].find_all("a", class_='image')[0]['src']
    else:
        return vcards[0].find_all("a", class_='image')[1]['src']
        
