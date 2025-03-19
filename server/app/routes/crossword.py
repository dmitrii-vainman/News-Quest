from fastapi import APIRouter
from app.puzzle.generator import CrosswordGenerator
import sys
from pydantic import BaseModel
from typing import Dict

# Make sure the path to crossword-puzzle-maker is correct
sys.path.append("external_libs/crossword-puzzle-maker")

from crossword import Crossword  # Import from the library

router = APIRouter()

class CrosswordInput(BaseModel):
    words: Dict[str, str]  # Dictionary of words and clues

@router.post("/generate-crossword")
def generate_crossword(data: CrosswordInput):
    # Generate crossword puzzle
    puzzle = Crossword.generate(data.words)

    return {
        "grid": puzzle.grid,
        "clues": puzzle.clues
    }

router = APIRouter()

@router.get("/generate_puzzle")
def generate_puzzle():
    words = ["PYTHON", "FASTAPI", "CROSSWORD", "PUZZLE"]
    crossword = CrosswordGenerator(size=10)
    grid = crossword.generate(words)
    return {"crossword": grid.tolist()}  # Convert NumPy array to list
