// External Libraries
import { useEffect, useState } from "react";
import { onCLS, onFID, onFCP, onLCP, onTTFB } from "web-vitals";
import posthog from "posthog-js";
import PropTypes from "prop-types";

// Internal Modules
import { WebVitalsContext } from "./WebVitalsContext";

const WebVitalsProvider = ({ children }) => {
    const [vitals, setVitals] = useState({});

    useEffect(() => {
        const reportMetric = (metric) => {
            setVitals(prev => ({
                ...prev,
                [metric.name]: metric,
            }));

            // Optionally send to PostHog
            if (import.meta.env.PROD) {
                posthog.capture("web_vitals", {
                    name: metric.name,
                    value: metric.value,
                    id: metric.id,
                    delta: metric.delta,
                });
            }
        };

        onCLS(reportMetric);
        onFID(reportMetric);
        onFCP(reportMetric);
        onLCP(reportMetric);
        onTTFB(reportMetric);
    }, []);

    return (
        <WebVitalsContext.Provider value={vitals}>
            {children}
        </WebVitalsContext.Provider>
    );
};

WebVitalsProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export default WebVitalsProvider;
