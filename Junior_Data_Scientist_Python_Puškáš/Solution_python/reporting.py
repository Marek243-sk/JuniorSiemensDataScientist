import pandas as pd

def get_gradient_color(percent_diff):

    # Returns a color based on the size of the percent difference.
    if percent_diff <= 0.20: return "green"
    elif percent_diff <= 0.5: return "yellow"
    elif percent_diff <= 0.8: return "orange"
    else: return "red"

def generate_statistics_report(statistics_differences):

    # Convert list of statistics differences to DataFrame
    stats_report = pd.DataFrame(statistics_differences)
    
    # Apply color-coded HTML formatting to the 'percent_difference' column
    for idx, row in stats_report.iterrows():
        color = get_gradient_color(row["percent_difference"])
        text_color = "black" if color == "yellow" else "white"
        stats_report.loc[idx, 'Change'] = (
            f'<span style="background-color:{color}; padding: 5px; color: {text_color}; border-radius: 4px;">'
            f'{row["percent_difference"]*100:.2f}%</span>'
        )

    # Convert DataFrame to HTML with custom class
    html_table = stats_report.to_html(index=False, escape=False, classes="styled-table")

    # Wrap table in complete HTML document with CSS styles
    full_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
            }}
            .styled-table {{
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.95em;
                min-width: 600px;
                border: 1px solid #ddd;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .styled-table thead tr {{
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }}
            .styled-table th, .styled-table td {{
                padding: 12px 15px;
                border: 1px solid #ddd;
            }}
            .styled-table tbody tr:nth-child(even) {{
                background-color: #f3f3f3;
            }}
        </style>
    </head>
    <body>
        <h1>Comparison Report</h1>
        <h2>Statistics Differences</h2>
        {html_table}
    </body>
    </html>
    """
    return full_html
