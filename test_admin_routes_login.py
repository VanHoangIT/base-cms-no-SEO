import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/admin/login"

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admi32n123"

admin_routes = [
    "/admin/dashboard",
    "/admin/products",
    "/admin/categories",
    "/admin/blogs",
    "/admin/users",
    "/admin/settings",
]

print("======================================================================")
print("🧪 TEST ADMIN ROUTES - BRICON VN")
print("======================================================================")

session = requests.Session()

# 1️⃣ Lấy trang login để lấy CSRF token
print("\n🔍 Lấy CSRF token...")
resp = session.get(LOGIN_URL)
soup = BeautifulSoup(resp.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
print("✅ Lấy token thành công:", csrf_token[:10], "...")

# 2️⃣ Gửi request login
print("\n🔐 Đang đăng nhập admin...")
login_data = {
    "email": ADMIN_EMAIL,
    "password": ADMIN_PASSWORD,
    "csrf_token": csrf_token,
}
login_resp = session.post(LOGIN_URL, data=login_data, allow_redirects=True)

# 🧠 Kiểm tra thật sự login thành công
if "/admin/dashboard" in login_resp.url:
    print("✅ Đăng nhập thành công (redirect tới dashboard)")
elif "csrf_token" in login_resp.text:
    print("❌ Đăng nhập thất bại (vẫn ở trang login)")
    exit(1)
else:
    print("⚠️ Không xác định được trạng thái đăng nhập (status:", login_resp.status_code, ")")
    exit(1)

# 3️⃣ Test các route admin
print("\n======================================================================")
print("📍 TEST ADMIN ROUTES")
print("======================================================================")

passed, failed = 0, 0
for route in admin_routes:
    url = f"{BASE_URL}{route}"
    resp = session.get(url)
    if resp.status_code == 200:
        print(f"✅ {route:30} - OK (200)")
        passed += 1
    elif resp.status_code == 302:
        print(f"⚠️  {route:30} - Redirect (chưa login?)")
        failed += 1
    else:
        print(f"❌ {route:30} - Lỗi ({resp.status_code})")
        failed += 1

print("\n======================================================================")
print("📊 KẾT QUẢ TEST")
print("======================================================================")
print(f"  ✅ Passed: {passed}")
print(f"  ❌ Failed: {failed}")
print("======================================================================")
