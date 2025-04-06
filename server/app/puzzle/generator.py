import sqlite3
import dotenv
from openai import OpenAI
import os
import json

# Load environment variables
dotenv.load_dotenv()

# Initialize OpenAI client
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Function to reset the clues table (drop and recreate)
def reset_clues_table():
    try:
        conn = sqlite3.connect('../db/news.db')
        cursor = conn.cursor()

        # Drop the clues table if it exists
        cursor.execute("DROP TABLE IF EXISTS clues;")

        # Recreate the clues table with proper schema and AUTOINCREMENT
        cursor.execute('''
            CREATE TABLE clues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                clue TEXT NOT NULL,
                headline_id INTEGER,
                source TEXT,
                FOREIGN KEY (headline_id) REFERENCES headlines(id)
            );
        ''')

        conn.commit()
        conn.close()
        print("Clues table has been reset.")
    except Exception as e:
        print(f"Error resetting clues table: {e}")

# Function to generate clue for a word based on a headline
def generate_clue_for_word(headline):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": (
                    "Generate a single word and a short, witty, clear, and concise crossword clue for it, "
                    f"based on this headline: '{headline}'.\n"
                    "Respond only in JSON format without explanations.\n"
                    'Example response: { "word": "Bitcoin", "clue": "An expensive non-physical currency." }'
                )
            }],
            max_tokens=100
        )

        response_text = response.choices[0].message.content.strip()
        clue_data = json.loads(response_text)  # Convert string to dictionary

        word = clue_data.get("word", "UNKNOWN")
        clue = clue_data.get("clue", "No clue available.")

        return word, clue  # Return only the extracted data
    except Exception as e:
        print(f"Error generating clue: {e}")
        return None, None

# Function to fetch headlines from the database
def fetch_headlines_from_db(source, limit=12):
    conn = sqlite3.connect('../db/news.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title FROM headlines WHERE source=? LIMIT ?", (source, limit))
    headlines = cursor.fetchall()
    conn.close()
    
    return headlines

# Function to generate and save clues
def generate_and_save_clues(source):
    headlines = fetch_headlines_from_db(source)
    
    conn = sqlite3.connect('../db/news.db')
    cursor = conn.cursor()
    
    for headline_id, headline in headlines:
        word, clue = generate_clue_for_word(headline)
        
        if word and clue:  # Check if clue generation was successful
            cursor.execute(
                "INSERT INTO clues (word, clue, headline_id, source) VALUES (?, ?, ?, ?);",
                (word, clue, headline_id, source)
            )
            print(f"Saved clue: {word} - {clue} (from '{headline}')")
        else:
            print(f"Skipped clue generation for headline '{headline}' due to invalid result.")
    
    conn.commit()  # Commit only once after all insertions
    conn.close()



def run(source):
    generate_and_save_clues(source)

def runALL():
    # First, reset the clues table by dropping and recreating it
    reset_clues_table()
    
    sources = ['HackerNews', 'Reddit','NewsAPI']
    
    for source in sources:
        run(source)

runALL()

