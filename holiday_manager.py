from config import api_key
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
import datetime
import json
import time 


@dataclass
class Holiday:
    name: str
    date: str
    
    def __str__(self):
        return self.name+' '+'('+str(self.date)+')'
    
    def __repr__(self): 
        return self.__class__.__name__
        
@dataclass
class HolidayList:
    def __init__(self):
        self.innerHolidays = []
        
            
    ### fx to add holiday object to innerHolidays list with append
        
    def addHoliday(self,holidayObj):
        if isinstance(holidayObj,Holiday):
            self.innerHolidays.append(holidayObj)
            print(f"Success:\n{holidayObj} has been added to the holiday list.")
        else:
            print(f'Sorry, {holidayObj} is not a holiday object.')
        
    # fx to find a holiday in innerHolidays list
    def searchHoliday(self,holidayName, date):
        for holidict in self.innerHolidays:
            if holidict.date == date and holidict.name == holidayName:
                return holidict
            else:
                print("\nHoliday not found. Please try again.")    
    
    
    # fx to remove a holiday object from innerHolidays list
    def removeHoliday(self,holidayName):
        foundHoliday = False
        for i in range(0,len(self.innerHolidays)):
            if self.innerHolidays[i].name == holidayName:
                self.innerHolidays.remove(self.innerHolidays[i])
                print(f"{holidayName} successfully removed")
                foundHoliday = True
                return True
                
        if not foundHoliday:
            print("Holiday not found. Please try again.")
            return False
        
    # fx to read json file and use addHoliday fx ^^^ to add holiday object to inner list
    def read_json(self,fileLocation):
        with open(fileLocation, 'r') as openfile:
            json_object = json.load(openfile)

        for listitem in json_object['holidays']:
            holiday = Holiday(listitem['name'],listitem['date'])
            self.innerHolidays.append(holiday)

        
    # fx to save a json object as to a json file
    def overwrite_json(self,fileLocation):
        export_list = []
        for holiday in self.innerHolidays:
            dict = {"name":holiday.name, "date":holiday.date}
            export_list.append(dict)

        export_json = {"holidays": export_list}

        json_write = json.dumps(export_json, indent=4)

        with open(fileLocation, 'w') as output:
            output.write(json_write)
        
    # fx to scrape holidays website, check that the name,date dict is not in innerHolidays and add non-dupes to it
    def scrapeHolidays(self):
        new_list_of_dicts = []
        for i in range(2020, 2025):    
            req = requests.get(f"https://www.timeanddate.com/holidays/us/{i}").text
            formatted_date = []
            holidays = []
            holidates = []
            list_of_dicts = []
            seen = set()
            
            soup = BeautifulSoup(req, "html.parser")
            SoupDates = list(soup.tbody.find_all(attrs={"class": "nw"}))

            for item in SoupDates:
                if SoupDates.index(item) % 2 == 0:
                    holidates.append(item.string+f' {i}')

        #     print('got dates')

            for date in holidates:
                new_date = dt.strptime(date,"%b %d %Y")
                formatted_date.append(new_date.strftime("%Y-%m-%d"))
        #         print(f'done with date {date}')

            SoupHolidays = soup.tbody.find_all('a')

            for item in SoupHolidays:
                holidays.append(item.string)

            for j in range(0, len(holidays)):
                name_value = holidays[j]
                date_value = formatted_date[j]
                tempdict = {"name": name_value, "date": date_value}

                list_of_dicts.append(tempdict)

            for d in list_of_dicts:
                t = tuple(d.items())
                if t not in seen:
                    seen.add(t)
                    new_list_of_dicts.append(d)
        #     print(f'done with year {i}')

            for holidict in new_list_of_dicts:
                duplicateCount = 0
                for i in range(0,len(self.innerHolidays)):
                    if holidict['name'] == self.innerHolidays[i].name and holidict['date'] == self.innerHolidays[i].date:
                        duplicateCount += 1

                if duplicateCount == 0:
                    holiday = Holiday(holidict['name'],holidict['date'])
                    self.innerHolidays.append(holiday)
 
        
    # fx to return length of innerHolidays (total holidays)
    def numHolidays(self):
        holidayTotal= len(self.innerHolidays)
        print(f"There are currently {holidayTotal} holidays stored.")
    
    # lambda fx to filter innerHolidays list by year, week number and cast filter results to list, return list
    def filterHolidaysByWeek(self,year, week_number):
        startdate = dt.strptime(f'{year} %d 1' % int(week_number), '%Y %U %w')
        startdate.strftime('%Y-%m-%d')
        dates = [startdate.strftime('%Y-%m-%d')]

        for i in range(1,7):
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime('%Y-%m-%d'))

        filtered_holidays = list(filter(lambda holiday:  holiday.date in dates ,self.innerHolidays))
        print(f"These are the holidays for {year} week #{week_number}")
        return filtered_holidays
        
    # fx to display holidays in a given week (week 1 of year 2020, etc.) using the __str__ method
    def displayHolidaysInWeek(self,holidaylist):
        for i in range(0,len(holidaylist)):
            print(holidaylist[i])

    # fx to convert weeknumber into a range between two days, use Try/Except, query weatherAPI & returnformat info
    def getWeather(self,weekNum):
        global api_key
        CurrentDate = datetime.datetime.now()

        weekNum = int(CurrentDate.strftime("%U"))
        year = int(CurrentDate.strftime("%Y"))

        startdate = dt.strptime(f'{year} %d 1' % weekNum, '%Y %U %w')
        
        enddate = startdate + datetime.timedelta(days=6)

        dates = [startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d')]

        response = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/11420/{dates[0]}/{dates[1]}?key={api_key}')

        weather = []        
        for day in response.json()['days']:
            weather.append(day['conditions'])
            
        weatherDates = []
        for day in response.json()['days']:
            weatherDates.append(day['datetime'])

        weather_and_dates = []
        for i in range(0, len(weatherDates)):
            temp_dict = {'date':weatherDates[i], 'weather':weather[i]}
            weather_and_dates.append(temp_dict)

        return weather_and_dates
    
    # fx to lookup current week, year & return list of holidays, then use displayHolidaysinWeek fx ^^^, ask if want weather
    def viewCurrentWeek(self):
        CurrentDate = dt.now()

        weekNum = int(CurrentDate.strftime("%U"))
        year = int(CurrentDate.strftime("%Y"))

        holidayList = self.filterHolidaysByWeek(year,weekNum)

        weather_and_dates = self.getWeather(weekNum)

        self.displayHolidaysInWeek(holidayList)

        choiceMade = False

        while not choiceMade:
            validInput = False
            while not validInput:
                userSelect = input("Would you like to see this week's weather? [y/n]: ")
                if userSelect != 'y' and userSelect != 'n':
                    print('That input is not valid')
                else:
                    validInput = True

            if userSelect == 'y':
                for holiday in holidayList:
                    for item in weather_and_dates:
                        if holiday.date == item['date']:
                            print(f"{holiday} - {item['weather']}")
                choiceMade = True

            else:
                choiceMade = True


def main():
    holidaylist = HolidayList() 
    fileloc = 'holidays.json'
    holidaylist.read_json(fileloc)
    holidaylist.scrapeHolidays()
    savedChanges = False
    exit = False
    while not exit:
    
        print("Holiday Management")
        print("==================")
        holidaylist.numHolidays()
        
        selection = None

        if selection == None:
            print("================")
            print("Holiday Menu")
            print("================")
            print("""
                   1. Add a Holiday\n
                   2. Remove a Holiday\n
                   3. Save Holiday List\n
                   4. View Holidays\n
                   5. Exit""")
                    
        validInput = False
        
        while not validInput:
            selection = input("Please select a menu option: ")
            if selection.isnumeric() == False:
                print("Only options displayed in the menu are accepted. ")
            elif int(selection) < 1 or int(selection) > 5:
                print("Input value out of range. Try again.")
            else:
                selection = int(selection)
                validInput = True
                

        if selection == 1:
            print("Add a Holiday")
            print("=============")
            holidayName = input("Holiday: ")
            validDate = False
            while not validDate:
                inputDate = input("Date (yyyy-mm-dd): ")
                try:
                    holidayDate = datetime.datetime.strptime(inputDate, "%Y-%m-%d").strftime('%Y-%m-%d')
                    validDate = True
                except:
                    print("Error:\nInvalid date. Please try again.")
            holiday = Holiday(holidayName, holidayDate)

            holidaylist.addHoliday(holiday)
            savedChanges = False
            selection = None

        if selection == 2:
            print("Remove a Holiday")
            print("================")
            nameFound = False
            while not nameFound:
                holidayName = input("Holiday Name: ")
                nameFound = holidaylist.removeHoliday(holidayName)
            
            savedChanges = False
            selection = None

        if selection == 3:
            print("Save Holiday List")
            print("=================")
            validInput = False
            while not validInput:
                save_choice = input("Are you sure you want to save your changes? [y/n]: ")
                if save_choice != 'y' and save_choice != 'n':
                    print("Please type 'y' or 'n'")
                else:
                    validInput = True

            if save_choice == 'y':
                try:
                    holidaylist.overwrite_json(fileloc)
                    print("Success:\nYour changes have been saved.")
                    savedChanges = True
                except:
                    print("There was an issue saving your file.")
            elif save_choice == 'n':
                print("Canceled:\nHoliday list file save cancelled.")
            selection = None

        if selection == 4:
            print("View Holidays")
            print("=============")
            validInput = False
            while not validInput:
                year = input("Which year?: ")
                if year.isnumeric() == False:
                    print("Only numeric values accepted")
                elif int(year) > 2024 or int(year) < 2020:
                    print("Year is outside of range. List only goes 2 years prior and 2 years ahead of present.")
                else:
                    validInput = True
            validInput = False
            while not validInput:
                week = input("Which week? #[1-52, leave blank for the current week]: ")
                if week.isnumeric() == True:
                    if int(week) > 52 or int(week) < 1:
                        print("Week number out of range. Try again.")
                    else:
                        listOfHolidays = holidaylist.filterHolidaysByWeek(year, week)
                        holidaylist.displayHolidaysInWeek(listOfHolidays)
                        validInput = True
                elif week.isnumeric() == False:
                    if week != '':
                        print("Choice not supported. Please choose a number between 1-52 or leave blank")
                    else:
                        holidaylist.viewCurrentWeek()
                        validInput = True


            selection = None
        if selection == 5:
            print('Exit')
            print("====")
            
            if savedChanges == True:
                validInput = False
                while not validInput:
                    exit_select = input("Are you sure you want to exit? (y/n): ")
                    if exit_select == 'y':
                        exit = True
                        validInput = True
                    elif exit_select == 'n':
                        exit = False
                        validInput = True
                    else:
                        print("Input not recognized. Please type y or n")
                        
            elif not savedChanges:
                validInput = False
                while not validInput:
                    print("Are you sure you want to exit?")
                    exit_select = input("Your unsaved changes will be lost. (y/n) ")
                    if exit_select == 'y':
                        print("Goodbye!")
                        exit = True
                        validInput = True
                    elif exit_select == 'n':
                        exit = False
                        validInput = True
                    else:
                        print("Input not recognized. Please type y or n")

if __name__ == "__main__":
    main()