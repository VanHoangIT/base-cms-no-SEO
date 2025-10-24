#!/usr/bin/env python3
"""
CSS Build System - Tách và gộp CSS tự động cho Flask Project
Author: BRICON Web Development Team
Usage: python build_css.py [command]
pip install watchdog
"""

import os
import re
from pathlib import Path
from datetime import datetime

# ==================== CẤU HÌNH DỰ ÁN ====================
BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = BASE_DIR / 'app' / 'static'
CSS_DIR = STATIC_DIR / 'css'
MODULES_DIR = CSS_DIR / 'modules'
INPUT_FILE = CSS_DIR / 'style.css'
OUTPUT_FILE = CSS_DIR / 'main.min.css'

# ==================== CẤU TRÚC MODULE CSS ====================
CSS_MODULES = {
    '01-reset.css': {
        'start': '/* ==================== GLOBAL RESET ==================== */',
        'end': '/* ==================== NAVBAR ENHANCEMENTS ==================== */',
        'description': 'CSS Reset & Global Styles'
    },
    '02-navbar.css': {
        'start': '/* ==================== NAVBAR ENHANCEMENTS ==================== */',
        'end': '/* ==================== TOP BAR ==================== */',
        'description': 'Navigation Bar Styles'
    },
    '03-topbar.css': {
        'start': '/* ==================== TOP BAR ==================== */',
        'end': '/* ==================== BANNER  ==================== */',
        'description': 'Top Bar Styles'
    },
    '04-banner.css': {
        'start': '/* ==================== BANNER  ==================== */',
        'end': '/* ==================== PRODUCT CARD ==================== */',
        'description': 'Banner Carousel Styles'
    },
    '05-product-card.css': {
        'start': '/* ==================== PRODUCT CARD ==================== */',
        'end': '/* ==================== BLOG CARD ==================== */',
        'description': 'Product Card Component'
    },
    '06-blog-card.css': {
        'start': '/* ==================== BLOG CARD ==================== */',
        'end': '/* ==================== SECTION TITLE ==================== */',
        'description': 'Blog Card Component'
    },
    '07-section-title.css': {
        'start': '/* ==================== SECTION TITLE ==================== */',
        'end': '/* ==================== FILTER SIDEBAR ==================== */',
        'description': 'Section Title Styles'
    },
    '08-filter-sidebar.css': {
        'start': '/* ==================== FILTER SIDEBAR ==================== */',
        'end': '/* ==================== FLOATING ACTION BUTTONS ==================== */',
        'description': 'Filter Sidebar Component'
    },
    '09-floating-buttons.css': {
        'start': '/* ==================== FLOATING ACTION BUTTONS ==================== */',
        'end': '/* ==================== PAGE HEADER ==================== */',
        'description': 'Floating Action Buttons'
    },
    '10-page-header.css': {
        'start': '/* ==================== PAGE HEADER ==================== */',
        'end': '/* ==================== PAGINATION ==================== */',
        'description': 'Page Header Styles'
    },
    '11-pagination.css': {
        'start': '/* ==================== PAGINATION ==================== */',
        'end': '/* ==================== FOOTER ==================== */',
        'description': 'Pagination Component'
    },
    '12-footer.css': {
        'start': '/* ==================== FOOTER ==================== */',
        'end': '/* ==================== UTILITY ANIMATIONS ==================== */',
        'description': 'Footer Styles'
    },
    '13-animations.css': {
        'start': '/* ==================== UTILITY ANIMATIONS ==================== */',
        'end': '/* ==================== BUTTONS ENHANCEMENT ==================== */',
        'description': 'CSS Animations'
    },
    '14-buttons.css': {
        'start': '/* ==================== BUTTONS ENHANCEMENT ==================== */',
        'end': '/* ==================== CUSTOM SCROLLBAR',
        'description': 'Button Styles'
    },
    '15-scrollbar.css': {
        'start': '/* ==================== CUSTOM SCROLLBAR',
        'end': '/* ==================== ALERT MESSAGES ==================== */',
        'description': 'Custom Scrollbar'
    },
    '16-alerts.css': {
        'start': '/* ==================== ALERT MESSAGES ==================== */',
        'end': '/* ==================== LOADING STATES ==================== */',
        'description': 'Alert Messages'
    },
    '17-loading.css': {
        'start': '/* ==================== LOADING STATES ==================== */',
        'end': '/* ==================== GIỚI THIỆU PAGE ==================== */',
        'description': 'Loading States'
    },
    '18-about-page.css': {
        'start': '/* ==================== GIỚI THIỆU PAGE ==================== */',
        'end': '/* ==================== FEATURED PROJECTS CAROUSEL ==================== */',
        'description': 'About Page Styles'
    },
    '19-featured-projects.css': {
        'start': '/* ==================== FEATURED PROJECTS CAROUSEL ==================== */',
        'end': '/* ==================== SCROLL TO TOP BUTTON WITH PROGRESS ==================== */',
        'description': 'Featured Projects Carousel'
    },
    '20-scroll-to-top.css': {
        'start': '/* ==================== SCROLL TO TOP BUTTON WITH PROGRESS ==================== */',
        'end': '/* ==================== FORCE GRAY SCROLLBAR - OVERRIDE ALL ==================== */',
        'description': 'Scroll to Top Button'
    },
    '21-scrollbar-override.css': {
        'start': '/* ==================== FORCE GRAY SCROLLBAR - OVERRIDE ALL ==================== */',
        'end': '/* ==================== RETURN & REFUND POLICY STYLES ==================== */',
        'description': 'Scrollbar Override'
    },
    '22-policy-page.css': {
        'start': '/* ==================== RETURN & REFUND POLICY STYLES ==================== */',
        'end': '/* ==================== FORCE ROUND DOTS - MUST BE AT END OF FILE ==================== */',
        'description': 'Policy Page Styles'
    },
    '23-carousel-dots.css': {
        'start': '/* ==================== FORCE ROUND DOTS - MUST BE AT END OF FILE ==================== */',
        'end': '/* ==================== BREADCRUMB STYLES ==================== */',
        'description': 'Carousel Dots Override'
    },
    '24-breadcrumb.css': {
        'start': '/* ==================== BREADCRUMB STYLES ==================== */',
        'end': ' /* Skip Link */',
        'description': 'Breadcrumb Navigation'
    },
    '25-accessibility.css': {
        'start': ' /* Skip Link */',
        'end': '/* ============ CHATBOT WIDGET',
        'description': 'Accessibility Features'
    },
    '26-chatbot.css': {
        'start': '/* ============ CHATBOT WIDGET',
        'end': '/* ==================== PROJECT FILTER BUTTONS',
        'description': 'Chatbot Widget'
    },
    '27-project-filters.css': {
        'start': '/* ==================== PROJECT FILTER BUTTONS',
        'end': '/* ==================== ABOUT COMPANY SECTION',
        'description': 'Project Filter Buttons'
    },
    '28-about-company-section.css': {
        'start': '/* ==================== ABOUT COMPANY SECTION',
        'end': None,
        'description': 'CSS của about ở trang index'
    }
}


