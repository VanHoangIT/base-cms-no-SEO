import requests
from requests.exceptions import RequestException

print("\n======================================================================")
print("🧪 TEST ADMIN ROUTES - BRICON CMS")
print("======================================================================\n")

BASE_URL = "http://localhost:5000"

routes = [
    ("/admin/login", "Trang đăng nhập"),
    ("/admin/dashboard", "Trang dashboard"),
    ("/admin/products", "Quản lý sản phẩm"),
    ("/admin/blogs", "Quản lý blog"),
    ("/admin/categories", "Danh mục"),
    ("/admin/users", "Người dùng"),
    ("/admin/settings", "Cấu hình hệ thống"),
    ("/admin/faqs", "FAQ"),
    ("/admin/contacts", "Liên hệ"),
    ("/admin/projects", "Dự án"),
    ("/admin/jobs", "Tuyển dụng"),
    ("/admin/media", "Thư viện ảnh"),
]

# Kiểm tra server đang chạy
print("🔍 Kiểm tra server...")
try:
    res = requests.get(BASE_URL)
    if res.status_code == 200:
        print("✅ Server đang chạy\n")
    else:
        print(f"⚠️ Server phản hồi nhưng lỗi ({res.status_code})\n")
except RequestException:
    print("❌ Server không chạy. Hãy bật Flask app trước khi test.")
    exit(1)

passed = 0
failed = 0

print("======================================================================")
print("📍 TEST ADMIN ROUTES")
print("======================================================================\n")

for route, name in routes:
    url = BASE_URL + route
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in (200, 302):  # 302 cho phép redirect (vd chưa login)
            print(f"✅ {name:<30} - {url}")
            passed += 1
        else:
            print(f"❌ {name:<30} - Status: {response.status_code}")
            failed += 1
    except RequestException as e:
        print(f"❌ {name:<30} - Lỗi kết nối ({e})")
        failed += 1

print("\n======================================================================")
print("📊 KẾT QUẢ TEST")
print("======================================================================\n")

print(f"  ✅ Passed: {passed}/{len(routes)}")
print(f"  ❌ Failed: {failed}/{len(routes)}")

if failed == 0:
    print("\n🎉 TẤT CẢ ROUTE ADMIN ĐỀU HOẠT ĐỘNG TỐT!\n")
else:
    print("\n⚠️  CÓ ROUTE ADMIN BỊ LỖI, KIỂM TRA LẠI LOG FLASK.\n")
