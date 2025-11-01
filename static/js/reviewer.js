function filterArticles(status) {
    // Get the base URL for the reviewer
    const baseUrl = '/reviewer/';
    
    // Map status to corresponding URLs
    const urlMap = {
        'under-review': 'user-under-review-articles/',
        'accepted': 'user-accepted/',
        'rejected': 'user-rejected/'
    };
    
    // Get the user ID from the page (you'll need to add this as a data attribute somewhere)
    const userId = document.querySelector('[data-user-id]').getAttribute('data-user-id');
    
    // Navigate to the appropriate URL
    if (urlMap[status]) {
        window.location.href = baseUrl + urlMap[status] + userId + '/';
    }
}
