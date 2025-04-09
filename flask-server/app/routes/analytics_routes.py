from flask import Blueprint, render_template, jsonify

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics_dashboard():
    """
    Render a simple HTML page with a link to the PostHog dashboard.
    Useful for admins to review user behavior analytics.
    """
    return render_template('analytics.html')


@analytics_bp.route('/api/summary')
def summary():
    """
    API endpoint that returns a basic summary message.
    This can be expanded to return real-time metrics later.
    """
    return jsonify({
        'message': 'Analytics are tracked via PostHog.',
        'dashboard_link': 'https://us.posthog.com/project/145970' #this is a link associated with Posthog
    })
