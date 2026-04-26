"""HTML 파일을 PNG로 렌더링한다.

사용법:
    python html_to_png.py <html_path> <png_path> [--selector .diagram] [--width 1200]
"""
import argparse
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_png(html_path: str, png_path: str, selector: str = None, width: int = 1200) -> int:
    abs_html = Path(html_path).resolve()
    url = abs_html.as_uri()

    Path(png_path).parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": 900},
            device_scale_factor=2,
        )
        page.goto(url)
        page.wait_for_load_state("networkidle")

        if selector:
            target = page.locator(selector).first
            target.screenshot(path=png_path)
        else:
            page.screenshot(path=png_path, full_page=True)

        browser.close()

    return os.path.getsize(png_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html_path")
    parser.add_argument("png_path")
    parser.add_argument("--selector", default=None, help="CSS selector to capture (default: full page)")
    parser.add_argument("--width", type=int, default=1200)
    args = parser.parse_args()

    size = html_to_png(args.html_path, args.png_path, args.selector, args.width)
    print(f"OK: {args.png_path} ({size // 1024} KB)")


if __name__ == "__main__":
    main()
