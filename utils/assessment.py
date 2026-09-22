import pandas as pd
import numpy as np
from datetime import datetime

class AssessmentEngine:
    def __init__(self):
        self.learning_data = {}
    
    def assess_understanding(self, question, student_answer, correct_answer):
        """Assess student understanding of a concept"""
        is_correct = str(student_answer).strip().lower() == str(correct_answer).strip().lower()
        
        feedback = self.generate_feedback(is_correct, question, student_answer)
        
        return {
            'correct': is_correct,
            'feedback': feedback,
            'timestamp': datetime.now()
        }
    
    def generate_feedback(self, is_correct, question, student_answer):
        if is_correct:
            return self.get_positive_feedback()
        else:
            return self.get_constructive_feedback(question, student_answer)
    
    def get_positive_feedback(self):
        positive_messages = [
            "Excellent work! You've mastered this concept! 🎉",
            "Great job! Your understanding is solid. 🌟",
            "Perfect! You're making excellent progress. 💪"
        ]
        return np.random.choice(positive_messages)
    
    def get_constructive_feedback(self, question, student_answer):
        guidance_templates = [
            "Let's try a different approach. Remember: {hint}",
            "Good attempt! Here's a hint: {hint}"
        ]
        
        hint = self.generate_hint(question)
        template = np.random.choice(guidance_templates)
        return template.format(hint=hint)
    
    def generate_hint(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['add', 'sum', 'plus']):
            return "Try breaking the numbers into tens and ones, then add them separately."
        else:
            return "Take your time and review the main concepts."