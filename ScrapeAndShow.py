import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#Display
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, LCD_FONT



def run():
	headers = {'user-agent':'Mozilla/5.0 \ (Windows NT 10.0; Win64; x64) \ AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/84.0.4147.105 Safari/537.36'}
	i=0
	urls = [ 
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DE0007037129&name=rwe-ag-inh-on&token=72af16c5d77a5a446a92daeb8f5562ff',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=US0079031078&name=advanced-micdev-dl-01&token=871989097dea105cfa01f3b6936c5ee9',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DE0005664809&name=evotec-se-inh-on&token=6d280a51d1200898beba7d29039d1ead',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=US79466L3024&name=salesforce-inc-dl-001&token=51545fb92ee3da169b4b9607240b4b99',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DE000ENER6Y0&name=siemens-energy-ag-na-on&token=92828ebbee2b1e59d421244da14d8791',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=US69608A1088&name=palantir-technologies-inc&token=f513aed5476edde91a3d608cf8aa543a',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DE0005557508&name=dttelekom-ag-na&token=be89f5b6c64ba633f5ea85ec88f9f73b',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DE000TUAG505&name=tui-ag-na-on&token=f3e54a866239ce34aaafc549bc1d1ec0',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=DK0062498333&name=novo-nordisk-as-b-dk-01&token=bb78bdff423a77cbddf1176601e1cdac',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=NL0015000GX8&name=envipco-hldg-cva-b&token=7e070306c8240d658d48f2abeda9ce1d',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=US5949181045&name=microsoft-dl-00000625&token=9986d08f459cea28690ff398ac7d190a',
		'https://www.gettex.de/gettex-die-guenstige-und-schnelle-boerse/?isin=CNE100000296&name=byd-co-ltd-h-yc-1&token=b9e59c4e04077f83475cd2560f66f1a8'
		] 
	for url in urls:
		all=[]
		list=['RWE','AMD','EVOTEC','SALESFORCE','SIEMENS ENERGY','PALANTIER','DT TELEKOM','TUI','NOVO','ENVIPCO','MSFT','BYD'] #Shortname List for Matrix Display
		
		page = requests.get(url,headers=headers) 
		try: 
			soup = BeautifulSoup(page.text, 'html.parser') 
			aktie = soup.find('h1', {'class': 'stock-title h1'}).text.strip()
			price = soup.find('div', {'class': 'stock-details pull-left'}).find_all('span')[1].text.strip('\n \u00a0\u20ac\u20ac')
			time = soup.find('div', {'class': 'stock-details pull-left'}).find_all('span')[0].text.strip('\n \u00a0\u20ac\u20ac LETZTER KURS ( ): \\// ')
			change = soup.find('div', {'class': 'text-right'}).text.strip('\n \u00a0\u20ac\u20ac')
			x=[aktie,price,change,time]
			pricelcd = list[i] + " : " + price
			print(i)
			i =i+1
			all.append(x)

		except AttributeError: print("Change the Element id")

		column_names = ["Aktie", "Price", "Change", "Time"]
		df = pd.DataFrame(columns = column_names, data=all)
		df['Price'] = df['Price'].str[:-1]
		df['Change'] = df['Change'].str[:-1]
		df['Date'] = df['Time'].str[:-8]
		df['Time'] = df['Time'].str[13:]
		df['Combined'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
		df.to_string()
		aktiennamejson = aktie + '.json'
		aktiennamecsv = aktie + '.csv'
		df.to_json(aktiennamejson, mode="a", lines=True, orient='records',)
		df.to_csv(aktiennamecsv, mode="a",index_label='Record', header=False, encoding='utf-8', sep=';')

		# create matrix device
		serial = spi(port=0, device=0, gpio=noop())
		device = max7219(serial, cascaded=4, block_orientation=-90, contrast=150)

		show_message(device, pricelcd, fill="white", font=proportional(LCD_FONT), scroll_delay=0.06)

while True:
	run()
	time.sleep(60)
