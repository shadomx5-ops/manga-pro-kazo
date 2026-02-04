import cloudscraper
from bs4 import BeautifulSoup
import json
import time

def start_scraping():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','mobile': False})
    url = "https://mangalek.com" 
    
    try:
        print("🚀 بدأت عملية السحب... يرجى الانتظار")
        res = scraper.get(url, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        manga_data = []

        items = soup.select('.page-item-detail, .manga-item')
        
        for index, item in enumerate(items):
            title_el = item.select_one('h3 a')
            img_el = item.select_one('img')
            chapter_el = item.select_one('.chapter a')

            if title_el and img_el:
                title = title_el.get_text(strip=True)
                m_url = title_el['href']
                img = img_el.get('data-src') or img_el.get('src') or ""
                if img.startswith('//'): img = "https:" + img
                
                chapter = chapter_el.get_text(strip=True) if chapter_el else "فصل جديد"
                
                manga_data.append({
                    "id": index + 1000,
                    "title": title,
                    "cover": img,
                    "url": m_url,
                    "chapter": chapter,
                    "rating": "4.9",
                    "age": "+13",
                    "timestamp": time.time(),
                    "translator": {"name": "Mohammed Elfagih", "insta": "Gremory807", "insta_url": "https://instagram.com/Gremory807"}
                })

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(manga_data, f, ensure_ascii=False, indent=2)
        print(f"✅ تم بنجاح! تم إنشاء ملف data.json")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    start_scraping()

