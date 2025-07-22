# Gregor

An intelligent WhatsApp bot that integrates with OpenAI and Upstash for smart conversation handling and data persistence.

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- WhatsApp Business API credentials
- Upstash Redis database
- Upstash Vector database (optional)
- Upstash QStash (optional)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/lukasjoho/gregor.git
cd gregor
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

# Upstash
UPSTASH_REDIS_URL=your_upstash_redis_url
UPSTASH_REDIS_TOKEN=your_upstash_redis_token
UPSTASH_VECTOR_URL=your_upstash_vector_url
```

### Running the Application

1. Start the development server:

```bash
uv run uvicorn main:app --reload
```

2. In another terminal, expose your local server using ngrok:

```bash
ngrok http localhost:8000
```

## Features

- WhatsApp message handling and verification
- OpenAI Assistant integration with specialized agents
- Upstash Redis for session management and caching
- Multi-agent architecture for knowledge and communication
- Async/await architecture for better performance

## Security

- Environment variables are properly ignored by git
- API keys and sensitive data are kept secure
- WhatsApp webhook verification implemented

## Project Structure

```
gregor/
├── main.py                    # FastAPI application entry point
├── config/                    # Configuration files
│   ├── config.py             # App configuration
│   ├── communication_prompt.txt
│   └── knowledge_prompt.txt
├── routers/                   # API route handlers
│   └── whatsapp.py           # WhatsApp webhook routes
├── services/                  # Business logic services
│   ├── openai/               # OpenAI integration
│   │   ├── agents/           # Specialized AI agents
│   │   │   ├── communication_agent.py
│   │   │   └── knowledge_agent.py
│   │   ├── tools/            # Agent tools
│   │   └── run.py            # Agent runner
│   ├── database/             # Local data storage
│   │   ├── data/             # JSON data files
│   │   └── database.py       # Database utilities
│   ├── redis/                # Upstash Redis integration
│   │   ├── client.py         # Redis client
│   │   ├── session.py        # Session management
│   │   └── utils.py          # Redis utilities
│   └── whatsapp/             # WhatsApp API utilities
│       ├── api.py            # WhatsApp API client
│       ├── handler.py        # Message handlers
│       ├── messages.py       # Message utilities
│       └── verify.py         # Webhook verification
├── pyproject.toml            # Project configuration
└── uv.lock                   # Dependency lock file
```
