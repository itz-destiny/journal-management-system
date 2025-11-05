$(document).ready(function() {
    // Initialize sidebar
    initSidebar();
    
    function initSidebar() {
        // Handle dropdown toggle
        $('.nav-sidebar .has-treeview > a').off('click').on('click', function(e) {
            e.preventDefault();
            
            var $parentItem = $(this).parent('.has-treeview');
            var $treeview = $parentItem.find('> .nav-treeview');
            
            // Toggle current menu
            if ($parentItem.hasClass('menu-open')) {
                $parentItem.removeClass('menu-open');
                $treeview.slideUp(200);
            } else {
                // Close other open menus
                $('.nav-sidebar .has-treeview').not($parentItem).removeClass('menu-open');
                $('.nav-sidebar .nav-treeview').not($treeview).slideUp(200);
                
                // Open current menu
                $parentItem.addClass('menu-open');
                $treeview.slideDown(200);
            }
        });
        
        // Set active menu item based on current URL
        var currentUrl = window.location.pathname;
        $('.nav-sidebar a').each(function() {
            var linkUrl = $(this).attr('href');
            if (linkUrl && linkUrl !== '#' && currentUrl.indexOf(linkUrl) !== -1 && linkUrl !== '/') {
                $(this).addClass('active');
                // Open parent menu if this is a submenu item
                var $parentTreeview = $(this).closest('.has-treeview');
                if ($parentTreeview.length) {
                    $parentTreeview.addClass('menu-open');
                    $parentTreeview.find('> .nav-treeview').show();
                }
            }
        });
    }
    
    // Handle pushmenu (sidebar toggle on mobile)
    $('[data-widget="pushmenu"]').off('click').on('click', function(e) {
        e.preventDefault();
        $('body').toggleClass('sidebar-open');
        $('body').toggleClass('sidebar-collapse');
    });
    
    // Close sidebar when clicking outside on mobile
    $(document).on('click', function(e) {
        if ($('body').hasClass('sidebar-open') && 
            !$(e.target).closest('.main-sidebar').length && 
            !$(e.target).closest('[data-widget="pushmenu"]').length) {
            $('body').removeClass('sidebar-open');
        }
    });
    
    // Re-initialize after AJAX or dynamic content
    $(document).on('DOMContentLoaded', initSidebar);
});