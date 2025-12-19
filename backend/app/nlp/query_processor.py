"""
Query Processor Module
Converts natural language queries into API parameters
"""
from typing import Dict, Any, Optional
from .intent_classifier import IntentClassifier
from .entity_extractor import EntityExtractor


class QueryProcessor:
    """Convert natural language queries to API parameters."""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query into structured API parameters.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with:
            - intent: Main intent (search, compare, recommend, info)
            - sub_intent: Specific sub-intent
            - entities: Extracted entities
            - api_params: Parameters for API call
            - suggested_endpoint: Which API endpoint to call
            - confidence: Overall confidence score
        """
        # Classify intent
        intent, confidence = self.intent_classifier.classify(query)
        sub_intent = self.intent_classifier.get_sub_intent(query, intent)
        
        # Extract entities
        entities = self.entity_extractor.extract(query)
        
        # Convert to API parameters based on intent
        api_params = self._convert_to_api_params(intent, sub_intent, entities)
        
        # Determine suggested endpoint
        suggested_endpoint = self._get_suggested_endpoint(intent, api_params)
        
        return {
            'intent': intent,
            'sub_intent': sub_intent,
            'entities': entities,
            'api_params': api_params,
            'suggested_endpoint': suggested_endpoint,
            'confidence': confidence
        }
    
    def _convert_to_api_params(self, intent: str, sub_intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Convert entities to API parameters based on intent."""
        
        if intent == 'search':
            return self._build_search_params(entities)
        
        elif intent == 'compare':
            return self._build_compare_params(entities)
        
        elif intent == 'recommend':
            return self._build_recommend_params(entities, sub_intent)
        
        elif intent == 'info':
            return self._build_info_params(entities, sub_intent)
        
        return {}
    
    def _build_search_params(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters for /api/colleges/search endpoint."""
        params = {}
        
        # Add search query (college name if provided)
        if entities['colleges']:
            params['q'] = entities['colleges'][0]  # Use first college name
        
        # Add location filters
        if entities['states']:
            params['state'] = entities['states'][0]
        if entities['cities']:
            params['city'] = entities['cities'][0]
        
        # Add course filter
        if entities['courses']:
            # Map to course category
            course = entities['courses'][0]
            if course in ['Computer Science', 'AI/ML']:
                params['course_category'] = 'Computer Science'
            elif course == 'Electronics':
                params['course_category'] = 'Electronics and Communication'
            elif course == 'Mechanical':
                params['course_category'] = 'Mechanical Engineering'
            elif course == 'Civil':
                params['course_category'] = 'Civil Engineering'
            elif course == 'Chemical':
                params['course_category'] = 'Chemical Engineering'
        
        # Add budget filter
        if entities['budget']:
            params['max_fee'] = int(entities['budget'])
        
        # Add tier filter
        if entities['tier']:
            params['tier'] = entities['tier']
        
        # Add NIRF rank filter
        if entities['nirf_rank']:
            params['nirf_rank_max'] = entities['nirf_rank']['max']
        
        # Add ownership filter
        if entities['ownership']:
            params['ownership'] = entities['ownership']
        
        # Add facility filters
        for facility in entities['facilities']:
            if facility == 'hostel':
                params['has_hostel'] = True
            elif facility == 'library':
                params['has_library'] = True
            elif facility == 'gym':
                params['has_gym'] = True
            elif facility == 'sports':
                params['has_sports_complex'] = True
            elif facility == 'cafeteria':
                params['has_cafeteria'] = True
            elif facility == 'medical':
                params['has_medical_facilities'] = True
        
        return params
    
    def _build_compare_params(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters for /api/colleges/compare endpoint."""
        params = {}
        
        # Get college names for comparison
        if entities['colleges'] and len(entities['colleges']) >= 2:
            params['college_names'] = entities['colleges'][:4]  # Max 4 colleges
        
        return params
    
    def _build_recommend_params(self, entities: Dict[str, Any], sub_intent: str) -> Dict[str, Any]:
        """Build parameters for /api/colleges/recommendations endpoint."""
        params = {}
        
        # Location preferences
        if entities['states']:
            params['preferred_state'] = entities['states'][0]
        if entities['cities']:
            params['preferred_city'] = entities['cities'][0]
        
        # Course preferences
        if entities['courses']:
            course = entities['courses'][0]
            if course in ['Computer Science', 'AI/ML']:
                params['course_category'] = 'Computer Science'
            elif course == 'Electronics':
                params['course_category'] = 'Electronics and Communication'
            elif course == 'Mechanical':
                params['course_category'] = 'Mechanical Engineering'
        
        # Budget preferences
        if entities['budget']:
            params['max_fee'] = int(entities['budget'])
        
        # Tier preferences
        if entities['tier']:
            params['tier'] = entities['tier']
        
        # NIRF rank preferences
        if entities['nirf_rank']:
            params['nirf_rank_max'] = entities['nirf_rank']['max']
        
        # Ownership preference
        if entities['ownership']:
            params['ownership'] = entities['ownership']
        
        # Sub-intent specific parameters
        if sub_intent == 'recommend_budget':
            if not entities['budget']:
                # Default budget if not specified
                params['max_fee'] = 200000  # 2 lakhs
        
        elif sub_intent == 'recommend_top':
            if not entities['nirf_rank']:
                params['nirf_rank_max'] = 50  # Top 50
        
        return params
    
    def _build_info_params(self, entities: Dict[str, Any], sub_intent: str) -> Dict[str, Any]:
        """Build parameters for college details endpoint."""
        params = {}
        
        # Get college name for info lookup
        if entities['colleges']:
            params['college_name'] = entities['colleges'][0]
        
        # Specify what info is needed
        params['info_type'] = sub_intent.replace('info_', '') if sub_intent.startswith('info_') else 'general'
        
        return params
    
    def _get_suggested_endpoint(self, intent: str, api_params: Dict[str, Any]) -> str:
        """Determine which API endpoint to call based on intent."""
        
        if intent == 'search':
            return '/api/colleges/search'
        
        elif intent == 'compare':
            if 'college_names' in api_params and len(api_params.get('college_names', [])) >= 2:
                return '/api/colleges/compare'
            else:
                return '/api/colleges/search'  # Need to search first
        
        elif intent == 'recommend':
            return '/api/colleges/recommendations'
        
        elif intent == 'info':
            if 'college_name' in api_params:
                return '/api/colleges/{id}'  # Need to resolve ID first
            else:
                return '/api/colleges/search'
        
        elif intent == 'greeting':
            return None  # No API call needed
        
        return '/api/colleges/search'  # Default
    
    def get_friendly_response(self, result: Dict[str, Any]) -> str:
        """Generate a friendly response template based on processing result."""
        
        intent = result['intent']
        confidence = result['confidence']
        
        if confidence < 0.3:
            return "I'm not quite sure what you're looking for. Could you rephrase your question?"
        
        if intent == 'greeting':
            return "Hello! I can help you find engineering colleges, compare options, or get recommendations. What would you like to know?"
        
        elif intent == 'search':
            filters = []
            if result['entities']['states']:
                filters.append(f"in {result['entities']['states'][0]}")
            if result['entities']['courses']:
                filters.append(f"for {result['entities']['courses'][0]}")
            if result['entities']['budget']:
                budget_lakhs = result['entities']['budget'] / 100000
                filters.append(f"under ₹{budget_lakhs:.1f} lakhs")
            
            filter_text = ' '.join(filters) if filters else ''
            return f"Searching for colleges {filter_text}..."
        
        elif intent == 'compare':
            colleges = result['entities']['colleges']
            if len(colleges) >= 2:
                return f"Comparing {', '.join(colleges[:4])}..."
            else:
                return "I need at least 2 college names to compare. Which colleges would you like to compare?"
        
        elif intent == 'recommend':
            preferences = []
            if result['entities']['courses']:
                preferences.append(result['entities']['courses'][0])
            if result['entities']['states']:
                preferences.append(result['entities']['states'][0])
            if result['entities']['budget']:
                budget_lakhs = result['entities']['budget'] / 100000
                preferences.append(f"₹{budget_lakhs:.1f}L budget")
            
            pref_text = ', '.join(preferences) if preferences else 'your preferences'
            return f"Finding personalized recommendations based on {pref_text}..."
        
        elif intent == 'info':
            college = result['entities']['colleges'][0] if result['entities']['colleges'] else 'the college'
            return f"Getting detailed information about {college}..."
        
        return "Processing your request..."
