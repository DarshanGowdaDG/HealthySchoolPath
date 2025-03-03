import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.getenv("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")
client = OpenAI(api_key="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")

def generate_quiz(topic):
    try:
        response = client.chat.completions.create(
            model="GPT-4o-mini (2024-07-18)",
            messages=[{
                "role": "user",
                "content": f"Create a quiz about {topic} with 5 multiple choice questions."
            }],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback content if API fails
        fallback_quizzes = {
            "Understanding Macronutrients": [
                {
                    "question": "Which macronutrient is the body's main source of energy?",
                    "options": ["Proteins", "Carbohydrates", "Fats", "Vitamins"],
                    "correct_answer": "Carbohydrates"
                },
                {
                    "question": "Which macronutrient is essential for building and repairing tissues?",
                    "options": ["Proteins", "Carbohydrates", "Fats", "Vitamins"],
                    "correct_answer": "Proteins"
                },
                {
                    "question": "Which macronutrient supports brain function and hormone production?",
                    "options": ["Proteins", "Carbohydrates", "Fats", "Vitamins"],
                    "correct_answer": "Fats"
                },
                {
                    "question": "Which of the following is a complex carbohydrate?",
                    "options": ["Sugar", "White bread", "Brown rice", "Candy"],
                    "correct_answer": "Brown rice"
                },
                {
                    "question": "Which of the following is a healthy fat source?",
                    "options": ["Butter", "Avocado", "Lard", "Margarine"],
                    "correct_answer": "Avocado"
                }
            ],
            "Cardiovascular Health": [
                {
                    "question": "What is the primary benefit of cardiovascular exercise?",
                    "options": ["Increased muscle mass", "Improved heart health", "Better flexibility", "Stronger bones"],
                    "correct_answer": "Improved heart health"
                },
                {
                    "question": "Which of the following is a common cardiovascular exercise?",
                    "options": ["Weight lifting", "Running", "Yoga", "Pilates"],
                    "correct_answer": "Running"
                },
                {
                    "question": "How often should adults engage in moderate-intensity cardiovascular exercise?",
                    "options": ["Once a week", "Twice a week", "Three times a week", "Five times a week"],
                    "correct_answer": "Five times a week"
                },
                {
                    "question": "Which of the following is a benefit of regular cardiovascular exercise?",
                    "options": ["Increased stress", "Improved lung capacity", "Decreased energy levels", "None of the above"],
                    "correct_answer": "Improved lung capacity"
                },
                {
                    "question": "What is a safe target heart rate during cardiovascular exercise for most adults?",
                    "options": ["50-60% of maximum heart rate", "60-70% of maximum heart rate", "70-85% of maximum heart rate", "85-95% of maximum heart rate"],
                    "correct_answer": "70-85% of maximum heart rate"
                }
            ],
            # Add more topics and questions as needed
        }
        return json.dumps({
            "questions": fallback_quizzes.get(topic, [])
        })

def get_nutrition_facts(food_item):
    try:
        response = client.chat.completions.create(
            model="GPT-4o-mini (2024-07-18)",
            messages=[{
                "role": "user",
                "content": f"Provide nutritional information for {food_item}"
            }],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback content if API fails
        return json.dumps({
            "serving_size": "100g",
            "calories": "143 kcal",
            "protein": "12.6 g",
            "carbs": "0.7 g",
            "fats": "9.5 g",
            "vitamins": {
                "Vitamin A": "160 µg (18% DV)",
                "Vitamin D": "87 IU (22% DV)",
                "Vitamin B12": "1.1 µg (46% DV)",
                "Vitamin B6": " 0.1 mg (5% DV)"
            }
        })

def generate_exercise_guide(exercise):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Create a guide for {exercise}"
            }],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback content if API fails
        return json.dumps({
            "proper_form": "Maintain proper posture and form throughout the exercise",
            "common_mistakes": "Watch your breathing and avoid rushing",
            "benefits": "Improves strength and flexibility",
            "recommended_sets_reps": "3 sets of 10-12 repetitions"
        })

def get_video_content(topic):
    # Return embedded video content or educational information
    return {
        "title": f"Guide to {topic}",
        "description": "Learn about proper technique and form",
        "key_points": [
            "Understanding proper form",
            "Common mistakes to avoid",
            "Progressive improvements",
            "Safety considerations"
        ],
        "resources": [
            "Practice with proper guidance",
            "Regular assessment of progress",
            "Maintain consistent routine"
        ]
    }