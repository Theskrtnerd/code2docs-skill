---
title: Environment Configuration
slug: environment-configuration
category:
  uri: Documentation
content:
  excerpt: Complete reference for all environment variables, API keys, and configuration options required for different features (OpenAI, Google Gemini, MongoDB, ReadMe integration).
---

# Environment Configuration

Complete reference for all environment variables, API keys, and configuration options required for different features in the ReadMe AI Service.

## Overview

The ReadMe AI Service requires various environment variables to function properly. These variables control API integrations, database connections, authentication, and feature-specific configurations. All environment variables are defined in `config/custom-environment-variables.json` with defaults in `config/default.json`.

**Important**: The application will crash immediately if required API keys are not set when importing AI modules. For testing server startup only, you can use dummy values.

## Quick Start

### Minimum Required Configuration

To start the server with basic functionality:

```bash
OPENAI_KEY=your_openai_key \
GOOGLE_GENERATIVE_AI_API_KEY=your_google_key \
npm start
```

### Testing Server Startup Only

To test if the server starts without real API access:

```bash
OPENAI_KEY=dummy \
GOOGLE_GENERATIVE_AI_API_KEY=dummy \
npm start
```

## Core Configuration

### Server Settings

#### PORT

- **Description**: Port number for the AI service server
- **Default**: `9563`
- **Required**: No
- **Example**: `PORT=9563`

#### AI_TOKEN

- **Description**: Authentication token for AI service and ReadMe API communication
- **Default**: `"secret"`
- **Required**: Yes (for production)
- **Usage**: Used to authenticate requests between ReadMe main application and AI service
- **Local Development**: Can be any non-empty string as long as it matches in both repos
- **Example**: `AI_TOKEN=your_secure_token_here`

#### README_DOMAIN

- **Description**: Base URL of the ReadMe service
- **Default**: `http://dash.readme.local:3000`
- **Required**: No (uses default for local development)
- **Usage**: Used for API calls to ReadMe server
- **Environment-Specific Values**:
  - Local: `http://dash.readme.local:3000`
  - Next: `https://dash.next.readme.ninja`
  - Staging: `https://dash.readmestaging.com`
  - Production: `https://dash.readme.com`
- **Example**: `README_DOMAIN=https://dash.readme.com`

#### AI_SERVER_URL

- **Description**: URL of the AI service
- **Default**: `http://localhost:9563`
- **Required**: No (uses default for local development)
- **Usage**: Used for integration tests and service-to-service communication
- **Environment-Specific Values**:
  - Local: `http://localhost:9563`
  - Next: `https://readme-ai-next.onrender.com`
  - Staging: `https://readme-ai-stage.onrender.com`
  - Production: `https://readme-ai.onrender.com`
- **Example**: `AI_SERVER_URL=https://readme-ai.onrender.com`

## AI Provider API Keys

### OpenAI Configuration

#### OPENAI_KEY

- **Description**: OpenAI API key for text generation and embeddings
- **Required**: Yes (for chat, vectorization, and evaluation features)
- **Usage**: Powers chat responses, document embeddings, and content evaluation
- **Features Requiring This Key**:
  - Chat (all modes)
  - Vectorization (document indexing)
  - Evaluation (groundtruth generation and scoring)
  - Linting (content analysis)
- **Where to Get**: OpenAI Dashboard or 1Password
- **Example**: `OPENAI_KEY=sk-proj-...`

**Note**: This is the most critical API key. Without it, most AI features will not function.

### Google Gemini Configuration

#### GOOGLE_GENERATIVE_AI_API_KEY

- **Description**: Google Gemini API key for alternative text generation
- **Required**: Yes (application crashes without it)
- **Usage**: Alternative LLM provider for chat and evaluation
- **Features Requiring This Key**:
  - Chat (when using Gemini models)
  - Evaluation (when using Gemini as judge)
  - Linting (when using Gemini models)
- **Where to Get**: Google Cloud Console or 1Password
- **Example**: `GOOGLE_GENERATIVE_AI_API_KEY=AIza...`

## Database Configuration

### MongoDB Atlas

#### AI_MONGO_URI

- **Description**: MongoDB Atlas connection string for vector search
- **Default**: `""` (empty string)
- **Required**: Yes (for vectorization and chat with context features)
- **Important**: Regular MongoDB will not work. Must be MongoDB Atlas with vector search enabled.
- **Example**: `AI_MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname`

**Local Development Options**:

1. **Run without MongoDB** (default):
   - Leave `AI_MONGO_URI` empty
   - Database operations will fail, but server will start
   - Suitable if not using database features

2. **Use staging MongoDB**:
   - Get connection string from 1Password
   - Set `AI_MONGO_URI` to staging connection string

