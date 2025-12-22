# NLP Query Processing

## Overview

The College Recommendation System now includes **Natural Language Processing (NLP)** capabilities that allow users to interact with the system using everyday language instead of structured queries.

## Features

### 1. Intent Classification
The system can understand 5 main types of user intent:
- **search** - Find colleges based on criteria
- **compare** - Compare multiple colleges side-by-side
- **recommend** - Get personalized recommendations
- **info** - Get detailed information about specific colleges
- **greeting** - Conversational responses

### 2. Entity Extraction
The system extracts the following entities from natural language:
- **College Names**: IIT, NIT, IIIT, BITS, VIT, etc.
- **Cities**: Bangalore, Mumbai, Delhi, Chennai, Hyderabad, etc.
- **States**: Karnataka, Maharashtra, Tamil Nadu, Delhi, etc.
- **Courses**: CS, ECE, Mechanical, Civil, Chemical, Aerospace, etc.
- **Budget**: Amounts in lakhs or rupees (e.g., "2 lakhs", "under 3L")
- **Tier**: Tier 1, Tier 2, Budget-Friendly, Affordable, etc.
- **NIRF Rank**: Top X rankings (e.g., "top 50", "within top 100")
- **Facilities**: Hostel, library, gym, sports, cafeteria, medical, etc.
- **Ownership**: Government, Private

### 3. Query Understanding
Converts natural language queries into structured API parameters that can be used with existing endpoints.

## API Endpoints

### POST /api/nlp/query
Process a natural language query and get structured parameters.

**Request:**
```json
{
  "query": "Find CS colleges in Karnataka under 2 lakhs"
}
```

**Response:**
```json
{
  "query": "Find CS colleges in Karnataka under 2 lakhs",
  "intent": "search",
  "sub_intent": "search_cs",
  "entities": {
    "colleges": [],
    "courses": ["Computer Science"],
    "cities": [],
    "states": ["Karnataka"],
    "budget": 200000.0,
    "tier": null,
    "nirf_rank": null,
    "facilities": [],
    "ownership": null
  },
  "api_params": {
    "state": "Karnataka",
    "course_category": "Computer Science",
    "max_fee": 200000
  },
  "suggested_endpoint": "/api/colleges/search",
  "confidence": 0.8,
  "friendly_message": "Searching for colleges in Karnataka for Computer Science under ₹2.0 lakhs..."
}
```

### GET /api/nlp/examples
Get example queries demonstrating NLP capabilities.

**Response:**
```json
{
  "examples": [
    {
      "query": "Find CS colleges in Karnataka under 2 lakhs",
      "intent": "search",
      "description": "Search for colleges with filters"
    },
    ...
  ],
  "supported_intents": [...],
  "supported_entities": [...]
}
```

### GET /api/nlp/health
Check NLP service health status.

**Response:**
```json
{
  "status": "healthy",
  "message": "NLP services are operational",
  "components": {
    "intent_classifier": "operational",
    "entity_extractor": "operational",
    "query_processor": "operational"
  }
}
```

## Example Queries

### Search Queries
```
"Find CS colleges in Karnataka"
"Show me engineering colleges in Mumbai under 2 lakhs"
"What are the best colleges for mechanical engineering?"
"Government colleges in Tamil Nadu with hostel"
"Top 50 NIRF ranked colleges for ECE"
```

### Comparison Queries
```
"Compare IIT Bombay and IIT Delhi"
"Compare top 3 colleges in Bangalore for CS"
"Which is better: NIT Trichy or VIT Vellore?"
```

### Recommendation Queries
```
"Recommend me top engineering colleges"
"Suggest affordable ECE colleges in Tamil Nadu"
"I want recommendations for CS under 3 lakhs"
"Recommend tier 1 colleges with good placement"
```

### Information Queries
```
"Tell me about NIT Trichy fees and placements"
"What facilities does IIT Bombay have?"
"Give me details about BITS Pilani"
```

## Budget Formats Supported

The system understands various budget formats:
- `2 lakhs`, `2 lakh`, `2L` → ₹200,000
- `3.5 lakhs` → ₹350,000
- `Rs 200000`, `INR 200000` → ₹200,000
- `under 2 lakhs`, `below 3L` → max budget
- `within 5 lakhs` → max budget

## Course Mappings

The system maps various course names to standard categories:
- **CS, CSE, IT, Computer Science** → Computer Science
- **ECE, Electronics, EEE, Electrical** → Electronics and Communication
- **Mech, Mechanical** → Mechanical Engineering
- **Civil** → Civil Engineering
- **Chemical, Chem** → Chemical Engineering
- **Aerospace, Aero, Aeronautical** → Aerospace
- **Biotech, Bio** → Biotechnology
- **AI, ML, Data Science** → AI/ML (searches CS category)

## Tier Keywords

The system recognizes tier-related keywords:
- **Tier 1, Tier-1, tier1** → Tier 1
- **Tier 2, Tier-2, tier2** → Tier 2
- **Budget-friendly, affordable** → Budget-Friendly/Affordable
- **Moderate** → Moderate tier

## NIRF Rank Patterns

The system understands NIRF rank filters:
- `top 10` → ranks 1-10
- `within top 50` → ranks 1-50
- `in top 100` → ranks 1-100
- `rank between 10 and 50` → ranks 10-50

