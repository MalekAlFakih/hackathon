from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np

class WebCarsCrawler:

  def __init__(self,company_name,urls) -> None:
     self.urls=urls
     self.company_name=company_name
     self.model=list()
     self.year=list()
     self.mileage=list()
     self.dealer_name=list()
     self.rating=list()
     self.review_count=list()
     self.price=list()
     self.color=list()
     self.fuel_type=list()
     self.transmission=list()
     self.mpg=list()
     self.company=list()

  
  def getPage(self, url):
    try:
      req = requests.get(url)
    except requests.exceptions.RequestException:
      return None
    return BeautifulSoup(req.text, 'lxml')
  
  def scrape(self):
    print(50*'--')
    print(f'Scrapping {20*len(urls)} ads')
    print(50*'--')
    for url in self.urls:
      bs=self.getPage(url)
      cars=bs.find_all('div', {'class' : 'vehicle-card'})##Finding car ads
      for car in cars:

        # name
        name=car.find('h2').get_text()
        try:
          self.year.append(int(name.split()[0]))
        except:
          self.year.append(np.nan)
        self.company.append(self.company_name)
        try:
          self.model.append(name[4+len(self.company_name)+2:])
        except:
          self.model.append(np.nan)


        # mileage
        try:
            self.mileage.append(float((car.find('div', {'class':'mileage'}).get_text()).split()[0].replace(',','.')))
        except:
            self.mileage.append(np.nan)

        # dealer_name
        try:
            self.dealer_name.append(car.find('div', {'class':'dealer-name'}).get_text().strip())
        except:
            self.dealer_name.append(np.nan)

        # rating
        try:
            self.rating.append(float(car.find('span', {'class':'sds-rating__count'}).get_text()))
        except:
            self.rating.append(np.nan)

        # review_count
        try:
            self.review_count.append(float((car.find('span', {'class':'sds-rating__link'}).get_text()).strip('reviews)').strip('(').strip().replace(',','.')))
        except:
            self.review_count.append(np.nan)

        #price 
        try:
            self.price.append(float(car.find('span', {'class':'primary-price'}).get_text().strip('$').replace(',','.')))
        except:
            self.price.append(np.nan)

        details_url='https://www.cars.com'+car.find('a',{'class':"vehicle-card-visited-tracking-link"}).attrs['href']
        #print(details_url)
        self.innerScrape(details_url)

    print(50*'--')
    print('Scrap Finished Successfully ')
    print(50*'--')
    
  def innerScrape(self,url):
    bs=self.getPage(url)
    
    content=bs.find('div',{'class':'basics-content-wrapper'})
    basics=content.find_all('dd')
    self.color.append(basics[0].get_text())
    self.mpg.append(basics[3].get_text().split()[0])
    self.fuel_type.append(basics[4].get_text())
    self.transmission.append(basics[5].get_text())
    
  def createDataset(self):
    self.scrape()
    car_df = pd.DataFrame({'Company': self.company,'Model':self.model,'Year':self.year, 'Mileage(mi)':self.mileage, 'Dealer Name':self.dealer_name,
                              'Rating': self.rating, 'Review Count': self.review_count,'Color':self.color,'MPG':self.mpg,'Fuel Type':self.fuel_type,'Transmission':self.transmission ,'Price': self.price})
    return car_df

company_name='Mercedes-Benz'
urls=['https://www.cars.com/shopping/results/?page='+ str(i) +'&page_size=20&dealer_id=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=20&mileage_max=&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip=' for i in range(2)]
crawler=WebCarsCrawler(company_name,urls)

df=crawler.createDataset()
df.to_csv('car_df.csv',index=False)

