import sqlite3
import dotenv
from openai import OpenAI
import os
import re

# Load environment variables
dotenv.load_dotenv()
# Initialize OpenAI client
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
# Function to generate clue for a word based on a headline
def generate_clue_for_word(headline):
    try:
        # Make the API call to generate a crossword clue
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a single word and a short crossword clue for it, based on this headline: '{headline}'."
                }
            ],
            max_tokens=50
        )

        
        clue_text = response.choices[0].message.content.strip()
        return clue_text
    except Exception as e:
        print(f"Error generating clue: {e}")
        return None

# Function to fetch headlines from the database based on source
def fetch_headlines_from_db(source, limit=2):
    conn = sqlite3.connect('../db/news.db')
    cursor = conn.cursor()
    
    # Fetch 10 headlines from the 'headlines' table based on source
    cursor.execute("SELECT id, title FROM headlines WHERE source=? LIMIT ?", (source, limit))
    headlines = cursor.fetchall()
    conn.close()
    
    return headlines

# Function to generate word and clue pairs and save them to the database
def generate_and_save_clues(source):
    headlines = fetch_headlines_from_db(source)
    
    # Connect to the database to insert the clues
    conn = sqlite3.connect('../db/news.db')
    cursor = conn.cursor()
    
    for headline_id, headline in headlines:
        # Generate a clue for each headline
        clue = generate_clue_for_word(headline)
        
        if clue:
            # Use regex to extract the word after "Word:" and before "Clue:"
            match = re.search(r'\*\*(.*?)\*\*', clue)  # Looks for bold text in markdown format
            word = match.group(1) if match else "UNKNOWN"  # Fallback to "UNKNOWN" if not found
            
            # Save the word and clue to the 'clues' table
            cursor.execute("INSERT INTO clues (word, clue, headline_id, source) VALUES (?, ?, ?, ?);", 
                        (word, clue, headline_id, source))
            print(f"Saved clue: {word} - {clue} (from '{headline}')")
    
    conn.commit()
    conn.close()

# Run the generation and saving process for a specific source
def run():
    source = 'Reddit'  # Change this to 'NewsAPI' or 'HackerNews' as needed
    generate_and_save_clues(source)

# Run the script
run()
