window.addEventListener('beforeunload', function() {
    posthog.capture('page_leave', {
        current_url: window.location.href,
        timestamp: new Date().toISOString()
    });
});
