import openai
import random
import time
import os
from typing import Dict, List, Optional

class GameGenerator:
    def __init__(self, api_key: str):
        """Initialize the game generator with OpenAI API key."""
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.api_key = api_key
        openai.api_key = self.api_key
        
    def generate_games(self, job_role: str) -> Dict[str, List[Dict]]:
        """Generate games based on job role for each difficulty level."""
        try:
            prompt = f"""
            Create 3 fun and engaging mini-games for someone pursuing a career as a {job_role}.
            The games should be related to skills needed for this role.
            
            For each difficulty level (Easy, Medium, Complex), create 1 game.
            Each game should:
            1. Have a catchy, funny title
            2. Be playable in a terminal/text interface
            3. Be related to {job_role} skills
            4. Include clear instructions
            5. Have scoring or winning conditions
            6. Include 3 sample questions/challenges with correct answers
            
            Return the response in this exact JSON format:
            {{
                "easy": [{{
                    "title": "Funny game title",
                    "description": "Brief game description",
                    "instructions": "How to play",
                    "scoring": "How scoring works",
                    "win_condition": "How to win",
                    "questions": [
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 10
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 10
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 10
                        }}
                    ]
                }}],
                "medium": [{{
                    "title": "Funny game title",
                    "description": "Brief game description",
                    "instructions": "How to play",
                    "scoring": "How scoring works",
                    "win_condition": "How to win",
                    "questions": [
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 15
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 15
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 15
                        }}
                    ]
                }}],
                "complex": [{{
                    "title": "Funny game title",
                    "description": "Brief game description",
                    "instructions": "How to play",
                    "scoring": "How scoring works",
                    "win_condition": "How to win",
                    "questions": [
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 20
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 20
                        }},
                        {{
                            "question": "Question text",
                            "correct_answer": "Answer text",
                            "points": 20
                        }}
                    ]
                }}]
            }}
            
            Make sure the questions are:
            1. Relevant to the job role
            2. Fun and engaging
            3. Educational
            4. Appropriate for the difficulty level
            5. Have clear correct answers
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are a creative game designer who specializes in creating fun, educational games related to different career paths."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.8
            )
            
            return eval(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating games: {str(e)}")
            return None
            
    def play_game(self, game: Dict) -> None:
        """
        Play a selected game.
        """
        print(f"\n🎮 {game['title'].upper()} 🎮")
        print(f"\n📝 Description: {game['description']}")
        print(f"\n📋 Instructions: {game['instructions']}")
        print(f"\n🎯 Scoring: {game['scoring']}")
        print(f"\n🏆 Win Condition: {game['win_condition']}")
        
        input("\nPress Enter to start the game...")
        print("\nGame starting in...")
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        print("GO!")
        
        # Game logic will be implemented based on the specific game
        if "word" in game['title'].lower():
            self._play_word_game(game)
        elif "quiz" in game['title'].lower():
            self._play_quiz_game(game)
        elif "puzzle" in game['title'].lower():
            self._play_puzzle_game(game)
        else:
            self._play_generic_game(game)
            
    def _play_word_game(self, game: Dict) -> None:
        """Play a word-based game."""
        score = 0
        rounds = 3
        
        for round_num in range(1, rounds + 1):
            print(f"\nRound {round_num}/{rounds}")
            answer = input("Your answer: ").strip().lower()
            if answer:  # Simple scoring for now
                score += len(answer)
            
        print(f"\nGame Over! Final Score: {score}")
        
    def _play_quiz_game(self, game: Dict) -> None:
        """Play a quiz-based game."""
        score = 0
        rounds = 5
        
        for round_num in range(1, rounds + 1):
            print(f"\nQuestion {round_num}/{rounds}")
            answer = input("Your answer: ").strip().lower()
            if answer:  # Simple scoring for now
                score += 10
            
        print(f"\nGame Over! Final Score: {score}")
        
    def _play_puzzle_game(self, game: Dict) -> None:
        """Play a puzzle-based game."""
        score = 0
        rounds = 3
        
        for round_num in range(1, rounds + 1):
            print(f"\nPuzzle {round_num}/{rounds}")
            answer = input("Your solution: ").strip().lower()
            if answer:  # Simple scoring for now
                score += 15
            
        print(f"\nGame Over! Final Score: {score}")
        
    def _play_generic_game(self, game: Dict) -> None:
        """Play a generic game type."""
        score = 0
        rounds = 4
        
        for round_num in range(1, rounds + 1):
            print(f"\nRound {round_num}/{rounds}")
            action = input("Your action: ").strip().lower()
            if action:  # Simple scoring for now
                score += 5
            
        print(f"\nGame Over! Final Score: {score}")
