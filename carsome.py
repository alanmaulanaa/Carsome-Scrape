from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os
import sys
from time import sleep

servis = Service('chromedriver.exe')
driver = webdriver.Chrome()
driver.maximize_window()

sleep(4)
website = "https://www.carsome.id/beli-mobil-bekas"
driver.get(website)

try:
    closex = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/main/div/div/div[1]/div[2]/div[2]/div/div[1]/img"))
    )
    closex.click()

except NoSuchElementException:
    pass 

except Exception as e:
    pass

sleep(2)
car_detail = []
tahun_list = []
merk_list = []
nama_list = []
km_list = []
tipe_list = []
lokasi_list = []
harga_list = []
cicilan_list = []
cash_list = []

filterinto = sys.argv[1]  # Isi pencarian tertentu

if filterinto:
    url = f"https://www.carsome.id/beli-mobil-bekas?keywords={filterinto}"
    driver.get(url)
else:
    driver.get("https://www.carsome.id/beli-mobil-bekas")

def scrape_car_details():
    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mod-b-card__footer'))
        )

        elements = driver.find_elements(By.CLASS_NAME, 'mod-b-card__footer')
        
        for element in elements:
            if element.text not in car_detail:
                car_detail.append(element.text)

    except TimeoutException:
        print("Page not loaded within 10 seconds")

    except Exception as e:
        print(f"Error scraping data: {e}")

# Initialize an empty list to store car details
car_detail = []

# Call the function to scrape car details
scrape_car_details()

while True:
    try:
        # Find the "Next page" button
        next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next page']")

        # Check if the "Next page" button is clickable
        if next_button.is_enabled():
            next_button.click()
            sleep(7)  # Wait for 7 seconds for the next page to load
            
            # Call the function to scrape car details for the next page
            scrape_car_details()
        else:
            print("No more pages to load")
            break

    except NoSuchElementException:
        print("No more pages to load")
        break

    except Exception as e:
        print(f"Error navigating pages: {e}")
        break

len(car_detail)

splitter = [item.split('\n') for item in car_detail]

tahun_list = [item[0].split()[0] for item in splitter]
merk_list = [' '.join(item[0].split()[1:]) for item in splitter]

nama_list = [item[1] for item in splitter]
km_list = [item[2] for item in splitter]
tipe_list = [item[3] for item in splitter]
lokasi_list = [item[4] for item in splitter]
harga_list = [item[5] for item in splitter]
cicilan_list = [item[6] for item in splitter]
cash_list = [item[7] for item in splitter]

path = os.getcwd()
path = os.path.join(path, "scraping Carsome.id")
if not os.path.exists(path):
    os.mkdir(path)
    print(f"Directory {path} created.")
else:
    print(f"Directory {path} already exists.")
driver.execute_script("window.scrollTo(0, 0);")
sleep(2)

df = pd.DataFrame({
    'Brand': merk_list,
    'Tahun':tahun_list,
    'Nama': nama_list,
    'Lokasi': lokasi_list,
    'Harga': harga_list,
    'Harga Cicilan': cicilan_list,
    'Cash':cash_list,
})

if not filterinto:
    excel_file_path = os.path.join(path, 'Hasil Output.xlsx')
else:
    excel_file_path = os.path.join(path, filterinto + '.xlsx')
df.to_excel(excel_file_path, index=False)

print('Scraping telah selesai')
print(f"Silahkan cek pada folder {path}")

driver.quit()