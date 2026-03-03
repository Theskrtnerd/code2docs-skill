---
title: API Reference
slug: api-reference
category:
  uri: Documentation
content:
  excerpt: Complete API endpoint documentation for chat, agent chat, vectorization, and linting routes, including request/response formats and authentication.
---

# API Reference

Complete API endpoint documentation for chat, agent chat, vectorization, and linting routes, including request/response formats and authentication.

## Overview

The ReadMe AI Service provides a comprehensive REST API for AI-powered documentation features. This reference covers all available endpoints, authentication methods, request/response formats, and error handling.

**Base URL**: `http://localhost:9563` (development) or your deployed instance URL

**API Version**: Current

## Authentication

All API requests require authentication using a bearer token.

### Authentication Header

Include your API token in the `Authorization` header of every request:

```http
Authorization: Bearer YOUR_API_TOKEN
```

### Getting Your API Token

**For Development**:
- Set `AI_TOKEN` environment variable (default: `"secret"`)
- Token must match between AI service and ReadMe application

**For Production**:
- Obtain token from your deployment environment
- Store securely and never expose in client-side code

### Authentication Errors

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
```

## Rate Limiting

Currently, the API does not enforce rate limits. However, be mindful of:

- **LLM API costs**: Each request consumes tokens from your OpenAI/Google API quota
- **Database operations**: Vectorization operations are resource-intensive
- **Concurrent requests**: Limit parallel requests to avoid overwhelming the service

## Common Response Formats

### Success Response

Most endpoints return JSON responses with appropriate HTTP status codes:

```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response

Error responses follow a consistent format:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error description",
  "details": { ... }
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error
- `503 Service Unavailable`: Service temporarily unavailable

## Chat Endpoints

### Simple Chat

Execute a basic chat request without documentation context.

**Endpoint**: `POST /chat/simple`

**Request Body**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is an API?"
    }
  ],
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | Array | Yes | Array of message objects with `role` and `content` |
| `llmOptions` | Object | No | LLM configuration options |
| `llmOptions.model` | String | No | Model to use (default: `gpt-4o`) |
| `llmOptions.customModel` | Object | No | Custom model configuration |

**Response** (Streaming):

```
data: {"type":"text-delta","textDelta":"An API"}
data: {"type":"text-delta","textDelta":" (Application"}
data: {"type":"text-delta","textDelta":" Programming"}
data: {"type":"text-delta","textDelta":" Interface)"}
data: [DONE]
```

**Example Request**:

```bash
curl -X POST http://localhost:9563/chat/simple \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Explain REST APIs in simple terms"
      }
    ],
    "llmOptions": {
      "model": "gpt-4o"
    }
  }'
```

### Chat with Context

Execute chat with documentation context (RAG).

**Endpoint**: `POST /chat/withContext`

**Request Body**:

```json
{
  "query": "How do I authenticate?",
  "subdomains": ["my-docs"],
  "options": {
    "answerLength": "medium",
    "customTone": "friendly and helpful"
  },
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | String | Yes | User's question |
| `subdomains` | Array | Yes | List of project subdomains to search |
| `options` | Object | No | Customization options |
| `options.answerLength` | String | No | `short`, `medium`, `long`, or `unrestricted` |
| `options.customTone` | String | No | Desired response tone |
| `options.defaultAnswer` | String | No | Fallback when no context found |
| `options.forbiddenWords` | Array | No | Words to avoid in response |
| `llmOptions` | Object | No | LLM configuration |
| `pageContext` | Object | No | Current page context |

**Response** (Streaming):

```
data: {"type":"text-delta","textDelta":"To authenticate"}
data: {"type":"text-delta","textDelta":", include your"}
data: {"type":"text-delta","textDelta":" API key in"}
data: {"type":"source","source":{"title":"Authentication","url":"https://..."}}
data: [DONE]
```

**Example Request**:

```bash
curl -X POST http://localhost:9563/chat/withContext \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I create an API key?",
    "subdomains": ["developers"],
    "options": {
      "answerLength": "medium",
      "customTone": "professional"
    }
  }'
```

### Conversation Chat

Multi-turn conversation with context.

**Endpoint**: `POST /chat/conversation`

**Request Body**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I create an API key?"
    },
    {
      "role": "assistant",
      "content": "You can create an API key from your dashboard..."
    },
    {
      "role": "user",
      "content": "Can I revoke it later?"
    }
  ],
  "subdomains": ["my-docs"],
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | Array | Yes | Conversation history |
| `subdomains` | Array | Yes | Projects to search |
| `options` | Object | No | Same as withContext |
| `llmOptions` | Object | No | LLM configuration |

**Response**: Same streaming format as withContext

**Example Request**:

```bash
curl -X POST http://localhost:9563/chat/conversation \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What are webhooks?"},
      {"role": "assistant", "content": "Webhooks are..."},
      {"role": "user", "content": "How do I set one up?"}
    ],
    "subdomains": ["developers"]
  }'
