// ==================== FLOATING BUTTONS ====================
window.addEventListener("scroll", function () {
  const floatingButtons = document.querySelector(".floating-buttons");
  if (floatingButtons) {
    floatingButtons.style.display = "flex"; // luôn hiển thị
  }
});

// ==================== ANIMATE ON SCROLL ====================
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver(function (entries) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("animate-on-scroll");
    }
  });
}, observerOptions);

// Observe all product cards and blog cards
document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".product-card, .blog-card");
  cards.forEach((card) => {
    observer.observe(card);
  });
});

// ==================== AUTO DISMISS ALERTS ====================
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert.alert-dismissible");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 3000);
  });
});

// ==================== SEARCH FORM VALIDATION ====================
document.addEventListener("DOMContentLoaded", function () {
  const searchForms = document.querySelectorAll('form[action*="search"]');
  searchForms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const input = form.querySelector('input[name="q"], input[name="search"]');
      if (input && input.value.trim() === "") {
        e.preventDefault();
        alert("Vui lòng nhập từ khóa tìm kiếm");
      }
    });
  });
});

// ==================== IMAGE LAZY LOADING ====================
if ("loading" in HTMLImageElement.prototype) {
  const images = document.querySelectorAll("img[data-src]");
  images.forEach((img) => {
    img.src = img.dataset.src;
  });
} else {
  // Fallback for browsers that don't support lazy loading
  const script = document.createElement("script");
  script.src =
    "https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js";
  document.body.appendChild(script);
}

// ==================== SMOOTH SCROLL - FIXED ====================
// Chỉ áp dụng cho links KHÔNG phải Bootstrap tabs
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a[href*="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      // BỎ QUA nếu là Bootstrap tab hoặc có data-bs-toggle
      if (this.hasAttribute("data-bs-toggle")) {
        return;
      }

      const href = this.getAttribute("href");

      // BỎ QUA nếu href chỉ là "#" đơn thuần
      if (href === "#") {
        return;
      }

      // Kiểm tra nếu target element tồn tại
      const targetId = href.includes("#") ? href.split("#")[1] : null;

      if (targetId) {
        const target = document.getElementById(targetId);

        // Chỉ scroll nếu element thực sự tồn tại
        if (target) {
          e.preventDefault();
          const offsetTop = target.offsetTop - 120;
          window.scrollTo({
            top: offsetTop,
            behavior: "smooth",
          });
        }
      }
    });
  });
});

// ==================== SCROLL TO TOP WITH PROGRESS ====================
(function () {
  const scrollToTopBtn = document.getElementById("scrollToTop");
  if (!scrollToTopBtn) return;

  const progressCircle = scrollToTopBtn.querySelector("circle.progress");
  const radius = progressCircle.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;

  // Set initial progress circle
  progressCircle.style.strokeDasharray = circumference;
  progressCircle.style.strokeDashoffset = circumference;

  // Update progress on scroll
  function updateProgress() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight =
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight;
    const scrollPercentage = (scrollTop / scrollHeight) * 100;

    // Update progress circle
    const offset = circumference - (scrollPercentage / 100) * circumference;
    progressCircle.style.strokeDashoffset = offset;

    // Show/hide button
    if (scrollTop > 300) {
      scrollToTopBtn.classList.add("show");
    } else {
      scrollToTopBtn.classList.remove("show");
    }
  }

  // Smooth scroll to top
  scrollToTopBtn.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  // Listen to scroll event
  let ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        updateProgress();
        ticking = false;
      });
      ticking = true;
    }
  });

  // Initial check
  updateProgress();
})();

