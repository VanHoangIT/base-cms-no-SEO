#!/usr/bin/env python3
"""
JavaScript Build System - Tách và gộp JS tự động cho Flask Project
Author: BRICON Web Development Team
Usage: python build_js.py [command]
pip install watchdog
"""

import os
import re
from pathlib import Path
from datetime import datetime

# ==================== CẤU HÌNH DỰ ÁN ====================
BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = BASE_DIR / 'app' / 'static'
JS_DIR = STATIC_DIR / 'js'
MODULES_DIR = JS_DIR / 'modules'
INPUT_FILE = JS_DIR / 'main.js'
OUTPUT_FILE = JS_DIR / 'main.min.js'

# ==================== CẤU TRÚC MODULE JAVASCRIPT ====================
JS_MODULES = {
    '01-floating-buttons.js': {
        'start': '// ==================== FLOATING BUTTONS ====================',
        'end': '// ==================== ANIMATE ON SCROLL ====================',
        'description': 'NÚT HÀNH ĐỘNG NỔI',
        'details': '''
        📍 Vị trí: Góc phải màn hình
        🎯 Chức năng: Hiển thị các nút floating (Phone, Zalo, Messenger)
        📄 Sử dụng tại: 
           - layouts/base.html (component floating-buttons)
           - Tất cả các trang public
        🔧 Hoạt động: Luôn hiển thị khi scroll, style.display = "flex"
        '''
    },
    '02-animate-scroll.js': {
        'start': '// ==================== ANIMATE ON SCROLL ====================',
        'end': '// ==================== AUTO DISMISS ALERTS ====================',
        'description': 'HIỆU ỨNG CUỘN TRANG',
        'details': '''
        📍 Vị trí: Áp dụng cho tất cả card
        🎯 Chức năng: Tự động thêm animation khi card xuất hiện trong viewport
        📄 Sử dụng tại:
           - components/card_product.html (thẻ sản phẩm)
           - components/card_blog.html (thẻ tin tức)
        🔧 Hoạt động: 
           - Dùng IntersectionObserver API
           - Thêm class "animate-on-scroll" khi element vào màn hình
           - threshold: 0.1 (10% element hiển thị)
        '''
    },
    '03-auto-dismiss-alerts.js': {
        'start': '// ==================== AUTO DISMISS ALERTS ====================',
        'end': '// ==================== SEARCH FORM VALIDATION ====================',
        'description': 'TỰ ĐỘNG ĐÓNG THÔNG BÁO',
        'details': '''
        📍 Vị trí: Mọi trang có flash messages
        🎯 Chức năng: Tự động đóng thông báo Bootstrap sau 3 giây
        📄 Sử dụng tại:
           - layouts/base.html ({% with messages = get_flashed_messages() %})
           - Các trang admin sau khi submit form
        🔧 Hoạt động:
           - Target: .alert.alert-dismissible
           - Timeout: 3000ms (3 giây)
           - Dùng bootstrap.Alert().close()
        '''
    },
    '04-search-validation.js': {
        'start': '// ==================== SEARCH FORM VALIDATION ====================',
        'end': '// ==================== IMAGE LAZY LOADING ====================',
        'description': 'KIỂM TRA FORM TÌM KIẾM',
        'details': '''
        📍 Vị trí: Thanh tìm kiếm navbar và trang search
        🎯 Chức năng: Ngăn submit form tìm kiếm khi input rỗng
        📄 Sử dụng tại:
           - layouts/base.html (form search trong navbar)
           - public/search.html (trang tìm kiếm chính)
        🔧 Hoạt động:
           - Target: form[action*="search"]
           - Kiểm tra input[name="q"] hoặc input[name="search"]
           - preventDefault() nếu value.trim() === ""
           - Hiện alert "Vui lòng nhập từ khóa tìm kiếm"
        '''
    },
    '05-lazy-loading.js': {
        'start': '// ==================== IMAGE LAZY LOADING ====================',
        'end': '// ==================== SMOOTH SCROLL - FIXED ====================',
        'description': 'TẢI ẢNH CHẬM (LAZY LOAD)',
        'details': '''
        📍 Vị trí: Tất cả ảnh có attribute loading="lazy"
        🎯 Chức năng: Chỉ tải ảnh khi sắp vào viewport, tiết kiệm băng thông
        📄 Sử dụng tại:
           - components/card_product.html (ảnh sản phẩm)
           - components/card_blog.html (ảnh bài viết)
           - public/products.html, blogs.html
        🔧 Hoạt động:
           - Kiểm tra browser có hỗ trợ native lazy loading
           - Nếu CÓ: Dùng img[data-src] → img.src
           - Nếu KHÔNG: Tải lazysizes.min.js từ CDN làm fallback
        '''
    },
    '06-smooth-scroll.js': {
        'start': '// ==================== SMOOTH SCROLL - FIXED ====================',
        'end': '// ==================== SCROLL TO TOP WITH PROGRESS ====================',
        'description': 'CUỘN MỀM MẠI ANCHOR',
        'details': '''
        📍 Vị trí: Tất cả link có href="#..."
        🎯 Chức năng: Cuộn mượt mà đến section thay vì nhảy đột ngột
        📄 Sử dụng tại:
           - Navbar menu links (href="#about", "#products")
           - Banner CTA buttons (href="#featured-projects")
           - Footer quick links
        🔧 Hoạt động:
           - BỎ QUA nếu có data-bs-toggle (Bootstrap tabs)
           - BỎ QUA nếu href chỉ là "#" đơn thuần
           - Kiểm tra element có tồn tại trước khi scroll
           - Offset: -120px (tránh bị che bởi navbar fixed)
           - behavior: "smooth"
        ⚠️ Lưu ý: Fixed để không conflict với Bootstrap components
        '''
    },
    '07-scroll-to-top.js': {
        'start': '// ==================== SCROLL TO TOP WITH PROGRESS ====================',
        'end': '// ==================== BANNER LAZY LOAD + RESPONSIVE (INTEGRATED) ====================',
        'description': 'NÚT LÊN ĐẦU TRANG + TIẾN TRÌNH',
        'details': '''
        📍 Vị trí: Góc phải dưới màn hình
        🎯 Chức năng: 
           - Hiện nút khi scroll > 300px
           - Vòng tròn progress theo % scroll
           - Click để lên đầu trang
        📄 Sử dụng tại:
           - layouts/base.html (id="scrollToTop")
           - CSS: 20-scroll-to-top.css
        🔧 Hoạt động:
           - Dùng SVG circle với strokeDasharray/strokeDashoffset
           - Tính scrollPercentage = scrollTop / scrollHeight
           - Update offset theo % để vẽ progress circle
           - requestAnimationFrame để smooth
           - Show button: scrollTop > 300px
        '''
    },
    '08-banner-carousel.js': {
        'start': '// ==================== BANNER LAZY LOAD + RESPONSIVE (INTEGRATED) ====================',
        'end': '// ==================== RESPONSIVE IMAGE SOURCE HANDLER ====================',
        'description': 'BANNER CAROUSEL TRANG CHỦ',
        'details': '''
        📍 Vị trí: Trang chủ (index.html)
        🎯 Chức năng: Quản lý carousel banner với đầy đủ tính năng
        📄 Sử dụng tại:
           - public/index.html (id="bannerCarousel")
           - CSS: 04-banner.css
        🔧 Các tính năng:
           1. ✅ LAZY LOAD: IntersectionObserver tải ảnh khi cần
           2. ✅ PRELOAD: Tải trước slide hiện tại và 2 slide kế (prev/next)
           3. ✅ PAUSE ON HOVER: Desktop dừng khi hover
           4. ✅ PAUSE ON TOUCH: Mobile dừng khi chạm, resume sau 3s
           5. ✅ KEYBOARD: Arrow Left/Right điều khiển
           6. ✅ REDUCED MOTION: Tôn trọng prefers-reduced-motion
           7. ✅ SMOOTH CTA: Banner buttons scroll mượt
           8. ✅ FALLBACK: Force load tất cả ảnh sau 3s
           9. ✅ ANALYTICS: Track views nếu có Google Analytics/GTM
           10. ✅ PRECONNECT: Nếu dùng Cloudinary/ImgIX CDN
        '''
    },
    '09-responsive-images.js': {
        'start': '// ==================== RESPONSIVE IMAGE SOURCE HANDLER ====================',
        'end': 'window.addEventListener(\'load\', function() {',
        'description': 'XỬ LÝ ẢNH RESPONSIVE',
        'details': '''
        📍 Vị trí: Banner carousel (dùng <picture> tag)
        🎯 Chức năng: Force browser đánh giá lại <source> khi resize
        📄 Sử dụng tại:
           - public/index.html (banner với <picture><source media="...">)
        🔧 Hoạt động:
           - Listen resize event (debounced 250ms)
           - Tìm tất cả <picture> trong carousel
           - Set img.src = img.src để trigger re-evaluation
           - Browser tự chọn <source> phù hợp theo media query
        ⚠️ Cần thiết cho Safari/iOS không auto-update picture sources
        '''
    },
    '10-page-loader.js': {
        'start': 'window.addEventListener(\'load\', function() {',
        'end': '// ==================== FEATURED PROJECTS CAROUSEL WITH MOUSE DRAG ====================',
        'description': 'LOADING TOÀN TRANG',
        'details': '''
        📍 Vị trí: Tất cả các trang
        🎯 Chức năng: Hiển thị spinner khi trang đang load, ẩn khi xong
        📄 Sử dụng tại:
           - layouts/base.html (id="page-loader")
           - CSS: 17-loading.css
        🔧 Hoạt động:
           - Trigger: window load event
           - Fade out: opacity = 0 (transition 300ms)
           - Remove: setTimeout 300ms để xóa khỏi DOM
        💡 Cải thiện UX khi trang load chậm (hình ảnh lớn, JS nhiều)
        '''
    },
    '11-projects-carousel.js': {
        'start': '// ==================== FEATURED PROJECTS CAROUSEL WITH MOUSE DRAG ====================',
        'end': '/**\n * Chatbot Widget - MOBILE OPTIMIZED',
        'description': 'CAROUSEL DỰ ÁN NỔI BẬT',
        'details': '''
        📍 Vị trí: Trang chủ section "Dự án nổi bật"
        🎯 Chức năng: Carousel tùy chỉnh với kéo chuột/chạm
        📄 Sử dụng tại:
           - public/index.html (id="projectsCarousel")
           - components/featured_projects.html
           - CSS: 19-featured-projects.css
        🔧 Các tính năng:
           - ✅ MOUSE DRAG: Kéo chuột để chuyển slide (desktop)
           - ✅ TOUCH DRAG: Vuốt ngón tay (mobile)
           - ✅ RUBBER BAND: Hiệu ứng giới hạn khi kéo quá đầu/cuối
           - ✅ AUTO SLIDE: Tự động chuyển sau 5s
           - ✅ DOTS NAVIGATION: Click vào dot để jump slide
           - ✅ KEYBOARD: Arrow keys điều khiển
           - ✅ PAUSE ON HOVER: Dừng auto khi hover
           - ✅ TAB HIDDEN: Dừng khi tab ẩn (visibilitychange)
           - ✅ RESPONSIVE: Tự động điều chỉnh khi resize
        🎨 Cursor: grab → grabbing khi drag
        ⚠️ Threshold: 50px để chuyển slide
        '''
    },
    '12-chatbot.js': {
        'start': '/**\n * Chatbot Widget - MOBILE OPTIMIZED',
        'end': '// ==================== MOBILE PRODUCT CAROUSEL ====================',
        'description': 'CHATBOT HỖ TRỢ KHÁCH HÀNG',
        'details': '''
        📍 Vị trí: Góc phải dưới màn hình (trên scroll-to-top)
        🎯 Chức năng: Chatbot AI hỗ trợ khách hàng 24/7
        📄 Sử dụng tại:
           - layouts/base.html (id="chatbotButton", id="chatbotWidget")
           - components/chatbot.html
           - CSS: 26-chatbot.css
           - Backend: app/chatbot/routes.py
        🔧 Các tính năng:
           - ✅ FULL SCREEN MOBILE: Chiếm toàn màn hình trên mobile
           - ✅ NO AUTO-FOCUS: Không tự động mở bàn phím
           - ✅ BODY SCROLL LOCK: Khóa scroll body khi mở (iOS fix)
           - ✅ TYPING INDICATOR: Hiệu ứng "đang gõ..." khi bot trả lời
           - ✅ AUTO SCROLL: Tự động scroll xuống tin nhắn mới
           - ✅ REQUEST LIMIT: Hiển thị số tin nhắn còn lại (20/session)
           - ✅ RESET CHAT: Nút làm mới hội thoại
           - ✅ ERROR HANDLING: Xử lý lỗi mạng, server
           - ✅ INPUT VALIDATION: Giới hạn 500 ký tự
           - ✅ ESCAPE HTML: Bảo mật XSS
        🌐 API Endpoints:
           - POST /chatbot/send → Gửi tin nhắn
           - POST /chatbot/reset → Reset session
        💡 Dùng Flask session để lưu lịch sử chat
        '''
    },
    '13-product-carousel.js': {
        'start': '// ==================== MOBILE PRODUCT CAROUSEL ====================',
        'end': None,
        'description': 'CAROUSEL SẢN PHẨM MOBILE',
        'details': '''
        📍 Vị trí: Các grid sản phẩm (section "Sản phẩm" / "Danh mục") trên giao diện mobile & tablet

        🎯 Chức năng: 
        Chuyển danh sách sản phẩm dạng lưới sang carousel ngang khi màn hình ≤ 991px.  
        Cho phép người dùng vuốt, kéo, hoặc click mũi tên để di chuyển giữa các sản phẩm.

        📄 Sử dụng tại:
           - Các container có class: `.row.g-4` chứa `.product-card`
           - HTML: `components/products_section.html`, `public/index.html`
           - CSS: `19-products-carousel.css`

        🔧 Các tính năng:
           - ✅ RESPONSIVE: Chỉ kích hoạt khi màn hình ≤ 991px
           - ✅ MOUSE DRAG: Kéo chuột để chuyển sản phẩm (desktop nhỏ / tablet)
           - ✅ TOUCH DRAG: Vuốt ngón tay để chuyển sản phẩm (mobile)
           - ✅ NAV BUTTONS: Hai nút điều hướng trái / phải (bi-chevron-left / right)
           - ✅ DOTS NAVIGATION: Click vào dot để nhảy đến sản phẩm tương ứng
           - ✅ KEYBOARD: Hỗ trợ phím ← → để điều khiển khi trong viewport
           - ✅ SMOOTH TRANSITION: Hiệu ứng chuyển mượt cubic-bezier
           - ✅ RUBBER BAND LIMIT: Giới hạn kéo khi chạm đầu hoặc cuối
           - ✅ REINIT ON RESIZE: Tự khởi tạo lại khi thay đổi kích thước màn hình

        🎨 Cursor: `grab` → `grabbing` khi kéo sản phẩm  
        ⚙️ Threshold: 50px để chuyển sang slide kế tiếp
        '''
    }
}


