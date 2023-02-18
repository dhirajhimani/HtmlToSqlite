import os
import re
import sqlite3

from bs4 import BeautifulSoup

# Connect to the SQLite database
conn = sqlite3.connect('vintage_jokes.db')
c = conn.cursor()

# Create a table to hold the text content
c.execute('''
    CREATE TABLE text_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_content TEXT,
        read TEXT,
        likes TEXT
    )
''')

# Loop through HTML files in a directory and insert them into the database
html_dir = '../assets/dirtyjokes'
for filename in os.listdir(html_dir):
    if filename.endswith('.htm') or filename.endswith('.html'):
        with open(os.path.join(html_dir, filename), 'r') as f:
            # Parse the HTML file
            soup = BeautifulSoup(f, 'html.parser')
            lines = soup.find_all("p")

            for line in lines:
                if len(line.text.strip()) > 0:
                    formatted_line = line.text.strip().replace("\n", " ")
                    formatted_line = re.sub(r"\s+", " ", formatted_line)
                    # Insert the text content into the database
                    c.execute('INSERT INTO text_content (text_content) VALUES (?)',
                              (formatted_line,))

# Commit the changes and close the database connection
conn.commit()
conn.close()
