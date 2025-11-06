// GYMFIT BANGLADESH - MAIN JAVASCRIPT
// Developed by: Al Shahriar

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // ========== MOBILE MENU TOGGLE ==========
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.navbar')) {
            navMenu.classList.remove('active');
            if (mobileToggle) {
                const icon = mobileToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
    
    // ========== SMOOTH SCROLLING ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu after clicking
                navMenu.classList.remove('active');
            }
        });
    });
    
    // ========== ACTIVE NAVIGATION ==========
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    function setActiveNav() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', setActiveNav);
    
    // ========== SCROLL TO TOP BUTTON ==========
    const scrollTopBtn = document.getElementById('scrollTop');
    
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('active');
            } else {
                scrollTopBtn.classList.remove('active');
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ========== HEADER BACKGROUND ON SCROLL ==========
    const header = document.querySelector('.main-header');
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 100) {
            header.style.boxShadow = '0 5px 30px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        }
    });
    
    // ========== ANIMATION ON SCROLL ==========
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Add animation to elements
    document.querySelectorAll('.service-card, .class-card, .trainer-card, .why-card, .pricing-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
    
    // ========== COUNTER ANIMATION ==========
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current) + '+';
            }
        }, 20);
    }
    
    // Animate stat numbers when in view
    const statObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const h3 = entry.target.querySelector('h3');
                const target = parseInt(h3.textContent);
                if (!isNaN(target)) {
                    animateCounter(h3, target);
                }
                statObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.stat-box').forEach(stat => {
        statObserver.observe(stat);
    });
    
    // ========== NEWSLETTER FORM ==========
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            alert('Thank you for subscribing! We will send updates to: ' + email);
            this.reset();
        });
    }
    
    // ========== CONTACT FORM ==========
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for your message! We will contact you soon.');
            this.reset();
        });
    }
    
    // ========== TESTIMONIAL SLIDER ==========
    const testimonials = [
        {
            image: 'https://i.pravatar.cc/150?img=15',
            text: 'GymFit Bangladesh changed my life! I lost 15kg in 3 months with their amazing trainers and personalized diet plan. Best gym in Dhaka!',
            name: 'Sakib Rahman',
            title: 'Software Engineer'
        },
        {
            image: 'https://i.pravatar.cc/150?img=32',
            text: 'The trainers are very professional and supportive. The facilities are clean and well-maintained. Highly recommend for anyone serious about fitness!',
            name: 'Nusrat Jahan',
            title: 'Doctor'
        },
        {
            image: 'https://i.pravatar.cc/150?img=51',
            text: 'Great gym with excellent equipment and friendly staff. The membership prices are very reasonable compared to other gyms in Dhaka. Love it!',
            name: 'Tanvir Ahmed',
            title: 'Business Owner'
        }
    ];
    
    let currentTestimonial = 0;
    const dots = document.querySelectorAll('.testimonial-dots .dot');
    
    function showTestimonial(index) {
        const testimonialCard = document.querySelector('.testimonial-card');
        if (!testimonialCard) return;
        
        const data = testimonials[index];
        
        testimonialCard.querySelector('.testimonial-image img').src = data.image;
        testimonialCard.querySelector('.testimonial-content p').textContent = data.text;
        testimonialCard.querySelector('.testimonial-content h4').textContent = data.name;
        testimonialCard.querySelector('.testimonial-content span').textContent = data.title;
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    // Auto rotate testimonials
    setInterval(() => {
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        showTestimonial(currentTestimonial);
    }, 5000);
    
    // Manual testimonial navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentTestimonial = index;
            showTestimonial(index);
        });
    });
    
    // ========== LOADING ANIMATION ==========
    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s';
            document.body.style.opacity = '1';
        }, 100);
    });
    
    console.log('GymFit Bangladesh - Developed by Al Shahriar');
});