```

### Agent Chat

Execute agent chat with tool calling capabilities.

**Endpoint**: `POST /chat/agentChat`

**Request Body**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Search the documentation for authentication methods and summarize them"
    }
  ],
  "subdomains": ["my-docs"],
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | Array | Yes | Conversation history |
| `subdomains` | Array | Yes | Projects to search |
| `llmOptions` | Object | No | LLM configuration |
| `options` | Object | No | Customization options |

**Response** (Streaming):

```
data: {"type":"text-delta","textDelta":"Let me search"}
data: {"type":"tool-call","toolCallId":"call_123","toolName":"retrieveKnowledge","args":{"query":"authentication"}}
data: {"type":"tool-result","toolCallId":"call_123","result":{"text":"...","sources":[...]}}
data: {"type":"text-delta","textDelta":"Based on the documentation"}
data: [DONE]
```

**Available Tools**:

- `retrieveKnowledge`: Search documentation
- `analyzeUrl`: Analyze web page content
- `searchWeb`: Search the web
- `rewritePage`: Edit documentation pages
- `updateApiReference`: Update API reference

**Example Request**:

```bash
curl -X POST http://localhost:9563/chat/agentChat \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Find information about rate limiting and create a summary"
      }
    ],
    "subdomains": ["developers"]
  }'
```

## Vectorization Endpoints

### Initialize Database

Create required MongoDB collections and indexes.

**Endpoint**: `POST /vectorize/initdb`

**Request Body**: None

**Response**:

```json
{
  "success": true,
  "message": "Database initialized successfully"
}
```

**Example Request**:

```bash
curl -X POST http://localhost:9563/vectorize/initdb \
  -H "Authorization: Bearer secret"