def print_header(title):
    """In header đẹp"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_success(message):
    """In thông báo thành công"""
    print(f"✅ {message}")


def print_error(message):
    """In thông báo lỗi"""
    print(f"❌ {message}")


def print_info(message):
    """In thông báo thông tin"""
    print(f"ℹ️  {message}")


def print_warning(message):
    """In thông báo cảnh báo"""
    print(f"⚠️  {message}")


def extract_css_section(content, start_marker, end_marker):
    """Trích xuất section CSS giữa 2 marker"""
    if not start_marker:
        return ""

    start_idx = content.find(start_marker)
    if start_idx == -1:
        return ""

    if end_marker:
        end_idx = content.find(end_marker, start_idx)
        if end_idx == -1:
            return content[start_idx:]
        return content[start_idx:end_idx]

    return content[start_idx:]


def minify_css(css_content):
    """Minify CSS - loại bỏ comments và khoảng trắng thừa"""
    # Giữ lại comment đầu tiên (header info)
    first_comment = re.search(r'/\*.*?\*/', css_content, flags=re.DOTALL)
    header = first_comment.group(0) if first_comment else ""

    # Loại bỏ tất cả comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    # Loại bỏ khoảng trắng thừa
    css_content = re.sub(r'\s+', ' ', css_content)
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    css_content = re.sub(r';\s*}', '}', css_content)

    # Loại bỏ dòng trống
    css_content = re.sub(r'\n\s*\n', '\n', css_content)

    return (header + "\n" + css_content.strip()) if header else css_content.strip()


def split_css(input_file):
    """Tách file CSS lớn thành các module nhỏ"""
    print_header("🎨 TÁCH FILE CSS THÀNH CÁC MODULE")

    if not input_file.exists():
        print_error(f"Không tìm thấy file: {input_file}")
        return False

    print_info(f"Đọc file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tạo thư mục modules
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    print_success(f"Tạo thư mục: {MODULES_DIR}")

    print(f"\n📦 Đang tách thành {len(CSS_MODULES)} module...\n")

    total_lines = 0
    total_size = 0

    for filename, config in CSS_MODULES.items():
        section = extract_css_section(content, config['start'], config['end'])

        if section:
            output_path = MODULES_DIR / filename

            # Thêm header cho mỗi module
            header = f"""/* ==================== {config['description'].upper()} ====================
 * File: {filename}
 * Auto-generated from style.css
 * Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * ========================================================================== */

