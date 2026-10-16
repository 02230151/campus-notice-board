from pathlib import Path
from html import escape

department = "Department of Computing Technologies Department"

notices = []

for line in Path("/input/notices.txt").read_text().splitlines():
    title, date, body = line.split(" | ", 2)
    notices.append((title, date, body))

html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Campus Notice Board</title>
</head>
<body>
    <h1>Campus Notice Board</h1>
    <h2>{escape(department)}</h2>
"""

for title, date, body in notices:
    html += f"""
    <article>
        <h3>{escape(title)}</h3>
        <p><strong>Date:</strong> {escape(date)}</p>
        <p>{escape(body)}</p>
    </article>
    """

html += """
</body>
</html>
"""

Path("/output/index.html").write_text(html)