# Conversational AI Backend

A FastAPI-based backend service for a conversational AI system with e-commerce integration.

## Features

- 🤖 AI-powered chat using Groq API
- 🛍️ E-commerce database integration (products, customers, orders)
- 💬 Multi-user conversation sessions
- 📊 PostgreSQL database with SQLAlchemy ORM
- 🚀 FastAPI with automatic API documentation

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration and models
├── models.py            # SQLAlchemy models for chat system
├── schemas.py           # Pydantic schemas for API
├── load_data.py         # Data loading script
├── setup.py             # Project setup script
├── routes/
│   └── chat.py          # Chat API endpoints
├── services/
│   └── llm.py           # LLM integration service
└── requirements.txt     # Python dependencies
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/conversational-ai-backend.git
cd conversational-ai-backend
```

### 2. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/conversational_ai
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Database Setup

Make sure PostgreSQL is running, then:

```bash
cd backend
python setup.py
```

### 5. Run the Application

```bash
python main.py
```

The API will be available at:
- Main API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Chat API

**POST /api/chat**

Send a message to the AI assistant.

```json
{
  "user_id": "1",
  "message": "What products do you have?",
  "conversation_id": "optional"
}
```

### User Management

**POST /api/users** - Create a new user
**GET /api/users/{user_id}** - Get user details

## Database Schema

### Chat System Tables
- `users` - User accounts
- `conversation_sessions` - Chat sessions
- `messages` - Individual messages

### E-commerce Tables
- `products` - Product catalog
- `customers` - Customer information
- `orders` - Order records

## Technologies Used

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **Groq API** - LLM integration
- **Pydantic** - Data validation
- **Pandas** - Data processing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.