"""
🧪 TEST ADMIN ROUTES (Login as admin@example.com)
Chạy: python test/test_admin_routes.py
"""

import sys
import re
import requests
from requests.exceptions import RequestException


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'


BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/admin/login"
USERNAME = "admin@example.com"
PASSWORD = "admin123"

# Danh sách routes admin cần test
ADMIN_ROUTES = [
    ("/admin/dashboard", "📊 Dashboard", "GET"),
    ("/admin/welcome", "👋 Welcome", "GET"),
    ("/admin/banners", "🎨 Danh sách Banner", "GET"),
    ("/admin/banners/add", "➕ Thêm Banner", "GET"),
    ("/admin/blogs", "📝 Danh sách Blog", "GET"),
    ("/admin/blogs/add", "➕ Thêm Blog", "GET"),
    ("/admin/categories", "📁 Danh mục", "GET"),
    ("/admin/categories/add", "➕ Thêm Danh mục", "GET"),
    ("/admin/products", "🛍️ Sản phẩm", "GET"),
    ("/admin/products/add", "➕ Thêm Sản phẩm", "GET"),
    ("/admin/projects", "🏗️ Dự án", "GET"),
    ("/admin/projects/add", "➕ Thêm Dự án", "GET"),
    ("/admin/jobs", "💼 Tuyển dụng", "GET"),
    ("/admin/jobs/add", "➕ Thêm Tuyển dụng", "GET"),
    ("/admin/faqs", "❓ FAQ", "GET"),
    ("/admin/faqs/add", "➕ Thêm FAQ", "GET"),
    ("/admin/contacts", "📧 Liên hệ", "GET"),
    ("/admin/media", "🖼️ Thư viện Media", "GET"),
    ("/admin/media/upload", "⬆️ Upload Media", "GET"),
    ("/admin/users", "👥 Người dùng", "GET"),
    ("/admin/users/add", "➕ Thêm User", "GET"),
    ("/admin/roles", "🔑 Vai trò", "GET"),
    ("/admin/roles/add", "➕ Thêm Vai trò", "GET"),
    ("/admin/permissions", "🔐 Quyền hạn", "GET"),
    ("/admin/settings", "⚙️ Cài đặt", "GET"),
    ("/admin/quizzes", "📝 Quản lý Quiz", "GET"),
    ("/admin/quizzes/add", "➕ Thêm Quiz", "GET"),
    ("/admin/results", "📊 Kết quả Quiz", "GET"),
]


def check_server():
    """Kiểm tra server có chạy không"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code == 200 or response.status_code == 302
    except RequestException:
        return False


def get_csrf_token(html):
    """Trích xuất CSRF token từ form login"""
    match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html)
    return match.group(1) if match else None


def login_as_admin(session):
    """Đăng nhập bằng tài khoản admin"""
    print(f"{Colors.BLUE}🔑 Đang đăng nhập với admin@example.com...{Colors.END}")

    try:
        # Lấy trang login để có CSRF token
        r = session.get(LOGIN_URL, timeout=10)
        token = get_csrf_token(r.text)

        if not token:
            print(f"{Colors.RED}❌ Không tìm thấy CSRF token trong form login.{Colors.END}")
            return False

        payload = {
            "email": USERNAME,
            "password": PASSWORD,
            "csrf_token": token,
            "submit": "Đăng nhập"
        }

        res = session.post(LOGIN_URL, data=payload, allow_redirects=False, timeout=10)

        if res.status_code in [302, 303]:
            print(f"{Colors.GREEN}✅ Đăng nhập thành công (redirect).{Colors.END}")
            return True
        elif res.status_code == 200 and "dashboard" in res.text.lower():
            print(f"{Colors.GREEN}✅ Đăng nhập thành công (OK).{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Đăng nhập thất bại. Kiểm tra credentials hoặc CSRF field name.{Colors.END}")
            return False

    except RequestException as e:
        print(f"{Colors.RED}❌ Lỗi kết nối khi đăng nhập: {e}{Colors.END}")
        return False


def test_route(session, route, name, method):
    """Test một route admin"""
    url = BASE_URL + route
    try:
        response = session.get(url, allow_redirects=False, timeout=10)
        status = response.status_code

        if status == 200:
            print(f"{Colors.GREEN}✅{Colors.END} {name:<40} {Colors.CYAN}{url}{Colors.END}")
            return True
        elif status == 302 and '/login' in response.headers.get('Location', ''):
            print(f"{Colors.YELLOW}⚠️ {name:<40} (Redirect to login){Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ {name:<40} Status: {status}{Colors.END}")
            return False

    except RequestException:
        print(f"{Colors.RED}❌ {name:<40} Connection error{Colors.END}")
        return False


def main():
    print("\n" + "=" * 80)
    print(f"{Colors.BLUE}🧪 TEST ADMIN ROUTES (Login as admin@example.com){Colors.END}")
    print("=" * 80 + "\n")

    if not check_server():
        print(f"{Colors.RED}❌ Server không chạy tại {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}💡 Vui lòng chạy: flask run hoặc python run.py{Colors.END}\n")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Server đang chạy{Colors.END}\n")

    session = requests.Session()

    if not login_as_admin(session):
        sys.exit(1)

    # Test routes
    print("\n" + "=" * 80)
    print(f"{Colors.BLUE}📍 TEST ADMIN ROUTES{Colors.END}")
    print("=" * 80 + "\n")

    passed = 0
    failed = 0

    for route, name, method in ADMIN_ROUTES:
        if test_route(session, route, name, method):
            passed += 1
        else:
            failed += 1

    total = len(ADMIN_ROUTES)
    print("\n" + "=" * 80)
    print(f"{Colors.BLUE}📊 KẾT QUẢ TEST{Colors.END}")
    print("=" * 80 + "\n")

    print(f"  {Colors.GREEN}✅ Passed: {passed}/{total}{Colors.END}")
    print(f"  {Colors.RED}❌ Failed: {failed}/{total}{Colors.END}")
    if failed > 0:
        print(f"  {Colors.YELLOW}📈 Success rate: {(passed / total) * 100:.1f}%{Colors.END}")

    print(f"\n{'=' * 80}")
    if failed == 0:
        print(f"{Colors.GREEN}🎉 TẤT CẢ ADMIN ROUTES HOẠT ĐỘNG TỐT!{Colors.END}")
    else:
        print(f"{Colors.RED}⚠️ CÓ {failed} ROUTES LỖI - KIỂM TRA LẠI!{Colors.END}")
    print(f"{'=' * 80}\n")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Test bị hủy bởi user{Colors.END}\n")
        sys.exit(1)
