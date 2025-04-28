import {getCLS, getFID, getLCP} from 'https://unpkg.com/web-vitals@3/dist/web-vitals.iife.js';

function sendToPostHog(metric) {
    posthog.capture('web_vital', {
        name: metric.name,
        value: metric.value,
        id: metric.id,
    });
}

getCLS(sendToPostHog);
getFID(sendToPostHog);
getLCP(sendToPostHog);
