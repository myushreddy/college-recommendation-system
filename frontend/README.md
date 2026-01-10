# College Recommendation Chatbot - Frontend

A Next.js chatbot interface for the College Recommendation System.

## Features

- 💬 **Chat Interface** - Natural language conversation
- 🤖 **NLP Integration** - Powered by FastAPI backend
- 🎓 **College Cards** - Rich college information display
- ⚡ **Quick Actions** - Popular search shortcuts
- 📱 **Responsive Design** - Works on all devices

## Tech Stack

- **Framework:** Next.js 14
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **API Client:** Axios
- **Backend:** FastAPI (http://localhost:8000)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page (chat)
│   │   └── globals.css     # Global styles
│   ├── components/
│   │   ├── ChatInterface.tsx    # Main chat component
│   │   ├── MessageBubble.tsx    # Message display
│   │   ├── CollegeCard.tsx      # College card
│   │   └── QuickActions.tsx     # Quick action buttons
│   ├── services/
│   │   └── api.ts          # API service layer
│   └── types/
│       └── index.ts        # TypeScript types
├── public/                 # Static assets
└── package.json
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Example Queries

Try these in the chat:

- "Find CS colleges in Karnataka"
- "Show me top NIRF ranked colleges"
- "Recommend affordable colleges under 2 lakhs"
- "Compare IIT Bombay and IIT Delhi"
- "Government colleges in Tamil Nadu"

## API Integration

The frontend connects to the backend API:

- **NLP Query:** `POST /api/nlp/query`
- **Search Colleges:** `GET /api/colleges/search`
- **College Details:** `GET /api/colleges/{id}`
- **Compare:** `POST /api/colleges/compare`
- **Recommendations:** `POST /api/colleges/recommendations`

## Components

### ChatInterface
Main chat container with message handling and API integration.

### MessageBubble
Displays user and bot messages with timestamps.

### CollegeCard
Rich card displaying college information with badges and facilities.

### QuickActions
Horizontal scrollable buttons for popular searches.

## Styling

Uses Tailwind CSS with custom components:
- `.message-bubble` - Chat message styling
- `.message-user` - User message
- `.message-bot` - Bot message
- `.college-card` - College card
- `.quick-action-btn` - Quick action button

## Development

Make sure the backend API is running:

```bash
cd backend
python main.py
```

Then start the frontend:

```bash
cd frontend
npm run dev
```

## Build for Production

```bash
npm run build
npm start
```

## Troubleshooting

**Issue:** API connection error  
**Solution:** Ensure backend is running on http://localhost:8000

**Issue:** Module not found  
**Solution:** Run `npm install`

**Issue:** Port 3000 in use  
**Solution:** Change port with `PORT=3001 npm run dev`

## Future Enhancements

- [ ] College comparison page
- [ ] Detailed college profile pages
- [ ] Favorites/bookmarks
- [ ] Filter panel
- [ ] Search history
- [ ] Dark mode
- [ ] Voice input

## License

Part of the College Recommendation System project.
