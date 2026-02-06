"""
Intent Classification Module
Classifies user queries into: search, compare, recommend, info, greeting
"""
import re
from typing import Tuple


class IntentClassifier:
    """Classify user intent from natural language queries."""
    
    def __init__(self):
        # Intent patterns with keywords
        self.patterns = {
            'search': [
                r'\b(find|show|list|search|get|give|display)\b.*\b(college|university|institution)\b',
                r'\b(college|university|institution).*\b(in|at|near|around)\b',
                r'\b(what|which).*\b(college|university|institution)\b',
                r'\b(engineering college|technical university)\b',
                r'\b(show|find|list|get).*\b(top|best|ranked|nirf)\b',
                r'\b(government|private).*\b(college|engineering)\b',
                r'\b(top|best).*\b(\d+|fifty|hundred).*\b(college)\b',
            ],
            'compare': [
                r'\b(compare|difference|versus|vs|better)\b',
                r'\b(which is better|which one)\b',
                r'\b(compare|comparison)\b.*\b(between|with)\b',
                r'\b(iit|nit).*\b(or|and|vs)\b.*\b(iit|nit)\b',
            ],
            'recommend': [
                r'\b(recommend|suggest|advise)\b',
                r'\b(should i|which should)\b',
                r'\b(good|suitable|right).*\b(for me|based on)\b',
                r'\b(within|under|below|budget).*\b(lakh|rupee|rs|inr)\b',
            ],
            'info': [
                r'\btell me about\b.*\b(specific college|iit|nit|bits|vit)\b',
                r'\bwhat is\b.*\b(fees|placement|cutoff)\b',
                r'\b(fees|fee structure|cost|placement|cutoff|admission)\b(?!.*\b(find|show|list|search)\b)',
            ],
            'greeting': [
                r'\b(hi|hello|hey|greetings|good morning|good afternoon)\b',
                r'^(hi|hello|hey)[\s!?]*$',
            ]
        }
        
        # Confidence boosters
        self.strong_keywords = {
            'search': ['find', 'show', 'list', 'search'],
            'compare': ['compare', 'versus', 'vs', 'difference', 'better'],
            'recommend': ['recommend', 'suggest', 'best', 'should'],
            'info': ['tell me about', 'what is', 'explain', 'details'],
            'greeting': ['hello', 'hi', 'hey']
        }
    
    def classify(self, query: str) -> Tuple[str, float]:
        """
        Classify user query into intent category.
        
        Args:
            query: User's natural language query
            
        Returns:
            Tuple of (intent, confidence)
            intent: One of 'search', 'compare', 'recommend', 'info', 'greeting', 'unknown'
            confidence: Float between 0 and 1
        """
        query_lower = query.lower().strip()
        
        if not query_lower:
            return ('unknown', 0.0)
        
        # Check each intent pattern
        intent_scores = {}
        
        for intent, patterns in self.patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    matches += 1
                    score += 0.5
            
            # Boost score for strong keywords
            if intent in self.strong_keywords:
                for keyword in self.strong_keywords[intent]:
                    if keyword in query_lower:
                        score += 0.3
            
            if matches > 0:
                intent_scores[intent] = min(score, 1.0)
        
        if not intent_scores:
            return ('unknown', 0.0)
        
        # Get intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        # Adjust for ambiguous cases
        if len(intent_scores) > 1:
            sorted_scores = sorted(intent_scores.values(), reverse=True)
            if sorted_scores[0] - sorted_scores[1] < 0.2:
                confidence *= 0.8  # Lower confidence for ambiguous cases
        
        return (best_intent, confidence)
    
    def get_sub_intent(self, query: str, main_intent: str) -> str:
        """
        Get sub-intent for more specific classification.
        
        Args:
            query: User's query
            main_intent: Main intent classification
            
        Returns:
            Sub-intent string
        """
        query_lower = query.lower()
        
        if main_intent == 'search':
            if re.search(r'\b(cs|computer science|it|information technology)\b', query_lower):
                return 'search_cs'
            elif re.search(r'\b(tier 1|top|best|ranked)\b', query_lower):
                return 'search_top'
            elif re.search(r'\b(cheap|affordable|budget|economical)\b', query_lower):
                return 'search_affordable'
            elif re.search(r'\b(hostel|accommodation|residence)\b', query_lower):
                return 'search_hostel'
            else:
                return 'search_general'
        
        elif main_intent == 'recommend':
            if re.search(r'\b(budget|money|cost|afford)\b', query_lower):
                return 'recommend_budget'
            elif re.search(r'\b(course|branch|stream)\b', query_lower):
                return 'recommend_course'
            elif re.search(r'\b(location|city|state|place)\b', query_lower):
                return 'recommend_location'
            else:
                return 'recommend_general'
        
        elif main_intent == 'info':
            if re.search(r'\b(fees|fee|cost)\b', query_lower):
                return 'info_fees'
            elif re.search(r'\b(placement|job|recruit|package)\b', query_lower):
                return 'info_placement'
            elif re.search(r'\b(cutoff|admission|eligibility)\b', query_lower):
                return 'info_admission'
            elif re.search(r'\b(facilities|infrastructure|amenities)\b', query_lower):
                return 'info_facilities'
            else:
                return 'info_general'
        
        return main_intent
