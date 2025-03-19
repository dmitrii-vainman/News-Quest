from fastapi import APIRouter
from app.puzzle.generator import CrosswordGenerator

router = APIRouter()

@router.get("/generate_puzzle")
def generate_puzzle():
    words = ["PYTHON", "FASTAPI", "CROSSWORD", "PUZZLE"]
    crossword = CrosswordGenerator(size=10)
    grid = crossword.generate(words)
    return {"crossword": grid.tolist()}  # Convert NumPy array to list