// ==================== BANNER LAZY LOAD + RESPONSIVE (INTEGRATED) ====================
document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.getElementById('bannerCarousel');
  if (!carousel) return; // Không có banner thì bỏ qua
  
  // ✅ 1. LAZY LOAD BANNER IMAGES
  const lazyBannerImages = carousel.querySelectorAll('.banner-img[loading="lazy"]');
  
  if ('IntersectionObserver' in window && lazyBannerImages.length > 0) {
    const bannerObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const parent = img.closest('.carousel-item');
          
          // Add loading class for skeleton effect
          if (parent) parent.classList.add('loading');
          
          // Load image
          img.onload = function() {
            img.classList.add('loaded');
            if (parent) parent.classList.remove('loading');
            observer.unobserve(img);
          };
          
          // Trigger load if data-src exists
          if (img.dataset.src) {
            img.src = img.dataset.src;
          } else {
            img.classList.add('loaded'); // Image already has src
            if (parent) parent.classList.remove('loading');
          }
        }
      });
    }, {
      rootMargin: '100px' // Preload 100px before viewport
    });

    lazyBannerImages.forEach(img => bannerObserver.observe(img));
  } else {
    // Fallback: immediately mark as loaded
    lazyBannerImages.forEach(img => img.classList.add('loaded'));
  }

  // ✅ 2. PRELOAD ADJACENT SLIDES
  carousel.addEventListener('slide.bs.carousel', function(e) {
    const slides = carousel.querySelectorAll('.carousel-item');
    const nextIndex = e.to;
    
    // Preload current slide
    const currentSlide = slides[nextIndex];
    if (currentSlide) {
      const currentImg = currentSlide.querySelector('.banner-img');
      if (currentImg && !currentImg.classList.contains('loaded')) {
        currentImg.classList.add('loaded');
      }
    }

    // Preload adjacent slides (prev/next)
    const prevIndex = nextIndex - 1 < 0 ? slides.length - 1 : nextIndex - 1;
    const nextSlideIndex = nextIndex + 1 >= slides.length ? 0 : nextIndex + 1;
    
    [prevIndex, nextSlideIndex].forEach(index => {
      const slide = slides[index];
      if (slide) {
        const img = slide.querySelector('.banner-img');
        if (img && !img.classList.contains('loaded')) {
          img.classList.add('loaded');
        }
      }
    });
  });

  // ✅ 3. PAUSE ON HOVER (Desktop only)
  if (window.innerWidth >= 768) {
    let isHovering = false;
    
    carousel.addEventListener('mouseenter', function() {
      isHovering = true;
      const bsCarousel = bootstrap.Carousel.getInstance(carousel);
      if (bsCarousel) bsCarousel.pause();
    });
    
    carousel.addEventListener('mouseleave', function() {
      if (isHovering) {
        isHovering = false;
        const bsCarousel = bootstrap.Carousel.getInstance(carousel);
        if (bsCarousel) bsCarousel.cycle();
      }
    });
  }

  // ✅ 4. PAUSE ON TOUCH (Mobile)
  carousel.addEventListener('touchstart', function() {
    const bsCarousel = bootstrap.Carousel.getInstance(carousel);
    if (bsCarousel) bsCarousel.pause();
  });

  carousel.addEventListener('touchend', function() {
    const bsCarousel = bootstrap.Carousel.getInstance(carousel);
    if (bsCarousel) {
      setTimeout(() => bsCarousel.cycle(), 3000); // Resume after 3s
    }
  });

  // ✅ 5. KEYBOARD NAVIGATION
  carousel.addEventListener('keydown', function(e) {
    const bsCarousel = bootstrap.Carousel.getInstance(carousel);
    if (!bsCarousel) return;
    
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      bsCarousel.prev();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      bsCarousel.next();
    }
  });

  // ✅ 6. RESPECT REDUCED MOTION
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    carousel.setAttribute('data-bs-interval', 'false');
    carousel.querySelectorAll('.carousel-item').forEach(item => {
      item.style.transition = 'none';
    });
  }

  // ✅ 7. SMOOTH SCROLL FOR BANNER CTA
  const bannerCTAs = carousel.querySelectorAll('.carousel-caption .btn[href^="#"]');
  bannerCTAs.forEach(btn => {
    btn.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href && href !== '#') {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // ✅ 8. FALLBACK: Force load all images after 3s
  setTimeout(() => {
    const unloadedImages = carousel.querySelectorAll('.banner-img:not(.loaded)');
    unloadedImages.forEach(img => {
      img.classList.add('loaded');
      const parent = img.closest('.carousel-item');
      if (parent) parent.classList.remove('loading');
    });
  }, 3000);

  // ✅ 9. ANALYTICS: Track banner views (if GA4/GTM exists)
  if (typeof gtag !== 'undefined') {
    carousel.addEventListener('slid.bs.carousel', function(e) {
      const activeSlide = carousel.querySelector('.carousel-item.active');
      const bannerTitle = activeSlide?.querySelector('h1, h2')?.textContent;
      
      gtag('event', 'banner_view', {
        'event_category': 'Banner',
        'event_label': bannerTitle || `Slide ${e.to + 1}`,
        'value': e.to + 1
      });
    });
  }

  // ✅ 10. PRECONNECT TO CDN (if using Cloudinary/ImgIX)
  const firstBanner = carousel.querySelector('.banner-img');
  if (firstBanner) {
    const src = firstBanner.getAttribute('src') || '';
    if (src.includes('cloudinary.com') || src.includes('imgix.net')) {
      const preconnect = document.createElement('link');
      preconnect.rel = 'preconnect';
      preconnect.href = src.includes('cloudinary') 
        ? 'https://res.cloudinary.com'
        : 'https://assets.imgix.net';
      preconnect.crossOrigin = 'anonymous';
      document.head.appendChild(preconnect);
    }
  }
});

