---
title: AI Agent
slug: ai-agent
category:
  uri: Documentation
content:
  excerpt: Guide to the tool-augmented AI agent capabilities, including available tools (knowledge retrieval, web search, URL analysis, content editing), tool call flow, and extended reasoning modes.
---

# AI Agent

Complete guide to the tool-augmented AI agent capabilities, including available tools, tool call flow, and extended reasoning modes.

## Overview

The AI Agent extends chat capabilities with intelligent tool integration, enabling AI to interact with documentation, search the web, analyze URLs, and perform content editing tasks. The agent automatically selects and executes appropriate tools based on user requests, providing accurate, context-aware responses with proper source citations.

**Key Capabilities**:

- **Autonomous Tool Selection**: Agent determines which tools to use based on context
- **Multi-Step Reasoning**: Chain multiple tool calls to answer complex queries
- **Knowledge Retrieval**: Search and cite documentation from multiple projects
- **Web Integration**: Access current information through web search and URL analysis
- **Content Editing**: Rewrite documentation pages and update API references
- **Extended Thinking**: Support for advanced reasoning modes (Claude thinking, OpenAI reasoning)

## Architecture

```
User Request
    ↓
Agent Chat Endpoint (/chat/agentChat)
    ↓
Agent Analysis (determine if tools needed)
    ↓
Tool Selection (based on request context)
    ↓
Tool Execution (sequential, up to 10 calls)
    ↓
Result Integration
    ↓
Response Generation (with citations)
    ↓
Streaming Response to Client
```

## Agent Chat Endpoint

### POST /chat/agentChat

Execute agent chat with automatic tool calling capabilities.

**Request Format**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I authenticate with the API?"
    }
  ],
  "subdomains": ["developers"],
  "llmOptions": {
    "model": "gpt-4o"
  },
  "maxToolCalls": 10
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | Array | Yes | Conversation history with role and content |
| `subdomains` | Array | No | Projects to search (defaults to `["developers"]`) |
| `llmOptions` | Object | No | LLM configuration (model, temperature, etc.) |
| `maxToolCalls` | Number | No | Maximum tool calls allowed (default: 10) |
| `pageContext` | Object | No | Current page information for context |

**Response Format** (Server-Sent Events):

The response is streamed as newline-delimited JSON objects:

```json
{"type":"text-delta","textDelta":"Based on the documentation"}
{"type":"tool-call","toolCallId":"call_123","toolName":"retrieveKnowledge","args":{"query":"authentication"}}
{"type":"tool-result","toolCallId":"call_123","result":{"text":"...","sources":[...]}}
{"type":"text-delta","textDelta":", you can authenticate using..."}
```

**Event Types**:

- `text-delta`: Incremental text response
- `tool-call`: Tool invocation with arguments
- `tool-result`: Tool execution result
- `error`: Error message

## Available Tools

### 1. retrieveKnowledge

Search documentation and retrieve relevant context from multiple subdomains.

**Purpose**: Find and cite documentation content to answer questions

**Parameters**:

```typescript
{
  query: string;        // Search query
  subdomains?: string[]; // Projects to search (optional)
}
```

**Implementation Details**:

- Searches across specified subdomains (includes 'developers' by default)
- Returns top 5 most relevant documents sorted by similarity score
- Combines document content into a single text response
- Includes source citations with URLs and titles

**Example Tool Call**:

```json
{
  "toolName": "retrieveKnowledge",
  "args": {
    "query": "API authentication methods",
    "subdomains": ["developers", "api-docs"]
  }
}
```

**Example Result**:

```json
{
  "text": "Authentication can be done using API keys...",
  "sources": [
    {
      "url": "https://developers.readme.io/docs/authentication",
      "title": "Authentication Guide"
    }
  ]
}
```

### 2. analyzeUrl

Analyze content from a specific URL and extract relevant information.

**Purpose**: Extract and analyze content from web pages

**Parameters**:

```typescript
{
  url: string; // URL to analyze
}
```

**Implementation Details**:

- Uses grounding tools to fetch and analyze URL content
- Filters results to URL sources only
- Limits content to 10,000 characters
- Returns up to 5 sources

**Example Tool Call**:

```json
{
  "toolName": "analyzeUrl",
  "args": {
    "url": "https://example.com/blog/api-best-practices"
  }
}
```

### 3. searchWeb

Search the web for current information about a specific topic.

**Purpose**: Find up-to-date information from the web

**Parameters**:

```typescript
{
  query: string; // Search query
}
```

**Implementation Details**:

- Uses grounding tools to search the web
- Filters results to URL sources
- Limits content to 10,000 characters
- Returns up to 5 sources

**Example Tool Call**:

```json
{
  "toolName": "searchWeb",
  "args": {
    "query": "REST API authentication best practices 2024"
  }
}
```

### 4. rewritePage

Rewrite page content and optionally update the page title and meta description.

**Purpose**: Edit documentation pages

**Parameters**:

```typescript
{
  content: string;       // New page content
  title?: string;        // New page title (optional)
  excerpt?: string;      // New meta description (optional)
}
```

**Note**: This tool is defined in the AI service but executed by the ReadMe application.

### 5. updateApiReference

Generate a JSON payload to update a single API reference page.

**Purpose**: Update API endpoint documentation

**Parameters**:

```typescript
{
  path: string;          // API path (e.g., "/users/{id}")
  method: string;        // HTTP method (get, post, put, delete, etc.)
  operation: object;     // OpenAPI 3.0.0 Operation Object
}
```

**Implementation Details**:

- Validates against OpenAPI 3.0.0 PathsObject format
- Ensures proper structure for path items and operations
- Returns JSON payload for API reference updates

**Example Tool Call**:

```json
{
  "toolName": "updateApiReference",
  "args": {
    "path": "/users/{id}",
    "method": "get",
    "operation": {
      "summary": "Get user by ID",
      "parameters": [...],
      "responses": {...}
    }
  }
}
```

## Tool Call Flow

### 1. Request Analysis

When a user sends a message, the agent analyzes whether tools are needed:

```typescript
// Agent determines context and intent
const needsTools = analyzeRequest(userMessage, conversationHistory);
```

### 2. Tool Selection

The agent selects appropriate tools based on the request:

**Selection Criteria**:

- **Documentation questions** → `retrieveKnowledge`
- **Specific URL analysis** → `analyzeUrl`
- **Current web information** → `searchWeb`
- **Content editing** → `rewritePage`
- **API updates** → `updateApiReference`

### 3. Tool Execution

Tools execute sequentially (not in parallel):

```
Tool Call 1 → Result 1
    ↓
Tool Call 2 → Result 2
    ↓
Tool Call 3 → Result 3
    ↓
Response Generation
```

**Execution Limits**:

- Maximum 10 tool calls per request (configurable via `maxToolCalls`)
- Each tool has a timeout limit
- Failed tool calls return error messages

### 4. Result Integration

The agent incorporates tool results into the response:

```typescript
// Combine tool results with agent reasoning
const response = generateResponse({
  userQuery,
  toolResults,
  conversationHistory
});
```

### 5. Streaming Response

The response is streamed back to the client in chunks:

```json
{"type":"text-delta","textDelta":"Based on "}
{"type":"text-delta","textDelta":"the documentation, "}
{"type":"text-delta","textDelta":"you can authenticate using API keys."}
```

## Extended Thinking / Reasoning

The agent supports extended reasoning modes for complex problem-solving tasks. These modes allow the AI to "think" through problems step-by-step before generating a response.

### Configuration

Extended thinking is controlled via the `extendedThinkingBudget` parameter in `src/ai/constants.ts`:

```typescript
export const EXTENDED_THINKING_BUDGET = 0; // Default: disabled
```

**Budget Values**:

- `0`: Disabled (default, minimizes latency and cost)
- `1-10000`: Number of thinking tokens allowed

### Supported Models

**Claude (Anthropic)**:

- Uses Claude's native thinking capability
- Thinking process is separate from response
- Configurable via `thinking` parameter

**OpenAI**:

- Uses reasoning models (o1, o3, etc.)
- Reasoning integrated into response generation
- Configurable via model selection

### When to Use Extended Thinking

**Enable for**:

- Complex multi-step reasoning tasks
- Code generation requiring planning
- Analysis of intricate technical problems
- Tasks requiring careful consideration

**Disable for**:

- Simple documentation lookups
- Quick factual questions
- Real-time chat interactions
- Cost-sensitive applications

### Example Configuration

```typescript
// Enable extended thinking
const response = await agentChat({
  messages: [...],
  llmOptions: {
    model: "claude-3-5-sonnet-20241022",
    extendedThinkingBudget: 5000
  }
});
```

## Multi-Step Reasoning

The agent can chain multiple tool calls to answer complex queries:

**Example Flow**:

```
User: "Compare our authentication methods with industry best practices"
    ↓
Step 1: retrieveKnowledge("authentication methods")
    ↓
Step 2: searchWeb("API authentication best practices 2024")
    ↓
Step 3: Generate comparison with citations
```

**Benefits**:

- Handles complex, multi-faceted questions
- Combines internal and external knowledge
- Provides comprehensive, well-sourced answers

## File Attachments

The agent supports file attachments in conversations:

**Supported File Types**:

- Text files (.txt, .md, .json, etc.)
- Code files (.js, .py, .java, etc.)
- Configuration files (.yaml, .toml, etc.)

**Usage**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Review this API specification"
        },
        {
          "type": "file",
          "file": {
            "name": "openapi.yaml",
            "content": "..."
          }
        }
      ]
    }
  ]
}
```

## Best Practices

### Tool Selection

**Do**:

- Let the agent select tools automatically
- Provide clear, specific queries
- Include relevant context in messages

**Don't**:

- Manually specify which tools to use
- Send vague or ambiguous requests
- Omit important context

### Performance Optimization

**Reduce Latency**:

- Disable extended thinking for simple queries
- Limit `maxToolCalls` for straightforward questions
- Use faster models (gpt-4o-mini, gemini-flash)

**Improve Accuracy**:

- Enable extended thinking for complex tasks
- Increase `maxToolCalls` for multi-step reasoning
- Use more capable models (gpt-4o, claude-3-5-sonnet)

### Error Handling

**Common Errors**:

- **Tool timeout**: Tool execution exceeded time limit
- **Max calls reached**: Hit `maxToolCalls` limit
- **Invalid arguments**: Tool called with incorrect parameters

**Recovery Strategies**:

- Retry with simplified query
- Increase timeout limits
- Adjust `maxToolCalls` setting

## Troubleshooting

### Agent Not Using Tools

**Symptom**: Agent responds without calling tools

**Causes**:

- Query too simple (doesn't require tools)
- Agent determined tools unnecessary
- Tool definitions not loaded

**Solutions**:

1. Rephrase query to be more specific
2. Verify tool definitions are registered
3. Check agent configuration

### Incorrect Tool Selection

**Symptom**: Agent uses wrong tool for the task

**Causes**:

- Ambiguous query
- Tool descriptions unclear
- Missing context

**Solutions**:

1. Provide more specific instructions
2. Include relevant context in message
3. Review tool descriptions

### Tool Execution Failures

**Symptom**: Tools fail to execute or return errors

**Causes**:

- Invalid parameters
- External service unavailable
- Timeout exceeded

**Solutions**:

1. Check tool arguments are valid
2. Verify external services are accessible
3. Increase timeout limits

## Configuration Reference

### Agent Constants

Located in `src/ai/constants.ts`:

```typescript
// Maximum tool calls per request
export const MAX_TOOL_CALLS = 10;

// Extended thinking budget (0 = disabled)
export const EXTENDED_THINKING_BUDGET = 0;

// Tool timeout (milliseconds)
export const TOOL_TIMEOUT = 30000;
```

### LLM Options

```typescript
{
  model: string;                    // Model ID
  temperature?: number;             // 0.0-2.0 (default: 1.0)
  maxTokens?: number;              // Max response tokens
  extendedThinkingBudget?: number; // Thinking tokens (0 = disabled)
}
```

### Subdomain Configuration

```typescript
{
  subdomains: string[];  // Projects to search
  // Default: ["developers"]
  // Example: ["developers", "api-docs", "guides"]
}
```

## Related Documentation

- [Ask AI Chat](./ask-ai-chat.md) - Conversational AI without tools
- [Vectorization](./vectorization.md) - Documentation indexing for retrieval
- [MCP Server](./mcp-server.md) - Model Context Protocol integration
