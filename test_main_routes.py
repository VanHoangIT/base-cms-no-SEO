#!/usr/bin/env python3
"""
Script test tất cả routes sau migration
Chạy: python test_main_routes.py
"""

import sys
import requests
from urllib.parse import urljoin


# Màu cho terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


# Base URL - thay đổi nếu cần
BASE_URL = 'http://localhost:5000'

# Danh sách routes cần test
ROUTES_TO_TEST = [
    # Home & Static
    {'url': '/', 'name': 'Trang chủ', 'method': 'GET'},
    {'url': '/gioi-thieu', 'name': 'Giới thiệu', 'method': 'GET'},
    {'url': '/chinh-sach', 'name': 'Chính sách', 'method': 'GET'},

    # Products
    {'url': '/san-pham', 'name': 'Danh sách sản phẩm', 'method': 'GET'},
    {'url': '/san-pham?search=test', 'name': 'Tìm kiếm sản phẩm', 'method': 'GET'},
    {'url': '/san-pham?sort=price_asc', 'name': 'Sắp xếp sản phẩm', 'method': 'GET'},

    # Blog
    {'url': '/tin-tuc', 'name': 'Danh sách blog', 'method': 'GET'},
    {'url': '/tin-tuc?search=test', 'name': 'Tìm kiếm blog', 'method': 'GET'},

    # Contact
    {'url': '/lien-he', 'name': 'Liên hệ', 'method': 'GET'},

    # Projects
    {'url': '/du-an', 'name': 'Danh sách dự án', 'method': 'GET'},

    # Careers
    {'url': '/tuyen-dung', 'name': 'Tuyển dụng', 'method': 'GET'},

    # FAQ
    {'url': '/cau-hoi-thuong-gap', 'name': 'FAQ', 'method': 'GET'},

    # Search
    {'url': '/tim-kiem?q=test', 'name': 'Tìm kiếm', 'method': 'GET'},

    # Misc
    {'url': '/sitemap.xml', 'name': 'Sitemap', 'method': 'GET'},
    {'url': '/robots.txt', 'name': 'Robots.txt', 'method': 'GET'},
]


def test_route(route_info):
    """Test một route"""
    url = urljoin(BASE_URL, route_info['url'])
    name = route_info['name']

    try:
        response = requests.get(url, timeout=10, allow_redirects=False)

        # Check status code
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ {name:<30}{Colors.END} - {url}")
            return True
        elif response.status_code == 404:
            print(f"{Colors.RED}❌ {name:<30}{Colors.END} - 404 Not Found")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️  {name:<30}{Colors.END} - Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ {name:<30}{Colors.END} - Không kết nối được server")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ {name:<30}{Colors.END} - Lỗi: {e}")
        return False


def check_server():
    """Kiểm tra server có chạy không"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return True
    except:
        return False


def main():
    print("\n" + "=" * 70)
    print("🧪 TEST MAIN ROUTES - BRICON VN")
    print("=" * 70 + "\n")

    print(f"🌐 Server URL: {BASE_URL}\n")

    # Check server
    print("🔍 Kiểm tra server...")
    if not check_server():
        print(f"{Colors.RED}❌ Server không chạy tại {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Vui lòng chạy: flask run hoặc python run.py{Colors.END}\n")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Server đang chạy{Colors.END}\n")

    # Test routes
    print("=" * 70)
    print("📍 TEST ROUTES")
    print("=" * 70 + "\n")

    passed = 0
    failed = 0

    for route in ROUTES_TO_TEST:
        if test_route(route):
            passed += 1
        else:
            failed += 1

    # Summary
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ TEST")
    print("=" * 70 + "\n")

    total_routes = len(ROUTES_TO_TEST)
    print(f"  ✅ Passed: {passed}/{total_routes}")
    print(f"  ❌ Failed: {failed}/{total_routes}")

    print(f"\n{'=' * 70}")
    if failed == 0:
        print(f"{Colors.GREEN}🎉 TẤT CẢ TEST ĐỀU PASS!{Colors.END}")
    else:
        print(f"{Colors.RED}⚠️  CÓ {failed} TEST FAILED{Colors.END}")
    print(f"{'=' * 70}\n")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Test bị hủy bởi user{Colors.END}\n")
        sys.exit(1)
