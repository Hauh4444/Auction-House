from flask import jsonify, Response

import matplotlib.pyplot as plt
import io, base64


class AnalyticsService:
    @staticmethod
    def get_login_data():
        """
        Retrieves login data analytics and generates a chart.
        Returns a base64 image or HTML for rendering in the frontend.
        """
        # Mock data for chart
        mock_data = [
            ("01-01-2025", 1287),
            ("02-01-2025", 786),
            ("03-01-2025", 254),
            ("04-01-2025", 653),
            ("05-01-2025", 526),
            ("06-01-2025", 1123),
            ("07-01-2025", 1024),
            ("08-01-2025", 950),
            ("09-01-2025", 857)
        ]

        labels = [row[0] for row in mock_data]
        values = [row[1] for row in mock_data]

        # Generate the chart using matplotlib
        fig, ax = plt.subplots()
        ax.plot(labels, values, marker='o')
        ax.set(xlabel='Date', ylabel='Logins', title='Login Data Over Time')
        ax.grid()

        # Save the plot as a PNG image in memory
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close(fig)

        # Convert the image to base64
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

        # Return the base64 image for frontend rendering
        response_data = {"message": "Chart successfully created", "chart": f'<img src="data:image/png;base64,{img_base64}" alt="Login Chart"/>'}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")