"""

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(header + section)

            lines = len(section.split('\n'))
            size = len(section) / 1024
            total_lines += lines
            total_size += size

            print(f"  {filename:32s} | {lines:5d} dòng | {size:7.1f} KB | {config['description']}")
        else:
            print_warning(f"{filename:32s} | Không tìm thấy nội dung")

    print(f"\n{'─' * 70}")
    print(f"  Tổng cộng: {len(CSS_MODULES)} files | {total_lines:5d} dòng | {total_size:7.1f} KB")
    print(f"{'─' * 70}")

    print_success(f"Hoàn tất! Module được lưu tại: {MODULES_DIR}")
    return True


def build_css():
    """Gộp tất cả module thành main.min.css"""
    print_header("🔨 BUILD MAIN.MIN.CSS")

    if not MODULES_DIR.exists():
        print_error(f"Thư mục {MODULES_DIR} không tồn tại!")
        print_info("Chạy: python build_css.py split")
        return False

    combined_css = []
    total_size = 0
    module_count = 0

    print("📦 Đang gộp các module...\n")

    # Đọc các module theo thứ tự
    for filename in sorted(CSS_MODULES.keys()):
        file_path = MODULES_DIR / filename

        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_css.append(content)
                size = len(content) / 1024
                total_size += size
                module_count += 1
            print(f"  ✓ {filename:32s} | {size:7.1f} KB")
        else:
            print_warning(f"Không tìm thấy: {filename}")

    # Tạo header cho file build
    build_header = f"""/*! 
 * ============================================================================
 * BRICON - Main CSS Build
 * ============================================================================
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * Modules: {module_count} files
 * Description: Auto-generated minified CSS
 * DO NOT EDIT THIS FILE DIRECTLY - Edit individual modules instead
 * ============================================================================
 */

