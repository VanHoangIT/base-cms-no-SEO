/**
 * ==================== LOADING TOÀN TRANG ====================
 * File: 10-page-loader.js
 * Tạo tự động từ: main.js
 * Ngày tạo: 25/10/2025 18:06:06
 * ==========================================================================
 * 

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
        
 * ==========================================================================
 */

window.addEventListener('load', function() {
    const loader = document.getElementById('page-loader');
    if (loader) {
    loader.style.opacity = '0';
    setTimeout(() => loader.remove(), 300);
    }
});