3. **Use your own MongoDB Atlas instance**:
   - Create MongoDB Atlas cluster
   - Enable vector search
   - Set `AI_MONGO_URI` to your connection string
   - Initialize database: `npm run cli:vectorize initdb`

4. **Start local MongoDB Atlas container**:
   ```bash
   ./start-mongo.sh
   # Copy the connection_string output
   # Set AI_MONGO_URI to that value
   npm run cli:vectorize initdb
   ```

**Database Initialization**:

Only needed for new MongoDB instances:

```bash
npm run cli:vectorize initdb
```

This creates:
- `readme-ai-vector-collection`
- `vectorizeQueue`
- Vector search indexes

## ReadMe Integration

### README_API_KEY

- **Description**: API key for ReadMe API access
- **Required**: Yes (for integration tests and vectorization)
- **Usage**: Authenticate requests to ReadMe API for fetching documentation
- **Where to Get**:
  - Local: `https://dash.readme.com/project/<your-project>/v3.0/api-key`
  - Next: `https://dash.next.readme.ninja/project/developers/v3.0/api-key`
  - Staging: `https://dash.readmestaging.com/project/developers/v3.0/api-key`
  - Production: `https://dash.readme.com/project/developers/v3.0/api-key`
- **Example**: `README_API_KEY=rdme_...`

## Feature-Specific Configuration

### Chat Features

Chat functionality requires:

- `OPENAI_KEY` (required)
- `GOOGLE_GENERATIVE_AI_API_KEY` (required)
- `AI_MONGO_URI` (required for context-based chat)

**Environment Setup for Chat**:

```bash
OPENAI_KEY=sk-proj-... \
GOOGLE_GENERATIVE_AI_API_KEY=AIza... \
AI_MONGO_URI=mongodb+srv://... \
npm run cli:chat
```

### Vectorization Features

Vectorization requires:

- `OPENAI_KEY` (required for embeddings)
- `AI_MONGO_URI` (required for storage)
- `AI_TOKEN` (required for authentication)
- `README_DOMAIN` (required for fetching docs)

**Environment Setup for Vectorization**:

```bash
OPENAI_KEY=sk-proj-... \
AI_MONGO_URI=mongodb+srv://... \
AI_TOKEN=secret \
README_DOMAIN=http://dash.readme.local:3000 \
npm run cli:vectorize index <subdomain>
```

### Linting Features

Linting requires:

- `OPENAI_KEY` (required)
- `GOOGLE_GENERATIVE_AI_API_KEY` (required)

**Environment Setup for Linting**:

```bash
OPENAI_KEY=sk-proj-... \
GOOGLE_GENERATIVE_AI_API_KEY=AIza... \
npm run cli:lint rules
```

### Evaluation Features

Evaluation requires:

- `OPENAI_KEY` (required)
- `GOOGLE_GENERATIVE_AI_API_KEY` (required)
- `AI_MONGO_URI` (required)

**Environment Setup for Evaluation**:

```bash
OPENAI_KEY=sk-proj-... \
GOOGLE_GENERATIVE_AI_API_KEY=AIza... \
AI_MONGO_URI=mongodb+srv://... \
npm run cli:eval ./evals/subdomain/groundtruths/file.json subdomain
```

### MCP Server Features

MCP server requires:

- `OPENAI_KEY` (required)
- `GOOGLE_GENERATIVE_AI_API_KEY` (required)
- `AI_TOKEN` (required)
- `README_DOMAIN` (required)

**Environment Setup for MCP**:

```bash
OPENAI_KEY=sk-proj-... \
GOOGLE_GENERATIVE_AI_API_KEY=AIza... \
AI_TOKEN=secret \
README_DOMAIN=http://dash.readme.local:3000 \
npm run dev
```

## Integration Testing Configuration

Integration tests require all core variables:

```bash
README_API_KEY=rdme_... \
AI_TOKEN=secret \
README_DOMAIN=http://dash.readme.local:3000 \
AI_SERVER_URL=http://localhost:9563 \
OPENAI_KEY=sk-proj-... \
GOOGLE_GENERATIVE_AI_API_KEY=AIza... \
AI_MONGO_URI=mongodb+srv://... \
npm run test:integration
```

## Environment Files

### Using .env Files

Create a `.env` file in the project root:

```bash
# Core Configuration
PORT=9563
AI_TOKEN=secret
README_DOMAIN=http://dash.readme.local:3000
AI_SERVER_URL=http://localhost:9563

# API Keys
OPENAI_KEY=sk-proj-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...

# Database
AI_MONGO_URI=mongodb+srv://...

# ReadMe Integration
README_API_KEY=rdme_...
```

**Note**: Never commit `.env` files to version control. Add to `.gitignore`.

### Environment-Specific Files

The project uses `config` package for environment management:

- `config/default.json` - Default values
- `config/custom-environment-variables.json` - Environment variable mappings
- `config/{environment}.json` - Environment-specific overrides

## Configuration Validation

### Checking Required Variables

Before starting the server, verify required variables are set:

```bash
# Check if variables are set
echo $OPENAI_KEY
echo $GOOGLE_GENERATIVE_AI_API_KEY
echo $AI_MONGO_URI
```

### Testing Configuration

Test server startup with your configuration:

```bash
npm run build && npm start
```

If the server starts successfully, your configuration is valid.

## Common Configuration Scenarios

### Local Development (Full Features)

```bash
OPENAI_KEY=sk-proj-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
AI_MONGO_URI=mongodb+srv://...
AI_TOKEN=secret
README_DOMAIN=http://dash.readme.local:3000
README_API_KEY=rdme_...
```

### Local Development (Minimal)

```bash
OPENAI_KEY=sk-proj-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
AI_TOKEN=secret
```

### Staging Environment

```bash
OPENAI_KEY=sk-proj-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
AI_MONGO_URI=mongodb+srv://staging-cluster...
AI_TOKEN=staging_token
README_DOMAIN=https://dash.readmestaging.com
AI_SERVER_URL=https://readme-ai-stage.onrender.com
```

### Production Environment

```bash
OPENAI_KEY=sk-proj-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
AI_MONGO_URI=mongodb+srv://prod-cluster...
AI_TOKEN=production_token
README_DOMAIN=https://dash.readme.com
AI_SERVER_URL=https://readme-ai.onrender.com
```

## Security Best Practices

### API Key Management

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate keys regularly** in production
4. **Use different keys** for different environments
5. **Store keys securely** in 1Password or similar

### Token Security

1. **Use strong tokens** in production (not "secret")
2. **Keep tokens consistent** between ReadMe and AI service
3. **Rotate tokens** when team members leave
4. **Monitor token usage** for suspicious activity

### Database Security

1. **Use connection string encryption** in production
2. **Restrict IP access** to MongoDB Atlas
3. **Use strong passwords** for database users
4. **Enable audit logging** for production databases

## Troubleshooting

### Server Won't Start

**Error**: Application crashes immediately

**Cause**: Missing required API keys

**Solution**: Ensure `OPENAI_KEY` and `GOOGLE_GENERATIVE_AI_API_KEY` are set

```bash
# Check if keys are set
echo $OPENAI_KEY
echo $GOOGLE_GENERATIVE_AI_API_KEY
```

### Database Connection Fails

**Error**: MongoDB connection errors

**Cause**: Invalid connection string or network issues

**Solution**:
1. Verify `AI_MONGO_URI` is correct
2. Check MongoDB Atlas allows your IP
3. Test connection string in MongoDB Compass

### Authentication Errors

**Error**: 401 Unauthorized responses

**Cause**: Mismatched `AI_TOKEN` between services

**Solution**: Ensure `AI_TOKEN` matches in both ReadMe and AI service

### Integration Test Failures

**Error**: Tests fail with connection errors

**Cause**: Missing integration test variables

**Solution**: Set all required variables for integration tests:

```bash
README_API_KEY=rdme_...
AI_TOKEN=secret
README_DOMAIN=http://dash.readme.local:3000
AI_SERVER_URL=http://localhost:9563
```

## Getting API Keys

### OpenAI

1. Visit [OpenAI Dashboard](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create new secret key
4. Copy and store securely in 1Password

### Google Gemini

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Generative AI API
3. Create API credentials
4. Copy and store securely in 1Password

### ReadMe API Key

1. Log into ReadMe dashboard
2. Navigate to project settings
3. Go to API Key section
4. Copy existing key or generate new one
5. Store securely in 1Password

## Reference

### All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | `9563` | Server port |
| `AI_TOKEN` | Yes | `"secret"` | Authentication token |
| `README_DOMAIN` | No | `http://dash.readme.local:3000` | ReadMe server URL |
| `AI_SERVER_URL` | No | `http://localhost:9563` | AI service URL |
| `OPENAI_KEY` | Yes | - | OpenAI API key |
| `GOOGLE_GENERATIVE_AI_API_KEY` | Yes | - | Google Gemini API key |
| `AI_MONGO_URI` | No | `""` | MongoDB Atlas connection string |
| `README_API_KEY` | No | - | ReadMe API key |

### Configuration Files

- `config/default.json` - Default configuration values
- `config/custom-environment-variables.json` - Environment variable mappings
- `config/{environment}.json` - Environment-specific overrides
- `.env` - Local environment variables (not committed)

### Related Documentation

- [README.md](../README.md) - Main project documentation
- [AI Services](../src/ai/README.md) - AI features overview
- [MCP Server](./mcp-server.md) - MCP server configuration
- [Vectorization](./vectorization.md) - Vector database setup
