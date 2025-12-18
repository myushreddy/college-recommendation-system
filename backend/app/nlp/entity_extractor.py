"""
Entity Extraction Module
Extracts entities like college names, cities, courses, budget, tier from queries
"""
import re
import spacy
from typing import Dict, List, Optional, Any


class EntityExtractor:
    """Extract entities from natural language queries."""
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not loaded. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Common college name patterns
        self.college_patterns = [
            r'\b(IIT|Indian Institute of Technology)\s+\w+',
            r'\b(NIT|National Institute of Technology)\s+\w+',
            r'\b(IIIT|International Institute of Information Technology)\s+\w+',
            r'\b(IIM|Indian Institute of Management)\s+\w+',
            r'\b(BITS|Birla Institute of Technology and Science)\s*\w*',
            r'\b(VIT|Vellore Institute of Technology)',
            r'\b(SRM|SRM Institute of Science and Technology)',
            r'\b(Manipal Institute of Technology)',
            r'\b(PSG|PSG College of Technology)',
            r'\b(COEP|College of Engineering Pune)',
        ]
        
        # Course/branch keywords
        self.course_keywords = {
            'Computer Science': ['cs', 'computer science', 'cse', 'it', 'information technology', 'software'],
            'Electronics': ['ece', 'electronics', 'communication', 'electrical', 'eee'],
            'Mechanical': ['mechanical', 'mech', 'automobile', 'auto'],
            'Civil': ['civil', 'construction'],
            'Chemical': ['chemical', 'chem'],
            'Aerospace': ['aerospace', 'aeronautical', 'aero'],
            'Biotechnology': ['biotech', 'biotechnology', 'bio'],
            'AI/ML': ['ai', 'artificial intelligence', 'ml', 'machine learning', 'data science']
        }
        
        # Indian states
        self.states = [
            'Andhra Pradesh', 'Karnataka', 'Tamil Nadu', 'Kerala', 'Telangana', 
            'Maharashtra', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Delhi',
            'West Bengal', 'Punjab', 'Haryana', 'Madhya Pradesh', 'Bihar',
            'Odisha', 'Assam', 'Jharkhand', 'Chhattisgarh', 'Uttarakhand',
            'Himachal Pradesh', 'Goa', 'Tripura', 'Meghalaya', 'Manipur',
            'Nagaland', 'Mizoram', 'Arunachal Pradesh', 'Jammu and Kashmir', 'Sikkim'
        ]
        
        # Major cities
        self.cities = [
            'Bangalore', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 'Kolkata', 
            'Hyderabad', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur', 'Lucknow',
            'Kanpur', 'Nagpur', 'Indore', 'Bhopal', 'Visakhapatnam', 'Patna',
            'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
            'Meerut', 'Rajkot', 'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad',
            'Amritsar', 'Allahabad', 'Prayagraj', 'Ranchi', 'Gwalior', 'Chandigarh',
            'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur', 'Kota', 'Trichy'
        ]
    
    def extract(self, query: str) -> Dict[str, Any]:
        """
        Extract all entities from query.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with extracted entities
        """
        entities = {
            'colleges': [],
            'courses': [],
            'cities': [],
            'states': [],
            'budget': None,
            'tier': None,
            'nirf_rank': None,
            'facilities': [],
            'ownership': None
        }
        
        query_lower = query.lower()
        
        # Extract college names
        entities['colleges'] = self._extract_colleges(query)
        
        # Extract courses/branches
        entities['courses'] = self._extract_courses(query_lower)
        
        # Extract locations
        entities['cities'] = self._extract_cities(query)
        entities['states'] = self._extract_states(query)
        
        # Extract budget
        entities['budget'] = self._extract_budget(query_lower)
        
        # Extract tier
        entities['tier'] = self._extract_tier(query_lower)
        
        # Extract NIRF rank
        entities['nirf_rank'] = self._extract_nirf_rank(query_lower)
        
        # Extract facilities
        entities['facilities'] = self._extract_facilities(query_lower)
        
        # Extract ownership
        entities['ownership'] = self._extract_ownership(query_lower)
        
        return entities
    
    def _extract_colleges(self, query: str) -> List[str]:
        """Extract college names from query."""
        colleges = []
        
        for pattern in self.college_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            colleges.extend(matches)
        
        # Use spaCy NER if available
        if self.nlp:
            doc = self.nlp(query)
            for ent in doc.ents:
                if ent.label_ == 'ORG' and any(word in ent.text.lower() for word in ['institute', 'university', 'college']):
                    if ent.text not in colleges:
                        colleges.append(ent.text)
        
        return colleges
    
    def _extract_courses(self, query_lower: str) -> List[str]:
        """Extract course/branch names from query."""
        courses = []
        
        for course, keywords in self.course_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if course not in courses:
                        courses.append(course)
                    break
        
        return courses
    
    def _extract_cities(self, query: str) -> List[str]:
        """Extract city names from query."""
        cities = []
        query_lower = query.lower()
        
        for city in self.cities:
            if city.lower() in query_lower:
                cities.append(city)
        
        return cities
    
    def _extract_states(self, query: str) -> List[str]:
        """Extract state names from query."""
        states = []
        query_lower = query.lower()
        
        for state in self.states:
            if state.lower() in query_lower:
                states.append(state)
        
        return states
    
    def _extract_budget(self, query_lower: str) -> Optional[float]:
        """Extract budget amount from query."""
        # Pattern: X lakh, X lakhs, X lacs, X L
        lakh_pattern = r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lacs|lac|l)\b'
        match = re.search(lakh_pattern, query_lower)
        if match:
            amount = float(match.group(1))
            return amount * 100000  # Convert to rupees
        
        # Pattern: X rupees, Rs X, INR X
        rupee_pattern = r'(?:rs\.?|inr|rupees?)\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        match = re.search(rupee_pattern, query_lower)
        if match:
            amount_str = match.group(1).replace(',', '')
            return float(amount_str)
        
        # Pattern: under/below X
        under_pattern = r'(?:under|below|less than|within)\s*(\d+)'
        match = re.search(under_pattern, query_lower)
        if match:
            amount = float(match.group(1))
            # Assume lakhs if amount is small
            if amount < 100:
                return amount * 100000
            return amount
        
        return None
    
    def _extract_tier(self, query_lower: str) -> Optional[str]:
        """Extract tier information from query."""
        if 'tier 1' in query_lower or 'tier-1' in query_lower or 'tier1' in query_lower:
            return 'Tier 1'
        elif 'tier 2' in query_lower or 'tier-2' in query_lower or 'tier2' in query_lower:
            return 'Tier 2'
        elif 'tier 3' in query_lower or 'tier-3' in query_lower or 'tier3' in query_lower:
            return 'Tier 3'
        elif 'budget-friendly' in query_lower or 'budget friendly' in query_lower:
            return 'Budget-Friendly'
        elif 'affordable' in query_lower:
            return 'Affordable'
        elif 'moderate' in query_lower:
            return 'Moderate'
        return None
    
    def _extract_nirf_rank(self, query_lower: str) -> Optional[Dict[str, int]]:
        """Extract NIRF rank range from query."""
        # Pattern: top X, top-X, within top X
        top_pattern = r'(?:top|within top|in top)\s*(\d+)'
        match = re.search(top_pattern, query_lower)
        if match:
            rank = int(match.group(1))
            return {'min': 1, 'max': rank}
        
        # Pattern: rank between X and Y
        range_pattern = r'rank\s*between\s*(\d+)\s*and\s*(\d+)'
        match = re.search(range_pattern, query_lower)
        if match:
            return {'min': int(match.group(1)), 'max': int(match.group(2))}
        
        return None
    
    def _extract_facilities(self, query_lower: str) -> List[str]:
        """Extract required facilities from query."""
        facilities = []
        facility_keywords = {
            'hostel': ['hostel', 'accommodation', 'residence', 'boarding'],
            'library': ['library', 'books', 'reading room'],
            'gym': ['gym', 'gymnasium', 'fitness', 'workout'],
            'sports': ['sports', 'playground', 'stadium', 'games'],
            'lab': ['lab', 'laboratory', 'workshop'],
            'cafeteria': ['cafeteria', 'canteen', 'mess', 'dining'],
            'wifi': ['wifi', 'wi-fi', 'internet', 'connectivity'],
            'transport': ['transport', 'bus', 'shuttle'],
            'medical': ['medical', 'hospital', 'clinic', 'health center'],
            'auditorium': ['auditorium', 'hall', 'auditorium']
        }
        
        for facility, keywords in facility_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                facilities.append(facility)
        
        return facilities
    
    def _extract_ownership(self, query_lower: str) -> Optional[str]:
        """Extract college ownership type from query."""
        if any(word in query_lower for word in ['government', 'govt', 'public', 'state']):
            return 'Government'
        elif any(word in query_lower for word in ['private', 'pvt']):
            return 'Private'
        return None
