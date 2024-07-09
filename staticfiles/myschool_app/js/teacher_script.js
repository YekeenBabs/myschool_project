document.addEventListener("DOMContentLoaded", function() {
    // Sidebar submenu toggle
    const sidebarMenuItems = document.querySelectorAll(".sidebar ul li a");

    sidebarMenuItems.forEach(item => {
        item.addEventListener("click", function(event) {
            const submenu = this.nextElementSibling;

            if (submenu && submenu.classList.contains("submenu")) {
                event.preventDefault();

                submenu.classList.toggle("active");
                submenu.querySelector("ul").classList.toggle("active");
            }
        });
    });
    
    // Accordion toggle for teacher lectures
    var accordionItems = document.querySelectorAll('.card-header button');

    accordionItems.forEach(function(button) {
        button.addEventListener('click', function() {
            var parent = button.closest('.card');
            var collapse = parent.querySelector('.collapse');
            if (collapse.classList.contains('show')) {
                collapse.classList.remove('show');
            } else {
                document.querySelectorAll('.collapse.show').forEach(function(item) {
                    item.classList.remove('show');
                });
                collapse.classList.add('show');
            }
        });
    });

    // Toggle sidebar submenu in teacher_base
    const submenuLinks = document.querySelectorAll('.sidebar .nav .submenu > a');
    submenuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            const submenu = parent.querySelector('ul');
            if (parent.classList.contains('active')) {
                submenu.style.display = 'none';
                parent.classList.remove('active');
            } else {
                submenu.style.display = 'block';
                parent.classList.add('active');
            }
        });
    });

    // Toggle mobile menu in teacher_base
    const toggleBtn = document.getElementById('toggle_btn');
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.querySelector('.main-wrapper');
    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        mainWrapper.classList.toggle('active');
    });

    // Handle window resize for sidebar visibility in teacher_base
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            mainWrapper.classList.remove('active');
        }
    });

    // Tab navigation for teacher grading assignments
    const tabLinks = document.querySelectorAll('#myTab a');
    tabLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            tabLinks.forEach(function(link) {
                const pane = document.querySelector(link.getAttribute('href'));
                pane.classList.remove('show', 'active');
                link.classList.remove('active');
            });
            target.classList.add('show', 'active');
            this.classList.add('active');
        });
    });
});

// Function to confirm lesson
function confirmLesson(lessonId) {
    // Assume there's an AJAX call to update lesson status
    // Here's just a console log for demonstration
    console.log('Lesson confirmed:', lessonId);
}

// Function to reschedule lesson
function rescheduleLesson(lessonId) {
    // Assume there's a modal or form to reschedule the lesson
    // Here's just a console log for demonstration
    console.log('Reschedule lesson:', lessonId);
}

// Document ready function for additional initialization (if needed)
$(document).ready(function() {
    // Add event listeners or any other initialization here
});