## Facility Keywords

The system recognizes facility-related terms:
- **hostel, accommodation, residence** → hostel filter
- **library, books** → library filter
- **gym, gymnasium, fitness** → gym filter
- **sports, playground, stadium** → sports complex filter
- **cafeteria, canteen, mess** → cafeteria filter
- **medical, hospital, clinic** → medical facilities filter
- **wifi, internet** → wifi filter
- **transport, bus, shuttle** → transport filter

## Integration Workflow

### Typical NLP-to-API Flow

1. **User submits natural language query**
   ```
   "Find affordable CS colleges in Bangalore with hostel"
   ```

2. **NLP processes query**
   ```json
   {
     "intent": "search",
     "entities": {
       "courses": ["Computer Science"],
       "cities": ["Bangalore"],
       "tier": "Affordable",
       "facilities": ["hostel"]
     },
     "api_params": {
       "city": "Bangalore",
       "course_category": "Computer Science",
       "tier": "Affordable",
       "has_hostel": true
     },
     "suggested_endpoint": "/api/colleges/search"
   }
   ```

3. **Frontend uses API params to call search endpoint**
   ```
   GET /api/colleges/search?city=Bangalore&course_category=Computer%20Science&tier=Affordable&has_hostel=true
   ```

4. **Display results to user**

## Architecture

### Components

1. **IntentClassifier** (`backend/app/nlp/intent_classifier.py`)
   - Pattern-based intent recognition using regex
   - Confidence scoring
   - Sub-intent classification

2. **EntityExtractor** (`backend/app/nlp/entity_extractor.py`)
   - Extracts structured information from text
   - Uses spaCy NER for organization names
   - Custom pattern matching for domain-specific entities

3. **QueryProcessor** (`backend/app/nlp/query_processor.py`)
   - Combines intent and entities
   - Converts to API parameters
   - Determines appropriate endpoint
   - Generates friendly user messages

### Technologies Used

- **spaCy 3.8.11** - NLP and Named Entity Recognition
- **scikit-learn 1.8.0** - Machine learning capabilities
- **NLTK 3.8.1** - Natural language toolkit
- **FastAPI** - API framework
- **Pydantic** - Data validation

## Testing

Run NLP tests:
```bash
cd backend
python test_nlp_api.py
```

### Test Coverage
- ✅ Intent classification
- ✅ Entity extraction (colleges, cities, states, courses, budget)
- ✅ Budget parsing (lakhs, rupees, "under X")
- ✅ Tier recognition
- ✅ NIRF rank filtering
- ✅ Facility filtering
- ✅ Ownership filtering
- ✅ Complex multi-filter queries
- ✅ Greeting responses
- ✅ API parameter generation

## Performance

- **Average response time**: < 100ms
- **Confidence threshold**: 0.3 (queries below this get clarification request)
- **Supported languages**: English
- **Pattern matching**: Regex-based (fast, no training required)

## Future Enhancements

### Planned Features
1. **Machine Learning Model**: Train on real user queries for better accuracy
2. **Multi-language Support**: Hindi, Tamil, Telugu, etc.
3. **Context Awareness**: Remember previous queries in conversation
4. **Fuzzy Matching**: Better handling of typos and variations
5. **Voice Input**: Speech-to-text integration
6. **Sentiment Analysis**: Understand user preferences from tone
7. **Query Expansion**: Suggest related searches
8. **Learning from Feedback**: Improve based on user corrections

### Current Limitations
- Pattern-based (may miss complex or unusual phrasings)
- English only
- No conversation memory between queries
- Limited to predefined intent and entity types
- Requires exact college name matching for comparisons

## Error Handling

The system handles various error cases:

1. **Low Confidence** (< 0.3):
   ```json
   {
     "friendly_message": "I'm not quite sure what you're looking for. Could you rephrase your question?"
   }
   ```

2. **Insufficient Information for Comparison**:
   ```json
   {
     "friendly_message": "I need at least 2 college names to compare. Which colleges would you like to compare?"
   }
   ```

3. **Service Errors**:
   ```json
   {
     "status_code": 500,
     "detail": "Error processing query: [error message]"
   }
   ```

## Best Practices

### For Frontend Integration

1. **Check Confidence Score**: Display clarification prompts for low confidence
2. **Use Suggested Endpoint**: Follow the `suggested_endpoint` recommendation
3. **Show Friendly Message**: Display `friendly_message` to user
4. **Handle Missing Entities**: If critical entities are missing, prompt user
5. **Progressive Disclosure**: Show extracted entities for user verification
6. **Fallback Options**: Provide manual search if NLP fails

### For Query Formulation

**Good Queries:**
- "Find CS colleges in Karnataka under 2 lakhs"
- "Compare IIT Bombay and IIT Delhi"
- "Top 50 NIRF colleges with hostel"

**Less Optimal:**
- "i want collge" (typos, vague)
- "best one" (no context)
- "what about that" (no reference)

## API Documentation

Full interactive documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Support

For issues or questions:
1. Check examples at `/api/nlp/examples`
2. Verify service health at `/api/nlp/health`
3. Review this documentation
4. Check server logs for errors
