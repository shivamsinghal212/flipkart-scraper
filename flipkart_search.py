from flipkart_root import Scrapper

'''
To use scraper, use initialize() function. It fetches the data in data-frame format.
'''
print('Enter item you want to search:')
search = input()
obj = Scrapper(search)


def write_to_excel(dataframe):
    dataframe.to_excel('test.xlsx', sheet_name='sheet1', index=False)
    return dataframe


df = obj.initialize()
write_to_excel(df)