"""

    # Gộp và minify
    full_css = '\n\n'.join(combined_css)
    minified_css = minify_css(full_css)
    final_css = build_header + minified_css

    # Ghi file output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_css)

    # Thống kê
    original_kb = total_size
    minified_kb = len(final_css) / 1024
    saved_kb = original_kb - minified_kb
    saved_percent = (saved_kb / original_kb) * 100 if original_kb > 0 else 0

    print(f"\n{'─' * 70}")
    print(f"  📊 Thống kê Build:")
    print(f"     • Kích thước gốc:    {original_kb:8.1f} KB")
    print(f"     • Kích thước minify: {minified_kb:8.1f} KB")
    print(f"     • Tiết kiệm:         {saved_kb:8.1f} KB ({saved_percent:.1f}%)")
    print(f"{'─' * 70}")

    print_success(f"Build thành công: {OUTPUT_FILE}")
    return True


def watch_and_build():
    """Watch mode - tự động build khi có thay đổi"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print_error("Cần cài đặt watchdog!")
        print_info("Chạy: pip install watchdog")
        return

    class CSSChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith('.css') and 'main.min.css' not in event.src_path:
                print(f"\n🔄 Phát hiện thay đổi: {Path(event.src_path).name}")
                build_css()

    print_header("👀 WATCH MODE - Tự động build khi có thay đổi")
    print_info(f"Đang theo dõi: {MODULES_DIR}")
    print_info("Nhấn Ctrl+C để dừng...\n")

    event_handler = CSSChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, str(MODULES_DIR), recursive=False)
    observer.start()

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n")
        print_info("Đã dừng watch mode")

    observer.join()


def show_help():
    """Hiển thị hướng dẫn sử dụng"""
    print_header("📖 HƯỚNG DẪN SỬ DỤNG CSS BUILD SYSTEM")

    print("🔧 Các lệnh có sẵn:\n")

    commands = [
        ("python build_css.py", "Tách + Build (mặc định)", "Lần đầu sử dụng"),
        ("python build_css.py split", "Chỉ tách file CSS", "Tách style.css thành modules"),
        ("python build_css.py build", "Chỉ build CSS", "Gộp modules thành main.min.css"),
        ("python build_css.py watch", "Watch mode", "Tự động build khi sửa file"),
        ("python build_css.py help", "Hiển thị trợ giúp", "Xem hướng dẫn này"),
    ]

    for cmd, desc, note in commands:
        print(f"  {cmd:30s}")
        print(f"    └─ {desc}")
        print(f"       💡 {note}\n")

    print("📁 Cấu trúc thư mục:\n")
    print("  app/")
    print("  └── static/")
    print("      └── css/")
    print("          ├── modules/           ← Các module CSS")
    print("          │   ├── 01-reset.css")
    print("          │   ├── 02-navbar.css")
    print("          │   └── ...")
    print("          ├── style.css          ← File CSS gốc")
    print("          └── main.min.css       ← File build (dùng trong production)\n")

    print("⚡ Workflow khuyến nghị:\n")
    print("  1. Lần đầu: python build_css.py")
    print("  2. Phát triển: python build_css.py watch")
    print("  3. Production: Chỉ cần deploy main.min.css\n")

    print("🔗 Update template:\n")
    print('  <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/main.min.css\') }}">\n')


def main():
    """Main function"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'split':
            split_css(INPUT_FILE)

        elif command == 'build':
            build_css()

        elif command == 'watch':
            watch_and_build()

        elif command in ['help', '-h', '--help']:
            show_help()

        else:
            print_error(f"Lệnh không hợp lệ: {command}")
            print_info("Chạy 'python build_css.py help' để xem hướng dẫn")

    else:
        # Mặc định: split + build
        print_header("🚀 CSS BUILD SYSTEM - BRICON")
        print_info("Chế độ: Tự động (Split + Build)\n")

        if split_css(INPUT_FILE):
            build_css()

            print("\n" + "=" * 70)
            print("  🎉 HOÀN TẤT!")
            print("=" * 70)
            print("\n💡 Lần sau chỉ cần chạy:")
            print("   • python build_css.py build  (Build lại)")
            print("   • python build_css.py watch  (Auto build)\n")


if __name__ == '__main__':
    main()