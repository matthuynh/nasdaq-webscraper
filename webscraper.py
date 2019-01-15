from bs4 import BeautifulSoup
from requests import get
import re
import time


class Webscraper:
    # Initialize the class
    def __init__(self):
        self.text = ''
        self.lst = []

    # Retrieves data from the NASDAQ Summary Page
    def get_data_nasdaq_summary(self, ticker: str) -> dict:
        start_time = time.time()
        url = 'https://www.nasdaq.com/symbol/'+ ticker
        response = get(url)
        # Create parse tree (BeautifulSoup Object)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(class_= 'column span-1-of-2')
        #print(len(data))
        #print(type(data))

        items = []
        # Extract table rows
        for i in range(len(data)):
            items.extend(data[i].find_all(class_='table-cell'))

        # Cleans up data
        for i in range(len(items)):
            # get_text strips the HTML tags
            items[i] = items[i].get_text(strip = True).encode\
                ('ASCII', 'ignore').decode('utf-8')
            # Gets rid of the extra ASCII characters, the
            # 'ignore' keyword means any errors in the encoding
            # will leave the character as a ''

        
        # Puts data into a dictionary
        d = {}
        for i in range(0, len(items), 2):
            d[items[i]] = items[i+1].replace(',','')
        # print(d)
    
        # print('Elapsed time: ' + str(time.time() - start_time))
        return d

    # Retrieves data from NASDAQ Income Statement Page
    def get_data_nasdaq_income_statement(self, ticker: str) -> list:
        start_time = time.time()
        url = 'https://www.nasdaq.com/symbol/'+ ticker + \
            '/financials?query=income-statement'
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(class_= 'genTable') 
        # data is a list of all tags with the name genTable
        # there is only one item in the data list
        # data[0] is a tag object. These objects have MANY methods
        
        # text stores the relevant data in the form of a String
        # strip=True gets rid of the extra escape characters in the string (\n, etc)
        text = data[0].get_text(strip=True)
        # year1 stores the income statement data for the most recent year
        year1 = []
        year2 = []
        year3 = []
        year4 = []
        legend = ['Period Ending', 'Total Revenue', 'Gross Profit',\
                  'Research and Development' , 'Sales, General, and Admin,', \
                  'Non-Recurring Items', 'Other operating items', \
                  'Operating income', 'Addtnl income/expense items', \
                  'Earnings before interest and tax', 'Interest Expense', \
                  'Earnings Before Tax', 'Income Tax', 'Minority Interest', \
                  'Equity Earnings/Loss Unconsolidated Subsidiary', \
                  'Net income-cont. operations', 'Net income', \
                  'Net income appplicable to common shareholders']
        # print(len(legend))
        
        # Hardcoding method that uses regex, String methods, and index positions
        text = text.replace(',', '')
        # self.text = text
        pattern = re.compile(r'(\d*\d/\d\d/[2]\d\d\d)')
        # This pattern matches all the 
        matches = pattern.findall(text)
        # print(matches)
        # print('There is income statement data for ' + str(len(matches)) +' years')
        if (len(matches) % 4 != 0) or (len(matches) == 0):
            print('Incomplete income statement info. Your ticker may not be valid, \
                  or income statement data may not exist yet for your ticker.')    
        else:
            # Adds data to the list
            year1.append(matches[0])
            year2.append(matches[1])
            year2.append(matches[2])
            year3.append(matches[3])
       
        # Use Regular Expressions to get all dollar values into a list
        pattern = re.compile(r'\$(\d*)') #Keeps text starting with $, followed by digits
        matches = pattern.findall(text) #matches is now a list
        
        # Adds income statement values into appropiate year lists
        # WARNING: THIS ASSUMES THE COMPANY HAS INCOME STATEMENT INFORMATION FOR ALL 4 YEARS
        if (len(matches) % 4 != 0) or (len(matches) == 0):
            print('Incomplete income statement info. Your ticker may not be valid, \
                  or income statement data may not exist yet for your ticker.')
        else:
            # Adds data to the lists
            counter = 0
            values = len(matches)
            while counter < values:
                year1.append(matches[counter])
                year2.append(matches[counter+1])
                year3.append(matches[counter+2])
                year4.append(matches[counter+3])
                counter += 4
        # print('Successfully stored income statement information')
        # print(len(year1))
        
        # print('Elapsed time: ' + str(time.time() - start_time))
        return_list = (year1, year2, year3, year4)
        return return_list
         

def display_income_statement_data(list):
    data = webscraper.get_data_nasdaq_income_statement(ticker)
    legend = ['Period Ending', 'Total Revenue', 'Gross Profit',\
                  'Research and Development' , 'Sales, General, and Admin,', \
                  'Non-Recurring Items', 'Other operating items', \
                  'Operating income', 'Addtnl income/expense items', \
                  'Earnings before interest and tax', 'Interest Expense', \
                  'Earnings Before Tax', 'Income Tax', 'Minority Interest', \
                  'Equity Earnings/Loss Unconsolidated Subsidiary', \
                  'Net income-cont. operations', 'Net income', \
                  'Net income appplicable to common shareholders']
    for i in range(len(data[0]) - 1):
        print(legend[i])
        print(data[0][i])
        print(data[1][i])
        print(data[2][i])
        print(data[3][i])
    
if __name__ == '__main__':
    webscraper = Webscraper()
    print('Welcome! Start by typing in a stock ticker, such as AAPL, and then pressing enter');
    ticker = input("Type a stock ticker or type :q to exit: ")
    while(ticker != ":q"):
        print('Stock Summary: ')
        print(webscraper.get_data_nasdaq_summary(ticker))
        print('Income Statement Data: ')
        display_income_statement_data(webscraper.get_data_nasdaq_income_statement(ticker))
        print('\n')
        ticker = input("Type a stock ticker or type :q to exit: ")
    
