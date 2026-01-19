# Web Screenshot Tool

Veb-saytlardan turli qurilmalar uchun screenshot olish va performance ma'lumotlarini yig'ish vositasi.

## O'rnatish

```bash
pip install playwright
playwright install chromium
```

## Ishlatish

### Asosiy ishlatish

```bash
python web_screenshot.py "https://example.com"
```

### Qurilma turini tanlash

```bash
# Desktop (1920×1080)
python web_screenshot.py "https://example.com" -d desktop

# Laptop (1366×768)
python web_screenshot.py "https://example.com" -d laptop

# Tablet (768×1024)
python web_screenshot.py "https://example.com" -d tablet

# Mobile (375×667)
python web_screenshot.py "https://example.com" -d mobile
```

### Chiqish papkasini belgilash

```bash
python web_screenshot.py "https://example.com" -o my_screenshots -d mobile
```

## Parametrlar

- `url` - screenshot olinadigan sahifa manzili (majburiy)
- `-o, --output` - chiqish papkasi (default: `screenshots`)
- `-d, --device` - qurilma turi: desktop, laptop, tablet, mobile (default: `desktop`)

## Natija

Har bir ishga tushirishda quyidagi fayllar yaratiladi:

```
screenshots/
├── screenshot_20240119_143025_full.png      # To'liq sahifa
├── screenshot_20240119_143025_viewport.png  # Viewport qismi
├── screenshot_20240119_143025_body.png      # Body elementi
├── screenshot_20240119_143025.html          # HTML kod
└── screenshot_20240119_143025_log.json      # Batafsil log
```

### Log fayli tarkibi

```json
{
  "url": "https://example.com",
  "device": "mobile",
  "timestamp": "20240119_143025",
  "status_code": 200,
  "performance": {
    "load_time": "2.45s",
    "metrics": {
      "domContentLoaded": 1200,
      "fullyLoaded": 2450,
      "domInteractive": 1100
    }
  },
  "page_info": {
    "title": "Example Domain",
    "url": "https://example.com/",
    "width": 375,
    "height": 2340
  },
  "events": [...]
}
```

## Xususiyatlar

- ✅ 4 xil qurilma emulation (desktop, laptop, tablet, mobile)
- ✅ 3 turdagi screenshot (full, viewport, body)
- ✅ Performance metrics (yuklash vaqti, DOM events)
- ✅ Console va error loglar
- ✅ HTML kod saqlash
- ✅ Lazy-load rasmlarni avtomatik yuklash
- ✅ Touch screen emulation mobile uchun
- ✅ Timestamp bilan noyob fayl nomlari
- ✅ JSON formatda batafsil hisobot

## Konfiguratsiya

Kodda o'zgartirish mumkin bo'lgan parametrlar:

### Qurilma o'lchamlari

```python
devices = {
    "desktop": {"width": 1920, "height": 1080, "mobile": False},
    "laptop": {"width": 1366, "height": 768, "mobile": False},
    "tablet": {"width": 768, "height": 1024, "mobile": True},
    "mobile": {"width": 375, "height": 667, "mobile": True},
}
```

### Timeout sozlamalari

```python
# Sahifa yuklash timeout
timeout=60000  # 60 soniya

# Network idle timeout
timeout=30000  # 30 soniya

# Scroll kutish vaqti
page.wait_for_timeout(500)  # 500ms
```

### Scroll parametrlari

```python
# Scroll takrorlash soni
for i in range(5):  # 5 marta
    page.evaluate(f"window.scrollTo(0, {(i + 1) * 1000})")
```

## Foydalanish holatlari

### Responsive dizaynni tekshirish

```bash
# Barcha qurilmalarda screenshot olish
python web_screenshot.py "https://mysite.com" -d desktop -o test_desktop
python web_screenshot.py "https://mysite.com" -d tablet -o test_tablet
python web_screenshot.py "https://mysite.com" -d mobile -o test_mobile
```

### Performance monitoring

```bash
# Log faylidan yuklash vaqtini tekshirish
python web_screenshot.py "https://example.com"
cat screenshots/screenshot_*_log.json | grep load_time
```

### Avtomatik testing

```bash
# Bash script ichida ishlatish
for url in "site1.com" "site2.com" "site3.com"; do
    python web_screenshot.py "https://$url" -o "test_$url"
done
```

## Muammolarni hal qilish

### Screenshot olinmayapti

1. **_log.json** faylini tekshiring - qanday xatolar bor?
2. Timeout vaqtini oshiring
3. Internet aloqani tekshiring
4. URL to'g'ri ekanligini tasdiqlang

### Rasmlar yuklanmayapti

- Scroll sonini oshiring: `range(10)`
- Har bir scroll orasidagi vaqtni oshiring: `wait_for_timeout(1000)`

### Mobile emulation ishlamayapti

- `is_mobile=True` va `has_touch=True` sozlamalarini tekshiring
- User-Agent mobile versiyasini o'rnating

### Performance metrics bo'sh

- Sahifa JavaScript ishlatmayotgan bo'lishi mumkin
- `performance.timing` API qo'llab-quvvatlanmayotgan bo'lishi mumkin

### Juda katta fayllar

- Screenshot formatini o'zgartiring (PNG o'rniga JPEG)
- Quality parametrini qo'shing: `quality=80`
- Full page o'rniga faqat viewport screenshot oling

## Kengaytirish

### Yangi qurilma qo'shish

```python
devices = {
    # ... mavjud qurilmalar
    "iphone": {"width": 390, "height": 844, "mobile": True},
    "ipad": {"width": 1024, "height": 1366, "mobile": True},
}
```

### PDF qo'shish

```python
# Screenshot'lardan keyin
pdf_path = output_dir / f"{base_name}.pdf"
page.pdf(path=str(pdf_path), format="A4", print_background=True)
```

### Dark mode screenshot

```python
context = browser.new_context(
    color_scheme="dark",  # qo'shish
    # ... boshqa parametrlar
)
```

## Talablar

- Python 3.7+
- Playwright
- Chromium browser
