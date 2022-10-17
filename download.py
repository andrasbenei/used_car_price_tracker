import requests
from bs4 import BeautifulSoup
import pandas as pd


# Download data with BeautifulSoup

url = "https://www.hasznaltauto.hu/talalatilista/PCOG2VG3R3RDADH5S56ACLNXTHYLQKZUJAVTJUSK6NNBS2SKNAJKGJFNAYIP7PSOLOMLNS2TVVRTXNUPR4FXF6RON5PCNKIUEUCCZSBJ3BRC2VUMEVJPQKY22QL2QARV2BGAVUGDYBWYOH4VZMY2BLZBA57RLK45TR2I7VAMNNYJSUJWHYZJCQUMHXYN356MUXAMUZMDXTWSWR2MPPLOPKQWOTEE5YCM2W6CGROSPSLVEFHAYDXBK2HFL4CKI4KS2BSF76FY4YHB32RDAZ5OC7UXQL5SHLYCQ2ID3SUMNGQTLHACTQPDQD324AEZRKCNJYOZMPFR33AH34BRFRH6HUCXHL4NQAFXT3HJWTW6YY57RZO54GDTRZXHQMGP4RKXVM67UALRT7DYWI73UVZOZOSJXHYL54UBZQP6LQ5HENBUDEO54SWXXULEPVW3MHIVSMDRLSVPLWN2G3FRKY5KA2ZTXA4QHLUEJTSTC5WK6TGRNUMK7RIY4WTXDZXCQWN4FVCZWE6UXHZCPVBD3VQM3C4A6BIBJZ5ESMSP3T63VKVPDJUNS6USWVONVPJN36GM32A3KHKCNHDPEHFYA35OJFRLXYF3AFZITYVQDLPBJRA2YQGO4VG3LYTPISRGJUW2NG2NHVU6IZ55VWVTNDHVVG2XPFTYH6JZUIW5AVJORQNRX6UGS7BS7MGQVDGFRTQGP2DKYND2DSQDYBHTVLIVZKMMJVZ5JLNBHTPLVAIAPWKXGMDZP4W7SDWK73FBO4PDORIN6AY5GCFBVSYQKXRTHWDJDASMKGV2MJMVWNMCAONHHLB5PCW3TTJI3JVUT5SS6564YBH2OMP6CRTLWJ2CIR2FD5P3N7Y2H3HD5SSXKFVGKYCQR5B3SGW2BP5OYQFOABWXU7O6LOJFT7N7NFPRTNF5M3X76AB3RGTXS"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

# Define empty lists

price_list = []
description = []
link = []
fuel_type = []
year = []
engine_size = []
power_HP = []
power_KW = []
mileage = []

# Define function to update the lists

def update_lists(document):

    prices = doc.find_all(attrs={"class":"talalatisor-vetelar-mobil visible-xs-block"})

    for price in prices:
        price_text = price.get_text()
        try:
            price_number = int(''.join(c for c in price_text if (c.isdigit() or c =='.')))
        except ValueError:
            price_number = 0
        price_list.append(price_number)

    desc_list = doc.find_all('span', attrs={'class': 'parking-button-on-mobile'})

    for i in desc_list:
        text = i.parent.find('h3')
        description.append(text.get_text())
        link.append(text.find('a').get('href'))

    car_info = doc.find_all(attrs={"class":"talalatisor-info adatok"})
    for i in car_info:
        info_line = i.get_text()
        splitted_info_line = info_line.split(',')

        validate_info_line(splitted_info_line)

        fuel_type.append(splitted_info_line[0])
        year.append(splitted_info_line[1][1:5])

        engine_data = (splitted_info_line[2][:-1])
        engine_data_cleared = int(''.join(c for c in engine_data if (c.isdigit() or c =='.')))
        engine_size.append(engine_data_cleared)

        power_KW_data = (splitted_info_line[3])
        power_KW_data_cleared = int(''.join(c for c in power_KW_data if (c.isdigit() or c =='.')))
        power_KW.append(power_KW_data_cleared)

        power_HP_data = (splitted_info_line[4])
        power_HP_data_cleared = int(''.join(c for c in power_HP_data if (c.isdigit() or c =='.')))
        power_HP.append(power_HP_data_cleared)

        mileage_data = (splitted_info_line[5])
        mileage_data_cleared = int(''.join(c for c in mileage_data if (c.isdigit() or c =='.')))
        mileage.append(mileage_data_cleared)

# Define validation function because some of the advertisements doesn't contain all of the data

def validate_info_line(splitted_info_line):

    if any(char.isdigit() for char in splitted_info_line[0]):
        splitted_info_line.insert(0, "NA")

    if any(char.isalpha() for char in splitted_info_line[1][1:5]):
        splitted_info_line.insert(1, "1000")

    if splitted_info_line[2][-3:] != "cm³":
        splitted_info_line.insert(2, "0\xa0000 cm³")

    if splitted_info_line[3][-2:] != "kW":
        splitted_info_line.insert(3, "0\xa0kW")
    
    if splitted_info_line[4][-2:] != "LE":
        splitted_info_line.insert(4, "0\xa0LE")

    if len(splitted_info_line) == 6:
        if splitted_info_line[5][-2:] != "km":
            splitted_info_line.insert(5, "0\xa0000\xa0km")
    else:
        splitted_info_line.insert(5, "0\xa0000\xa0km")

    return splitted_info_line


# Call the function to update the lists. Repeat calling in case of more pages

update_lists(doc)

last_page = doc.find(class_="last").get_text()

for i in range(int(last_page)-1):
    next_page = doc.find(rel="next").get('href')
    url = next_page
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')

    update_lists(doc)
    
# Creating the Dataframe        

car_data = {'Price': price_list, 'Year': year, 'Power(HP)': power_HP, 'Mileage': mileage, 'Description': description, 'Link': link, 'Fuel_type': fuel_type}

car_data_df = pd.DataFrame(car_data)

# Save the results

car_data_df.to_csv('data.csv', index=False)