# Carsome Scraper


## Instalasi
1. Buat Virtual Environment<br/> 
    - `pip install virtualenv`
    - `virtualenv .venv`  
    
2. Lakukan aktivasi virtual environment
    - `source .venv/bin/activate`

3. Install dependensi
    - `pip install -r requirements.txt`

4. Jalankan file 
    - `python carsome.py "filter" `
   
    Ubah "filter" sesuai dengan Brand atau Keyword yang diinginkan atau dikosongi jika ingin scraping semua tanpa keyword. <br/>
    Contoh: `python carsome.py Daihatsu` 
            `python carsome.py` (Scraping tanpa filter)
 
8. Matikan virtual environment
    - `deactivate`