// ==================== RESPONSIVE IMAGE SOURCE HANDLER ====================
// Force browser to re-evaluate <picture> on resize (debounced)
let resizeTimer;
window.addEventListener('resize', function() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function() {
    const carousel = document.getElementById('bannerCarousel');
    if (!carousel) return;
    
    const pictures = carousel.querySelectorAll('picture');
    pictures.forEach(picture => {
      const img = picture.querySelector('img');
      if (img) {
        // Force browser to re-check <source> media queries
        img.src = img.src; // Trigger re-evaluation
      }
    });
  }, 250);
});
window.addEventListener('load', function() {
    const loader = document.getElementById('page-loader');
    if (loader) {
    loader.style.opacity = '0';
    setTimeout(() => loader.remove(), 300);
    }
});
// ==================== FEATURED PROJECTS CAROUSEL WITH MOUSE DRAG ====================
(function () {
  "use strict";

  const carousel = document.getElementById("projectsCarousel");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const dotsContainer = document.getElementById("carouselDots");

  // Exit if carousel doesn't exist
  if (!carousel || !dotsContainer) {
    console.warn("Featured Projects Carousel: Required elements not found");
    return;
  }

  const slides = carousel.querySelectorAll(".project-slide");
  const totalSlides = slides.length;

  if (totalSlides === 0) {
    console.warn("Featured Projects Carousel: No slides found");
    return;
  }

  let currentIndex = 0;
  let autoSlideInterval = null;

  // Mouse drag variables
  let isDragging = false;
  let startPos = 0;
  let currentTranslate = 0;
  let prevTranslate = 0;
  let animationID = 0;

  // Configuration
  const config = {
    autoSlideDelay: 5000,
    transitionDuration: 600,
    dragThreshold: 50,
  };

  // ==================== INITIALIZATION ====================
  function init() {
    createDots();
    setupEventListeners();
    updateCarousel(false);
    startAutoSlide();

    // Pause when tab is hidden
    document.addEventListener("visibilitychange", handleVisibilityChange);

    // Handle window resize
    window.addEventListener("resize", debounce(handleResize, 250));

    console.log(
      `Featured Projects Carousel: Initialized with ${totalSlides} slides`
    );
  }

  // ==================== DOTS CREATION ====================
  function createDots() {
    dotsContainer.innerHTML = ""; // Clear existing dots

    slides.forEach((_, index) => {
      const dot = document.createElement("div");
      dot.className = "dot";
      if (index === 0) dot.classList.add("active");
      dot.setAttribute("aria-label", `Go to slide ${index + 1}`);
      dot.setAttribute("data-index", index);
      dot.addEventListener("click", () => goToSlide(index));
      dotsContainer.appendChild(dot);
    });

    console.log(`Created ${slides.length} dots`);
  }

  // ==================== CAROUSEL UPDATES ====================
  function updateCarousel(smooth = true) {
    // Set transition
    if (smooth) {
      carousel.style.transition = `transform ${config.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1)`;
    } else {
      carousel.style.transition = "none";
    }

    // Calculate and apply transform
    const offset = -currentIndex * 100;
    carousel.style.transform = `translateX(${offset}%)`;

    // Update dots
    const currentDots = dotsContainer.querySelectorAll(".dot");
    currentDots.forEach((dot, index) => {
      dot.classList.toggle("active", index === currentIndex);
    });

    // Update ARIA attributes
    slides.forEach((slide, index) => {
      slide.setAttribute("aria-hidden", index !== currentIndex);
    });
  }

  function goToSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    currentIndex = index;
    updateCarousel();
    resetAutoSlide();
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateCarousel();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateCarousel();
  }

  // ==================== AUTO SLIDE ====================
  function startAutoSlide() {
    stopAutoSlide(); // Clear any existing interval
    autoSlideInterval = setInterval(nextSlide, config.autoSlideDelay);
  }

  function stopAutoSlide() {
    if (autoSlideInterval) {
      clearInterval(autoSlideInterval);
      autoSlideInterval = null;
    }
  }

  function resetAutoSlide() {
    stopAutoSlide();
    startAutoSlide();
  }

  // ==================== DRAG FUNCTIONALITY ====================
  function getPositionX(event) {
    return event.type.includes("mouse")
      ? event.pageX
      : event.touches[0].clientX;
  }

  function dragStart(event) {
    // Ignore if clicking on buttons or links
    if (event.target.closest("a, button")) {
      return;
    }

    isDragging = true;
    startPos = getPositionX(event);
    animationID = requestAnimationFrame(animation);
    stopAutoSlide();

    carousel.style.cursor = "grabbing";
    carousel.classList.add("dragging");
  }

  function dragMove(event) {
    if (!isDragging) return;

    const currentPosition = getPositionX(event);
    const diff = currentPosition - startPos;
    currentTranslate = prevTranslate + diff;
  }

  function dragEnd() {
    if (!isDragging) return;

    isDragging = false;
    cancelAnimationFrame(animationID);

    carousel.style.cursor = "grab";
    carousel.classList.remove("dragging");

    const movedBy = currentTranslate - prevTranslate;

    // Determine if we should change slide
    if (Math.abs(movedBy) > config.dragThreshold) {
      if (movedBy < 0) {
        nextSlide();
      } else {
        prevSlide();
      }
    } else {
      updateCarousel();
    }

    prevTranslate = -currentIndex * carousel.offsetWidth;
    currentTranslate = prevTranslate;
    startAutoSlide();
  }

  function animation() {
    if (!isDragging) return;

    const slideWidth = carousel.offsetWidth;
    const maxTranslate = 0;
    const minTranslate = -(totalSlides - 1) * slideWidth;

    // Limit dragging beyond boundaries
    if (currentTranslate > maxTranslate) {
      currentTranslate = maxTranslate + (currentTranslate - maxTranslate) * 0.3; // Rubber band effect
    }
    if (currentTranslate < minTranslate) {
      currentTranslate = minTranslate + (currentTranslate - minTranslate) * 0.3;
    }

    const percentageTranslate = (currentTranslate / slideWidth) * 100;

    carousel.style.transition = "none";
    carousel.style.transform = `translateX(${percentageTranslate}%)`;

    animationID = requestAnimationFrame(animation);
  }

  // ==================== EVENT LISTENERS ====================
  function setupEventListeners() {
    // Mouse events
    carousel.addEventListener("mousedown", dragStart);
    carousel.addEventListener("mousemove", dragMove);
    carousel.addEventListener("mouseup", dragEnd);
    carousel.addEventListener("mouseleave", () => {
      if (isDragging) dragEnd();
    });

    // Touch events
    carousel.addEventListener("touchstart", dragStart, { passive: true });
    carousel.addEventListener("touchmove", dragMove, { passive: true });
    carousel.addEventListener("touchend", dragEnd);

    // Prevent context menu and text selection
    carousel.addEventListener("contextmenu", (e) => e.preventDefault());
    carousel.addEventListener("dragstart", (e) => e.preventDefault());

    // Set cursor style
    carousel.style.cursor = "grab";

    // Hover to pause auto-slide
    carousel.addEventListener("mouseenter", stopAutoSlide);
    carousel.addEventListener("mouseleave", () => {
      if (!isDragging) startAutoSlide();
    });

    // Keyboard navigation
    document.addEventListener("keydown", handleKeyboard);

    // Button events (if visible)
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        nextSlide();
        resetAutoSlide();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        prevSlide();
        resetAutoSlide();
      });
    }
  }

  // ==================== UTILITY FUNCTIONS ====================
  function handleKeyboard(e) {
    // Only handle if carousel is in viewport
    const rect = carousel.getBoundingClientRect();
    const isInView = rect.top < window.innerHeight && rect.bottom >= 0;

    if (!isInView) return;

    if (e.key === "ArrowLeft") {
      prevSlide();
      resetAutoSlide();
    } else if (e.key === "ArrowRight") {
      nextSlide();
      resetAutoSlide();
    }
  }

  function handleVisibilityChange() {
    if (document.hidden) {
      stopAutoSlide();
    } else {
      startAutoSlide();
    }
  }

  function handleResize() {
    prevTranslate = -currentIndex * carousel.offsetWidth;
    currentTranslate = prevTranslate;
    updateCarousel(false);
  }

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // ==================== CLEANUP ====================
  function destroy() {
    stopAutoSlide();
    document.removeEventListener("visibilitychange", handleVisibilityChange);
    window.removeEventListener("resize", handleResize);
    document.removeEventListener("keydown", handleKeyboard);
    console.log("Featured Projects Carousel: Destroyed");
  }

  // Expose destroy method globally if needed
  window.destroyProjectsCarousel = destroy;

  // Initialize carousel
  init();
})();
/**
 * Chatbot Widget - MOBILE OPTIMIZED
 * ✅ Full màn hình + Tắt auto-focus bàn phím
 */

