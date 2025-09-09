document.addEventListener('DOMContentLoaded', function () {
    // Add copy functionality to code blocks
    const copyButtons = document.querySelectorAll('.copy-button');

    copyButtons.forEach(button => {
        button.addEventListener('click', function () {
            const codeBlock = this.parentElement.nextElementSibling;
            const textToCopy = codeBlock.textContent;

            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bx bx-check"></i> Copied!';

                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        });
    });

    // Simple navigation highlighting
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.section');

    // Highlight active section on scroll
    window.addEventListener('scroll', function () {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (pageYOffset >= (sectionTop - 100)) {
                current = section.getAttribute('id');
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === '#' + current) {
                item.classList.add('active');
            }
        });
    });

    // Smooth scrolling for navigation links
    navItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
});