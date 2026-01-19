import argparse
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def capture_website(url: str, output_dir: str, device: str = "desktop"):
    """Veb-saytdan turli formatda screenshot olish"""
    
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"screenshot_{timestamp}"
    
    # Device sozlamalari
    devices = {
        "desktop": {"width": 1920, "height": 1080, "mobile": False},
        "laptop": {"width": 1366, "height": 768, "mobile": False},
        "tablet": {"width": 768, "height": 1024, "mobile": True},
        "mobile": {"width": 375, "height": 667, "mobile": True},
    }
    
    device_config = devices.get(device, devices["desktop"])
    
    logs = {
        "url": url,
        "device": device,
        "timestamp": timestamp,
        "events": [],
        "performance": {}
    }
    
    def log_event(msg: str):
        logs["events"].append({"time": datetime.now().isoformat(), "message": msg})
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox"]
        )
        
        context = browser.new_context(
            viewport={"width": device_config["width"], "height": device_config["height"]},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
            locale="en-US",
            is_mobile=device_config["mobile"],
            has_touch=device_config["mobile"],
        )
        
        page = context.new_page()
        
        # Event listener'lar
        page.on("console", lambda m: log_event(f"Console [{m.type}]: {m.text}"))
        page.on("pageerror", lambda e: log_event(f"Page Error: {e}"))
        page.on("requestfailed", lambda r: log_event(f"Request Failed: {r.url}"))
        
        start_time = datetime.now()
        
        try:
            # Sahifaga kirish
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            if response:
                log_event(f"Response: {response.status} - {response.url}")
                logs["status_code"] = response.status
        except PlaywrightTimeoutError:
            log_event("Timeout on page load")
        
        try:
            page.wait_for_load_state("networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            log_event("Timeout on networkidle")
        
        # Lazy-load uchun scroll
        try:
            for i in range(5):
                page.evaluate(f"window.scrollTo(0, {(i + 1) * 1000})")
                page.wait_for_timeout(500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
        except Exception as e:
            log_event(f"Scroll error: {e}")
        
        load_time = (datetime.now() - start_time).total_seconds()
        logs["performance"]["load_time"] = f"{load_time:.2f}s"
        
        # Screenshot'lar
        # 1. To'liq sahifa
        full_page_path = output_dir / f"{base_name}_full.png"
        page.screenshot(path=str(full_page_path), full_page=True)
        log_event(f"Full page screenshot saved: {full_page_path.name}")
        
        # 2. Viewport screenshot
        viewport_path = output_dir / f"{base_name}_viewport.png"
        page.screenshot(path=str(viewport_path), full_page=False)
        log_event(f"Viewport screenshot saved: {viewport_path.name}")
        
        # 3. Element screenshot (agar body bo'lsa)
        try:
            body = page.query_selector("body")
            if body:
                element_path = output_dir / f"{base_name}_body.png"
                body.screenshot(path=str(element_path))
                log_event(f"Body screenshot saved: {element_path.name}")
        except Exception as e:
            log_event(f"Body screenshot error: {e}")
        
        # Performance metrics
        try:
            metrics = page.evaluate("""() => {
                const timing = performance.timing;
                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    fullyLoaded: timing.loadEventEnd - timing.navigationStart,
                    domInteractive: timing.domInteractive - timing.navigationStart
                };
            }""")
            logs["performance"]["metrics"] = metrics
        except Exception as e:
            log_event(f"Metrics error: {e}")
        
        # Page info
        try:
            page_info = page.evaluate("""() => {
                return {
                    title: document.title,
                    url: window.location.href,
                    width: document.documentElement.scrollWidth,
                    height: document.documentElement.scrollHeight
                };
            }""")
            logs["page_info"] = page_info
        except Exception as e:
            log_event(f"Page info error: {e}")
        
        # HTML saqlash
        try:
            html = page.content()
            html_path = output_dir / f"{base_name}.html"
            html_path.write_text(html, encoding="utf-8")
            log_event(f"HTML saved: {html_path.name} ({len(html)} chars)")
        except Exception as e:
            log_event(f"HTML save error: {e}")
        
        context.close()
        browser.close()
    
    # Log saqlash
    log_path = output_dir / f"{base_name}_log.json"
    log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n✅ Screenshot muvaffaqiyatli olinadi!")
    print(f"📁 Papka: {output_dir}")
    print(f"🖼️  Full page: {full_page_path.name}")
    print(f"🖼️  Viewport: {viewport_path.name}")
    print(f"📄 HTML: {html_path.name}")
    print(f"📊 Log: {log_path.name}")
    print(f"⏱️  Vaqt: {load_time:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Veb-saytdan screenshot olish vositasi")
    parser.add_argument("url", help="Screenshot olinadigan URL")
    parser.add_argument("-o", "--output", default="screenshots", help="Chiqish papkasi (default: screenshots)")
    parser.add_argument(
        "-d", "--device", 
        choices=["desktop", "laptop", "tablet", "mobile"],
        default="desktop",
        help="Qurilma turi (default: desktop)"
    )
    
    args = parser.parse_args()
    capture_website(args.url, args.output, args.device)


# Ishlatish:
# python web_screenshot.py "https://example.com"
# python web_screenshot.py "https://example.com" -o my_screenshots -d mobile
