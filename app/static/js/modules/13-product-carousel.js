/**
 * ==================== CAROUSEL SẢN PHẨM MOBILE ====================
 * File: 13-product-carousel.js
 * Tạo tự động từ: main.js
 * Ngày tạo: 25/10/2025 18:06:06
 * ==========================================================================
 * 

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
        
 * ==========================================================================
 */

// ==================== MOBILE PRODUCT CAROUSEL ====================
(function() {
  'use strict';

  // Chỉ chạy trên mobile và tablet (≤991px)
  if (window.innerWidth > 991) {
    return;
  }

  class MobileProductCarousel {
    constructor(container) {
      this.container = container;
      this.track = null;
      this.slides = [];
      this.currentIndex = 0;
      this.isDragging = false;
      this.startPos = 0;
      this.currentTranslate = 0;
      this.prevTranslate = 0;
      this.animationID = 0;

      this.init();
    }

    init() {
      // Tạo cấu trúc carousel
      this.createCarouselStructure();

      // Setup event listeners
      this.setupEventListeners();

      // Initial update
      this.updateCarousel(false);

      console.log(`Product Carousel: Initialized with ${this.slides.length} products`);
    }

    createCarouselStructure() {
      // Wrap các card sản phẩm vào carousel structure
      const products = Array.from(this.container.children);

      if (products.length === 0) return;

      // Tạo wrapper
      const wrapper = document.createElement('div');
      wrapper.className = 'mobile-product-carousel-wrapper';

      // Tạo track (container chứa các slides)
      this.track = document.createElement('div');
      this.track.className = 'mobile-product-carousel-track';

      // Wrap mỗi product card vào slide
      products.forEach((product, index) => {
        const slide = document.createElement('div');
        slide.className = 'mobile-product-slide';
        slide.setAttribute('data-index', index);

        // Di chuyển product card vào slide
        slide.appendChild(product);
        this.track.appendChild(slide);
        this.slides.push(slide);
      });

      // Tạo navigation buttons
      const prevBtn = document.createElement('button');
      prevBtn.className = 'mobile-carousel-btn mobile-carousel-prev';
      prevBtn.innerHTML = '<i class="bi bi-chevron-left"></i>';
      prevBtn.setAttribute('aria-label', 'Previous product');

      const nextBtn = document.createElement('button');
      nextBtn.className = 'mobile-carousel-btn mobile-carousel-next';
      nextBtn.innerHTML = '<i class="bi bi-chevron-right"></i>';
      nextBtn.setAttribute('aria-label', 'Next product');

      // Tạo dots navigation
      const dotsContainer = document.createElement('div');
      dotsContainer.className = 'mobile-carousel-dots';

      this.slides.forEach((_, index) => {
        const dot = document.createElement('button');
        dot.className = 'mobile-carousel-dot';
        if (index === 0) dot.classList.add('active');
        dot.setAttribute('aria-label', `Go to product ${index + 1}`);
        dot.setAttribute('data-index', index);
        dotsContainer.appendChild(dot);
      });

      // Thêm tất cả vào wrapper
      wrapper.appendChild(this.track);
      wrapper.appendChild(prevBtn);
      wrapper.appendChild(nextBtn);
      wrapper.appendChild(dotsContainer);

      // Clear container và add wrapper
      this.container.innerHTML = '';
      this.container.appendChild(wrapper);

      // Lưu references
      this.prevBtn = prevBtn;
      this.nextBtn = nextBtn;
      this.dotsContainer = dotsContainer;
    }

    setupEventListeners() {
      // Button clicks
      this.prevBtn.addEventListener('click', () => this.prevSlide());
      this.nextBtn.addEventListener('click', () => this.nextSlide());

      // Dot clicks
      const dots = this.dotsContainer.querySelectorAll('.mobile-carousel-dot');
      dots.forEach(dot => {
        dot.addEventListener('click', () => {
          const index = parseInt(dot.getAttribute('data-index'));
          this.goToSlide(index);
        });
      });

      // Touch/Mouse drag
      this.track.addEventListener('mousedown', (e) => this.dragStart(e));
      this.track.addEventListener('touchstart', (e) => this.dragStart(e), { passive: true });

      this.track.addEventListener('mousemove', (e) => this.dragMove(e));
      this.track.addEventListener('touchmove', (e) => this.dragMove(e), { passive: true });

      this.track.addEventListener('mouseup', () => this.dragEnd());
      this.track.addEventListener('touchend', () => this.dragEnd());

      this.track.addEventListener('mouseleave', () => {
        if (this.isDragging) this.dragEnd();
      });

      // Prevent default behaviors
      this.track.addEventListener('contextmenu', (e) => e.preventDefault());
      this.track.addEventListener('dragstart', (e) => e.preventDefault());

      // Keyboard navigation
      document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    updateCarousel(smooth = true) {
      // Set transition
      if (smooth) {
        this.track.style.transition = 'transform 400ms cubic-bezier(0.4, 0, 0.2, 1)';
      } else {
        this.track.style.transition = 'none';
      }

      // Calculate and apply transform
      const offset = -this.currentIndex * 100;
      this.track.style.transform = `translateX(${offset}%)`;

      // Update dots
      const dots = this.dotsContainer.querySelectorAll('.mobile-carousel-dot');
      dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === this.currentIndex);
      });

      // Update button states
      this.updateButtonStates();
    }

    updateButtonStates() {
      // Disable prev button on first slide
      this.prevBtn.disabled = this.currentIndex === 0;
      this.prevBtn.style.opacity = this.currentIndex === 0 ? '0.3' : '1';

      // Disable next button on last slide
      this.nextBtn.disabled = this.currentIndex === this.slides.length - 1;
      this.nextBtn.style.opacity = this.currentIndex === this.slides.length - 1 ? '0.3' : '1';
    }

    goToSlide(index) {
      if (index < 0 || index >= this.slides.length) return;
      this.currentIndex = index;
      this.updateCarousel();
    }

    nextSlide() {
      if (this.currentIndex < this.slides.length - 1) {
        this.currentIndex++;
        this.updateCarousel();
      }
    }

    prevSlide() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.updateCarousel();
      }
    }

    // Drag functionality
    getPositionX(event) {
      return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }

    dragStart(event) {
      // Ignore if clicking on buttons or links
      if (event.target.closest('a, button, .mobile-carousel-btn')) {
        return;
      }

      this.isDragging = true;
      this.startPos = this.getPositionX(event);
      this.animationID = requestAnimationFrame(() => this.animation());

      this.track.style.cursor = 'grabbing';
    }

    dragMove(event) {
      if (!this.isDragging) return;

      const currentPosition = this.getPositionX(event);
      const diff = currentPosition - this.startPos;
      this.currentTranslate = this.prevTranslate + diff;
    }

    dragEnd() {
      if (!this.isDragging) return;

      this.isDragging = false;
      cancelAnimationFrame(this.animationID);

      this.track.style.cursor = 'grab';

      const movedBy = this.currentTranslate - this.prevTranslate;
      const threshold = 50; // pixels

      // Determine if we should change slide
      if (Math.abs(movedBy) > threshold) {
        if (movedBy < 0 && this.currentIndex < this.slides.length - 1) {
          this.nextSlide();
        } else if (movedBy > 0 && this.currentIndex > 0) {
          this.prevSlide();
        } else {
          this.updateCarousel();
        }
      } else {
        this.updateCarousel();
      }

      this.prevTranslate = -this.currentIndex * this.track.offsetWidth;
      this.currentTranslate = this.prevTranslate;
    }

    animation() {
      if (!this.isDragging) return;

      const slideWidth = this.track.offsetWidth;
      const percentageTranslate = (this.currentTranslate / slideWidth) * 100;

      this.track.style.transition = 'none';
      this.track.style.transform = `translateX(${percentageTranslate}%)`;

      this.animationID = requestAnimationFrame(() => this.animation());
    }

    handleKeyboard(event) {
      // Only handle if carousel is in viewport
      const rect = this.container.getBoundingClientRect();
      const isInView = rect.top < window.innerHeight && rect.bottom >= 0;

      if (!isInView) return;

      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        this.prevSlide();
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        this.nextSlide();
      }
    }
  }

  // Initialize carousels
  function initCarousels() {
    const productGrids = document.querySelectorAll('.row.g-4');

    productGrids.forEach(grid => {
      // Kiểm tra xem có phải là product grid không
      const hasProducts = grid.querySelector('.product-card');
      if (hasProducts) {
        new MobileProductCarousel(grid);
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCarousels);
  } else {
    initCarousels();
  }

  // Re-initialize on window resize (if switching from desktop to mobile)
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (window.innerWidth <= 991) {
        initCarousels();
      }
    }, 250);
  });

})();
// ==================== MOBILE BLOG CAROUSEL ====================