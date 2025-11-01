$(document).ready(function() {
    // Add overlay div if it doesn't exist
    if ($('.main-overlay').length === 0) {
        $('body').append('<div class="main-overlay"></div>');
    }

    // Handle sidebar toggle
    $('[data-widget="pushmenu"]').on('click', function(e) {
        e.preventDefault();
        if ($(window).width() <= 991.98) {
            $('body').toggleClass('sidebar-open');
        } else {
            $('body').toggleClass('sidebar-collapse');
        }
    });

    // Close sidebar when clicking overlay
    $('.main-overlay').on('click', function() {
        $('body').removeClass('sidebar-open');
    });

    // Handle window resize
    $(window).on('resize', function() {
        if ($(window).width() > 991.98) {
            $('body').removeClass('sidebar-open');
            $('.main-overlay').hide();
        }
    });

    // Ensure proper dropdown behavior
    $('.nav-sidebar .nav-link').on('click', function(e) {
        if ($(this).next('.nav-treeview').length) {
            e.preventDefault();
            $(this).parent().toggleClass('menu-open');
        }
    });
});