```

**Note**: Only run this once per database instance.

### Index Documentation

Vectorize all documentation for a subdomain.

**Endpoint**: `POST /vectorize/index`

**Request Body**:

```json
{
  "subdomain": "my-docs"
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | String | Yes | Project subdomain to index |

**Response**:

```json
{
  "success": true,
  "jobCount": 35,
  "message": "Vectorization started"
}
```

**Example Request**:

```bash
curl -X POST http://localhost:9563/vectorize/index \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{"subdomain": "developers"}'
```

### Check Vectorization Status

Get the status of vectorization jobs.

**Endpoint**: `GET /vectorize/status/:subdomain`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subdomain` | String | Yes | Project subdomain (URL parameter) |

**Response**:

```json
{
  "subdomain": "my-docs",
  "totalJobs": 35,
  "completedJobs": 30,
  "failedJobs": 0,
  "pendingJobs": 5,
  "status": "in_progress"
}
```

**Example Request**:

```bash
curl http://localhost:9563/vectorize/status/developers \
  -H "Authorization: Bearer secret"
```

## Linting Endpoints

### Lint Content (Rules)

Check content against custom rules.

**Endpoint**: `POST /lint/rules`

**Request Body**:

```json
{
  "prompt": "Don't use emojis\nAlways capitalize ReadMe as ReadMe",
  "content": "This is readme documentation 🎨",
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | String | Yes | Rules to check against |
| `content` | String | Yes | Content to analyze |
| `llmOptions` | Object | No | LLM configuration |

**Response**:

```json
{
  "violations": [
    {
      "rule": "Don't Use Emojis",
      "message": "Emoji '🎨' found.",
      "violatingText": "🎨",
      "startIndex": 35,
      "endIndex": 37
    },
    {
      "rule": "ReadMe Capitalization",
      "message": "'readme' should be capitalized as 'ReadMe'",
      "violatingText": "readme",
      "startIndex": 8,
      "endIndex": 14
    }
  ]
}
```

**Example Request**:

```bash
curl -X POST http://localhost:9563/lint/rules \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Use curly quotes instead of straight quotes",
    "content": "This is a \"test\" document"
  }'
```

### Lint Content (Style Guide)

Score content against a style guide.

**Endpoint**: `POST /lint/styleguide`

**Request Body**:

```json
{
  "prompt": "Our style guide emphasizes clarity and simplicity...",
  "content": "# Getting Started\n\nThis guide will help you...",
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | String | Yes | Style guide description |
| `content` | String | Yes | Content to analyze |
| `llmOptions` | Object | No | LLM configuration |

**Response**:

```json
{
  "score": 8,
  "feedback": "The content follows the style guide well. It uses clear, simple language and maintains a consistent tone. Consider breaking up longer paragraphs for better readability."
}
```

**Score Range**: 0-10 (10 being perfect adherence)

**Example Request**:

```bash
curl -X POST http://localhost:9563/lint/styleguide \
  -H "Authorization: Bearer secret" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Use active voice and short sentences",
    "content": "The API was called by the user"
  }'
```

## LLM Options

All chat and linting endpoints support LLM configuration through the `llmOptions` parameter.

### Supported Models

**OpenAI**:
- `gpt-4o` (default for chat)
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

**Google**:
- `gemini-2.5-pro`
- `gemini-2.5-flash`
- `gemini-2.0-flash`

**Anthropic**:
- `claude-3-5-sonnet-20241022`
- `claude-3-opus-20240229`

### Custom Models

Use any OpenAI-compatible endpoint:

```json
{
  "llmOptions": {
    "customModel": {
      "modelId": "custom-model-name",
      "baseUrl": "https://api.example.com/v1",
      "apiKey": "your-api-key"
    }
  }
}
```

### Model Parameters

```json
{
  "llmOptions": {
    "model": "gpt-4o",
    "temperature": 0.7,
    "maxTokens": 2000,
    "topP": 1.0
  }
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | String | `gpt-4o` | Model identifier |
| `temperature` | Number | 0.7 | Randomness (0.0-2.0) |
| `maxTokens` | Number | 2000 | Maximum response length |
| `topP` | Number | 1.0 | Nucleus sampling |

## Streaming Responses

Chat endpoints return Server-Sent Events (SSE) for streaming responses.

### Event Types

**text-delta**: Incremental text chunks

```json
{"type":"text-delta","textDelta":"Hello"}
```

**source**: Source citation

```json
{
  "type":"source",
  "source":{
    "title":"Authentication Guide",
    "url":"https://docs.example.com/auth"
  }
}
```

**tool-call**: Agent tool invocation

```json
{
  "type":"tool-call",
  "toolCallId":"call_123",
  "toolName":"retrieveKnowledge",
  "args":{"query":"authentication"}
}
```

**tool-result**: Tool execution result

```json
{
  "type":"tool-result",
  "toolCallId":"call_123",
  "result":{"text":"...","sources":[...]}
}
```

**done**: Stream complete

```
data: [DONE]
```

### Consuming Streams

**JavaScript Example**:

```javascript
const response = await fetch('http://localhost:9563/chat/withContext', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer secret',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'How do I authenticate?',
    subdomains: ['developers']
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') break;
      
      const event = JSON.parse(data);
      console.log(event);
    }
  }
}
```

## Error Handling

### Common Errors

**Missing API Keys**:

```json
{
  "error": "ConfigurationError",
  "message": "OPENAI_KEY environment variable not set"
}
```

**Invalid Subdomain**:

```json
{
  "error": "NotFoundError",
  "message": "Subdomain 'invalid-project' not found"
}
```

**Vectorization Not Complete**:

```json
{
  "error": "VectorizationError",
  "message": "Documentation not vectorized for subdomain 'my-docs'"
}
```

**LLM API Error**:

```json
{
  "error": "LLMError",
  "message": "OpenAI API rate limit exceeded",
  "details": {
    "provider": "openai",
    "statusCode": 429
  }
}
```

### Retry Strategy

For transient errors (500, 503, 429):

1. Implement exponential backoff
2. Start with 1 second delay
3. Double delay on each retry
4. Maximum 5 retries
5. Maximum 32 second delay

**Example**:

```javascript
async function retryRequest(fn, maxRetries = 5) {
  let delay = 1000;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      if (![429, 500, 503].includes(error.statusCode)) throw error;
      
      await new Promise(resolve => setTimeout(resolve, delay));
      delay = Math.min(delay * 2, 32000);
    }
  }
}
```

## Best Practices

### Performance

1. **Vectorize documentation first**: Always vectorize before using chat endpoints
2. **Limit subdomain count**: Search 1-3 subdomains for best performance
3. **Use appropriate models**: `gpt-4o-mini` for simple queries, `gpt-4o` for complex ones
4. **Cache responses**: Cache common queries client-side
5. **Stream responses**: Use streaming for better UX

### Security

1. **Protect API tokens**: Never expose tokens in client-side code
2. **Validate input**: Sanitize user input before sending to API
3. **Use HTTPS**: Always use encrypted connections in production
4. **Monitor usage**: Track API calls to detect anomalies
5. **Rotate tokens**: Regularly rotate authentication tokens

### Cost Optimization

1. **Choose efficient models**: Balance cost vs. quality
2. **Limit context**: Only include necessary documentation
3. **Set token limits**: Use `maxTokens` to control response length
4. **Monitor spending**: Track LLM API usage and costs
5. **Cache aggressively**: Reduce redundant API calls

## SDK Usage

### JavaScript Client

```javascript
import { AiClient } from '@readme/ai-client';

const client = new AiClient({
  url: 'http://localhost:9563',
  authToken: 'secret'
});

// Simple chat
const response = await client.chat.simple({
  messages: [{ role: 'user', content: 'Hello!' }]
});

// Chat with context
const stream = await client.chat.withContext({
  query: 'How do I authenticate?',
  subdomains: ['developers']
});

for await (const chunk of stream) {
  console.log(chunk);
}

// Vectorize documentation
await client.vectorize.index({ subdomain: 'developers' });

// Lint content
const violations = await client.lint.rules({
  prompt: 'No emojis',
  content: 'Hello 🎨'
});
```

## Support

For technical support and questions:

- **Documentation**: https://docs.readme.com
- **GitHub Issues**: https://github.com/readmeio/ai/issues
- **Email**: support@readme.io
