window.onerror = function(message, source, lineno, colno, error) {
    posthog.capture('frontend_error', {
        message: message,
        source: source,
        lineno: lineno,
        colno: colno,
        error: error ? JSON.stringify(error) : null
    });
};