class ChatbotWidget {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.remainingRequests = 20;

        // DOM elements
        this.chatButton = document.getElementById('chatbotButton');
        this.chatWidget = document.getElementById('chatbotWidget');
        this.closeBtn = document.getElementById('chatbotCloseBtn');
        this.messagesContainer = document.getElementById('chatbotMessages');
        this.userInput = document.getElementById('chatbotInput');
        this.sendBtn = document.getElementById('chatbotSendBtn');
        this.resetBtn = document.getElementById('chatbotResetBtn');
        this.requestCountEl = document.getElementById('requestCount');

        if (!this.chatButton || !this.chatWidget) {
            console.error('Chatbot elements not found');
            return;
        }

        this.init();
    }

    init() {
        this.chatButton.addEventListener('click', () => this.toggleChat());
        this.closeBtn.addEventListener('click', () => this.toggleChat());
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.resetBtn.addEventListener('click', () => this.resetChat());

        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // ❌ XÓA AUTO-FOCUS - KHÔNG CÒN TỰ ĐỘNG MỞ BÀN PHÍM
        // Không dùng transitionend để focus nữa

        console.log('Chatbot initialized successfully');
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatWidget.classList.toggle('active');

        // ✅ THÊM/XÓA CLASS VÀO BODY
        if (this.isOpen) {
            document.body.classList.add('chatbot-open');
            this.scrollToBottom();

            // Fix cho iOS: Ngăn body scroll
            if (this.isMobile()) {
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'fixed';
                document.body.style.width = '100%';
                document.body.style.top = '0';
            }
        } else {
            document.body.classList.remove('chatbot-open');

            // Khôi phục scroll
            if (this.isMobile()) {
                document.body.style.overflow = '';
                document.body.style.position = '';
                document.body.style.width = '';
                document.body.style.top = '';
            }
        }
    }

    isMobile() {
        return window.innerWidth <= 768;
    }

    async sendMessage() {
        const message = this.userInput.value.trim();

        if (!message || this.isTyping) {
            return;
        }

        if (message.length > 500) {
            alert('Tin nhắn quá dài! Vui lòng nhập tối đa 500 ký tự.');
            return;
        }

        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.setInputState(false);
        this.showTyping();

        try {
            const response = await fetch('/chatbot/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            this.hideTyping();

            if (response.ok) {
                this.addMessage(data.response, 'bot');

                if (data.remaining_requests !== undefined) {
                    this.remainingRequests = data.remaining_requests;
                    this.updateRequestCount();
                }
            } else {
                this.addMessage(
                    data.error || data.response || 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại! 😊',
                    'bot'
                );
            }

        } catch (error) {
            console.error('Chatbot error:', error);
            this.hideTyping();
            this.addMessage(
                'Xin lỗi, không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng! 🔌',
                'bot'
            );
        } finally {
            this.setInputState(true);
            // ❌ KHÔNG FOCUS SAU KHI GỬI - TRÁNH MỞ BÀN PHÍM
            // this.userInput.focus(); // Đã xóa dòng này
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'chatbot-message-content';
        contentDiv.innerHTML = this.escapeHtml(text).replace(/\n/g, '<br>');

        messageDiv.appendChild(contentDiv);
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showTyping() {
        this.isTyping = true;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot';
        typingDiv.id = 'chatbotTypingIndicator';

        const typingContent = document.createElement('div');
        typingContent.className = 'chatbot-typing';
        typingContent.innerHTML = '<span></span><span></span><span></span>';

        typingDiv.appendChild(typingContent);
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTyping() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('chatbotTypingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    setInputState(enabled) {
        this.userInput.disabled = !enabled;
        this.sendBtn.disabled = !enabled;
        this.sendBtn.style.opacity = enabled ? '1' : '0.5';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }

    async resetChat() {
        if (!confirm('Bạn có chắc muốn làm mới hội thoại? Tất cả tin nhắn sẽ bị xóa.')) {
            return;
        }

        try {
            const response = await fetch('/chatbot/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const messages = this.messagesContainer.querySelectorAll('.chatbot-message');
                messages.forEach((msg, index) => {
                    if (index > 0) {
                        msg.remove();
                    }
                });

                this.remainingRequests = 20;
                this.updateRequestCount();
                this.addMessage('Đã làm mới hội thoại! Tôi có thể giúp gì cho bạn? 😊', 'bot');
            }
        } catch (error) {
            console.error('Reset error:', error);
            alert('Không thể làm mới hội thoại. Vui lòng thử lại!');
        }
    }

    updateRequestCount() {
        if (this.requestCountEl) {
            this.requestCountEl.textContent = `Còn ${this.remainingRequests} tin nhắn`;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chatbotButton')) {
        new ChatbotWidget();
    }
});
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