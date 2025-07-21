# AI Bot API

A WhatsApp bot API that integrates with OpenAI and Supabase for intelligent conversation handling.

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- WhatsApp Business API credentials
- Supabase project

### Installation

1. Clone the repository:

```bash
git clone https://github.com/lukasjoho/ai-bot-api.git
cd ai-bot-api
```

2. Install dependencies using uv:

```bash
uv sync
```

3. Set up environment variables:

```bash
cp .env.example .env
```

4. Edit `.env` file with your actual credentials:

```bash
# WhatsApp
WHATSAPP_ACCESS_TOKEN=your_actual_whatsapp_access_token
WHATSAPP_PHONE_NUMBER_ID=your_actual_phone_number_id
WHATSAPP_API_VERSION=v22.0
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_RECIPIENT_DEMO_WAID=your_demo_waid

# OpenAI
OPENAI_API_KEY=your_actual_openai_api_key
OPENAI_ASSISTANT_ID=your_actual_assistant_id

# Supabase
SUPABASE_URL=your_actual_supabase_url
SUPABASE_API_KEY=your_actual_supabase_api_key
```

### Running the Application

```bash
uv run python main.py
```

## Features

- WhatsApp message handling and verification
- OpenAI Assistant integration for intelligent responses
- Supabase database for conversation persistence
- Async/await architecture for better performance

## Security

- Environment variables are properly ignored by git
- API keys and sensitive data are kept secure
- WhatsApp webhook verification implemented

## Project Structure

```
ai-bot-api/
├── main.py                 # FastAPI application entry point
├── routers/               # API route handlers
│   └── whatsapp.py       # WhatsApp webhook routes
├── services/             # Business logic services
│   ├── openai/          # OpenAI integration
│   ├── supabase/        # Database operations
│   └── whatsapp/        # WhatsApp API utilities
└── pyproject.toml       # Project configuration and dependencies
```
