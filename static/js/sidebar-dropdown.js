$(document).ready(function() {
    // Handle sidebar dropdown toggle
    $('.nav-sidebar .has-treeview > a').on('click', function(e) {
        e.preventDefault();
        
        var $parentItem = $(this).parent('.has-treeview');
        
        // Close other open menus
        $('.nav-sidebar .has-treeview').not($parentItem).removeClass('menu-open');
        $('.nav-sidebar .nav-treeview').not($parentItem.find('.nav-treeview')).slideUp();
        
        // Toggle current menu
        $parentItem.toggleClass('menu-open');
        $parentItem.find('> .nav-treeview').slideToggle();
    });
    
    // Set active menu item based on current URL
    var currentUrl = window.location.pathname;
    $('.nav-sidebar a').each(function() {
        if ($(this).attr('href') === currentUrl) {
            $(this).addClass('active');
            $(this).parents('.has-treeview').addClass('menu-open');
            $(this).parents('.nav-treeview').show();
        }
    });
});
