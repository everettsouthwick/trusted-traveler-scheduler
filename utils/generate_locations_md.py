import requests

GOES_URL_FORMAT = 'https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true'

class Location:
     def __init__(self, id, name, city, state, country_code, services) -> None:
          self.id = id
          self.name = name.strip()
          self.city = city.strip()
          self.state = state.strip()
          self.country_code = country_code.strip()
          self.services = services
     
class Services:
    def __init__(self, global_entry : bool, nexus: bool, sentri: bool, mexico_fast: bool, canada_fast: bool) -> None:
        # if global entry is true then make self.globalentry = :heavy_check_mark:
        # else make self.globalentry = :x:
        if global_entry:
            self.global_entry = ':heavy_check_mark:'
        else:
            self.global_entry = ':x:'
        if nexus:
            self.nexus = ':heavy_check_mark:'
        else:
            self.nexus = ':x:'
        if sentri:
            self.sentri = ':heavy_check_mark:'
        else:
            self.sentri = ':x:'
        if mexico_fast:
            self.mexico_fast = ':heavy_check_mark:'
        else:
            self.mexico_fast = ':x:'
        if canada_fast:
            self.canada_fast = ':heavy_check_mark:'
        else:
            self.canada_fast = ':x:'

def determine_services(location):
    global_entry = False
    nexus = False
    sentri = False
    mexico_fast = False
    canada_fast = False
    for service in location['services']:
        if service['name'] == 'Global Entry':
            global_entry = True
        elif service['name'] == 'NEXUS':
            nexus = True
        elif service['name'] == 'SENTRI':
            sentri = True
        elif service['name'] == 'Mexico FAST':
            mexico_fast = True
        elif service['name'] == 'Canada FAST':
            canada_fast = True
        else:
            continue
    return Services(global_entry, nexus, sentri, mexico_fast, canada_fast)

def output_to_markdown(locations):
    with open('LOCATIONS.md', 'w', encoding='utf-8') as f:
        f.write('| Id | Name | Area | Global Entry | NEXUS | SENTRI | Mexico FAST | Canada FAST |\n')
        f.write('| -- | ---- | ---- | ------------ | ----- | ------ | ----------- | ----------- |\n')
        for location in locations:
            f.write(f'| {location.id} | {location.name} | {location.city}, {location.state}, {location.country_code} | {location.services.global_entry} | {location.services.nexus} | {location.services.sentri} | {location.services.mexico_fast} | {location.services.canada_fast} |\n')

def get_locations():
        try:
            locations = requests.get(GOES_URL_FORMAT).json()

            if not locations:
                return
            
            enrollment_centers = []
            for location in locations:
                if location['operational']:
                    enrollment_centers.append(Location(location['id'], location['name'], location['city'], location['state'], location['countryCode'], determine_services(location)))

            if not enrollment_centers:
                return
            
            output_to_markdown(enrollment_centers)
            
        except OSError:
            return
        
get_locations()
    