# ==================== HÀM TIỆN ÍCH ====================
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


# ==================== HÀM XỬ LÝ JAVASCRIPT ====================
def extract_js_section(content, start_marker, end_marker):
    """Trích xuất section JS giữa 2 marker"""
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


def minify_js(js_content):
    """Minify JavaScript - loại bỏ comments và khoảng trắng thừa (cơ bản)"""
    # Giữ lại comment đầu tiên (header info)
    first_comment = re.search(r'/\*.*?\*/', js_content, flags=re.DOTALL)
    header = first_comment.group(0) if first_comment else ""

    # Loại bỏ single-line comments (cẩn thận với URLs)
    js_content = re.sub(r'(?<!:)//.*?$', '', js_content, flags=re.MULTILINE)

    # Loại bỏ multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)

    # Loại bỏ khoảng trắng thừa (giữ nguyên strings)
    js_content = re.sub(r'\n\s*\n', '\n', js_content)

    # Loại bỏ trailing spaces
    js_content = re.sub(r'[ \t]+$', '', js_content, flags=re.MULTILINE)

    return (header + "\n" + js_content.strip()) if header else js_content.strip()


def split_js(input_file):
    """Tách file JS lớn thành các module nhỏ"""
    print_header("🎯 TÁCH FILE JAVASCRIPT THÀNH CÁC MODULE")

    if not input_file.exists():
        print_error(f"Không tìm thấy file: {input_file}")
        return False

    print_info(f"Đọc file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tạo thư mục modules
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    print_success(f"Tạo thư mục: {MODULES_DIR}")

    print(f"\n📦 Đang tách thành {len(JS_MODULES)} module...\n")

    total_lines = 0
    total_size = 0

    for filename, config in JS_MODULES.items():
        section = extract_js_section(content, config['start'], config['end'])

        if section:
            output_path = MODULES_DIR / filename

            # Thêm header chi tiết bằng tiếng Việt
            header = f"""/**
 * ==================== {config['description']} ====================
 * File: {filename}
 * Tạo tự động từ: main.js
 * Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
 * ==========================================================================
 * 
{config['details']}
 * ==========================================================================
 */

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
    print(f"  Tổng cộng: {len(JS_MODULES)} files | {total_lines:5d} dòng | {total_size:7.1f} KB")
    print(f"{'─' * 70}")

    print_success(f"Hoàn tất! Module được lưu tại: {MODULES_DIR}")
    return True


def build_js():
    """Gộp tất cả module thành main.min.js"""
    print_header("🔨 BUILD MAIN.MIN.JS")

    if not MODULES_DIR.exists():
        print_error(f"Thư mục {MODULES_DIR} không tồn tại!")
        print_info("Chạy: python build_js.py split")
        return False

    combined_js = []
    total_size = 0
    module_count = 0

    print("📦 Đang gộp các module...\n")

    # Đọc các module theo thứ tự
    for filename in sorted(JS_MODULES.keys()):
        file_path = MODULES_DIR / filename

        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_js.append(content)
                size = len(content) / 1024
                total_size += size
                module_count += 1
            print(f"  ✓ {filename:32s} | {size:7.1f} KB")
        else:
            print_warning(f"Không tìm thấy: {filename}")

    # Tạo header cho file build
    build_header = f"""/*! 
 * ============================================================================
 * BRICON - Main JavaScript Build
 * ============================================================================
 * Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
 * Modules: {module_count} files
 * Description: Auto-generated optimized JavaScript
 * DO NOT EDIT THIS FILE DIRECTLY - Edit individual modules instead
 * ============================================================================
 */

"use strict";

"""

    # Gộp và minify
    full_js = '\n\n'.join(combined_js)
    minified_js = minify_js(full_js)
    final_js = build_header + minified_js

    # Ghi file output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_js)

    # Thống kê
    original_kb = total_size
    minified_kb = len(final_js) / 1024
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

    class JSChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith('.js') and 'main.min.js' not in event.src_path:
                print(f"\n🔄 Phát hiện thay đổi: {Path(event.src_path).name}")
                build_js()

    print_header("👀 WATCH MODE - Tự động build khi có thay đổi")
    print_info(f"Đang theo dõi: {MODULES_DIR}")
    print_info("Nhấn Ctrl+C để dừng...\n")

    event_handler = JSChangeHandler()
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


def list_modules():
    """Liệt kê chi tiết tất cả các module"""
    print_header("📋 DANH SÁCH CHI TIẾT CÁC MODULE JAVASCRIPT")

    print(f"Tổng số module: {len(JS_MODULES)}\n")

    for i, (filename, config) in enumerate(JS_MODULES.items(), 1):
        print(f"\n{'=' * 70}")
        print(f"📦 MODULE #{i:02d}: {filename}")
        print(f"{'=' * 70}")
        print(f"📌 Tên: {config['description']}")
        print(config['details'])

    print(f"\n{'=' * 70}")
    print(f"💡 Để xem code chi tiết, mở file trong thư mục: {MODULES_DIR}")
    print(f"{'=' * 70}\n")


def show_help():
    """Hiển thị hướng dẫn sử dụng"""
    print_header("📖 HƯỚNG DẪN SỬ DỤNG JAVASCRIPT BUILD SYSTEM")

    print("🔧 Các lệnh có sẵn:\n")

    commands = [
        ("python build_js.py", "Tách + Build (mặc định)", "Lần đầu sử dụng"),
        ("python build_js.py split", "Chỉ tách file JS", "Tách main.js thành modules"),
        ("python build_js.py build", "Chỉ build JS", "Gộp modules thành main.min.js"),
        ("python build_js.py watch", "Watch mode", "Tự động build khi sửa file"),
        ("python build_js.py list", "Liệt kê modules", "Xem chi tiết từng module"),
        ("python build_js.py help", "Hiển thị trợ giúp", "Xem hướng dẫn này"),
    ]

    for cmd, desc, note in commands:
        print(f"  {cmd:30s}")
        print(f"    └─ {desc}")
        print(f"       💡 {note}\n")

    print("📁 Cấu trúc thư mục:\n")
    print("  app/")
    print("  └── static/")
    print("      └── js/")
    print("          ├── modules/               ← Các module JavaScript")
    print("          │   ├── 01-floating-buttons.js")
    print("          │   ├── 02-animate-scroll.js")
    print("          │   └── ...")
    print("          ├── main.js                ← File JS gốc")
    print("          └── main.min.js            ← File build (dùng trong production)\n")

    print("⚡ Workflow khuyến nghị:\n")
    print("  1. Lần đầu: python build_js.py")
    print("  2. Phát triển: python build_js.py watch")
    print("  3. Production: Chỉ cần deploy main.min.js\n")

    print("🔗 Update template:\n")
    print('  <script src="{{ url_for(\'static\', filename=\'js/main.min.js\') }}" defer></script>\n')


def main():
    """Main function"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'split':
            split_js(INPUT_FILE)

        elif command == 'build':
            build_js()

        elif command == 'watch':
            watch_and_build()

        elif command == 'list':
            list_modules()

        elif command in ['help', '-h', '--help']:
            show_help()

        else:
            print_error(f"Lệnh không hợp lệ: {command}")
            print_info("Chạy 'python build_js.py help' để xem hướng dẫn")

    else:
        # Mặc định: split + build
        print_header("🚀 JAVASCRIPT BUILD SYSTEM - BRICON")
        print_info("Chế độ: Tự động (Split + Build)\n")

        if split_js(INPUT_FILE):
            build_js()

            print("\n" + "=" * 70)
            print("  🎉 HOÀN TẤT!")
            print("=" * 70)
            print("\n💡 Lần sau chỉ cần chạy:")
            print("   • python build_js.py build  (Build lại)")
            print("   • python build_js.py watch  (Auto build)")
            print("   • python build_js.py list   (Xem chi tiết modules)\n")


if __name__ == '__main__':
    main()