---
title: Ask AI Chat
slug: ask-ai-chat
category:
  uri: Documentation
content:
  excerpt: Documentation for the conversational AI chatbot feature with Retrieval-Augmented Generation (RAG), covering chat modes, customization options, and LLM configuration.
---

# Ask AI Chat

Complete documentation for the conversational AI chatbot feature with Retrieval-Augmented Generation (RAG), covering chat modes, customization options, and LLM configuration.

## Overview

Ask AI Chat is an intelligent conversational AI feature that enables users to get instant answers about your documentation. It combines the power of large language models (LLMs) with Retrieval-Augmented Generation (RAG) to provide accurate, contextual responses grounded in your actual documentation content.

**Key Capabilities**:

- Answer questions using documentation context
- Maintain multi-turn conversation history
- Support multiple LLM providers (OpenAI, Google Gemini, Anthropic)
- Customize response tone, length, and content filtering
- Provide source citations for transparency
- Search across multiple documentation projects

## How It Works

Ask AI Chat uses RAG to enhance AI responses with relevant documentation context:

```
User Question
    ↓
Query Contextualization (using conversation history)
    ↓
Vector Search (semantic similarity in documentation)
    ↓
Context Assembly (top K most relevant documents)
    ↓
Prompt Building (system instructions + context + history + query)
    ↓
LLM Generation (streaming response)
    ↓
Response with Citations
```

This approach ensures responses are grounded in your actual documentation rather than relying solely on the LLM's training data, reducing hallucinations and improving accuracy.

## Chat Modes

Ask AI Chat supports five distinct modes, each optimized for different use cases:

### 1. Simple Chat

Direct LLM interaction without modifications or context injection.

**Use Case**: Generic AI assistance, testing LLM behavior

**Characteristics**:
- No prompt modifications
- No documentation context
- Raw LLM responses
- Fastest response time

**When to Use**: When you need a general-purpose AI assistant without documentation-specific knowledge.

### 2. With Context (Single-Turn)

One-shot question answering with documentation context, used by Owlbot.

**Use Case**: Quick answers to specific documentation questions

**Flow**:
1. Search vector database for relevant documentation
2. Build prompt with documentation context
3. Generate response with citations

**Characteristics**:
- No conversation history
- Fresh context for each query
- Optimized for standalone questions
- Includes source citations

**When to Use**: For FAQ-style interactions where each question is independent.

### 3. Conversation (Multi-Turn)

Multi-turn conversations without documentation context.

**Use Case**: MDX conversion, general assistance tasks

**Characteristics**:
- Maintains conversation history
- Natural follow-up questions
- History-aware responses
- No documentation grounding

**When to Use**: For tasks requiring conversational context but not documentation knowledge.

### 4. Conversation with Context (Multi-Turn + RAG)

Full-featured conversational AI with documentation grounding—the primary mode for Ask AI Chat.

**Flow**:
1. **Contextualize**: Create search query using conversation history
2. **Search**: Query vector database with contextualized query
3. **Build**: Construct prompt with documentation + conversation history
4. **Generate**: Stream LLM response
5. **Cite**: Include source references

**Example Contextualization**:
```
History: "How do I create an API key?"
User Query: "Can I revoke it later?"
Contextualized Query: "How do I revoke an API key?"
```

**Characteristics**:
- Full conversation memory
- Documentation-grounded responses
- Intelligent query reformulation
- Source attribution

**When to Use**: For interactive documentation assistance where users ask follow-up questions.

### 5. Agent Chat

Advanced mode with tool-calling capabilities for complex workflows.

**Use Case**: Multi-step tasks, API interaction, content editing

**Capabilities**:
- Knowledge retrieval across projects
- Web search integration
- URL content analysis
- API endpoint execution
- Documentation editing

See the [AI Agent documentation](./ai-agent.md) for complete details.

## Retrieval-Augmented Generation (RAG)

### Vector Search Configuration

**Embedding Model**: OpenAI text-embedding-3-large (3,072 dimensions)

**Search Parameters**:
- **Similarity Threshold**: 0.75
- **Top-K Documents**: 10 (configurable)
- **Search Method**: Cosine similarity

**Implementation**: MongoDB Atlas Vector Search

### Query Contextualization

For multi-turn conversations, user queries are contextualized using chat history to improve retrieval accuracy.

**Process**:
1. Analyze conversation history
2. Identify key entities and topics
3. Reformulate query for better search results
4. Execute vector search with contextualized query

**Example**:
```
History:
  User: "How do I authenticate?"
  AI: "You can authenticate using API keys..."
  
Current Query: "Where do I find them?"

Contextualized: "Where do I find API keys for authentication?"
```

This ensures the vector search retrieves relevant documentation even when the user's query lacks context.

### Page Context Priority

When a user is viewing a specific documentation page, that page's content is prioritized in the context.

**Behavior**:
1. Page content is prepended to retrieved context
2. Vector search still executes normally
3. Both contexts are combined in the prompt
4. LLM has immediate access to current page content

**Benefits**:
- Faster answers about the current page
- Reduced need for vector search
- Better context relevance

### Multi-Subdomain Search

Enterprise users can search across multiple documentation projects simultaneously.

**Configuration**:
```json
{
  "subdomains": ["main-docs", "api-docs", "guides"]
}
```

**Behavior**:
- Searches all specified subdomains
- Returns results with full URLs
- Cites sources with project names
- Maintains separate vector indexes per project

**Use Case**: Organizations with multiple product documentation sets that need unified search.

## Customization Options

### Answer Length

Control response verbosity to match user preferences.

**Options**:
- `short`: 1-2 sentences
- `medium`: 1-2 paragraphs (default)
- `long`: Comprehensive, detailed explanation
- `unrestricted`: No length constraint

**Example Request**:
```json
{
  "query": "How do I authenticate?",
  "options": {
    "answerLength": "short"
  }
}
```

**Effect on Prompt**: Adds length instruction to system prompt, guiding LLM output length.

### Custom Tone

Adjust response style and personality.

**Example Values**:
- "professional and formal"
- "friendly and casual"
- "technical and precise"
- "beginner-friendly"

**Example Request**:
```json
{
  "query": "Explain webhooks",
  "options": {
    "customTone": "beginner-friendly"
  }
}
```

**Effect**: Modifies system prompt to adopt specified tone, affecting word choice, sentence structure, and explanation depth.

### Default Answer

Fallback response when no relevant documentation is found.

**Purpose**: Provide helpful guidance when the AI cannot answer from documentation.

**Example Request**:
```json
{
  "options": {
    "defaultAnswer": "I couldn't find information about that in our documentation. Please contact support at support@example.com for assistance."
  }
}
```

**When Used**: When vector search returns no results above the similarity threshold.

### Forbidden Words

Filter out specific terms from responses.

**Purpose**: Avoid competitor names, deprecated terminology, or sensitive terms.

**Example Request**:
```json
{
  "options": {
    "forbiddenWords": ["competitor-name", "legacy-feature", "deprecated-api"]
  }
}
```

**Behavior**:
- LLM is instructed to avoid these words
- Best-effort filtering (not guaranteed)
- Alternative phrasing encouraged

**Note**: This is a soft constraint—the LLM will attempt to avoid these words but may use them if necessary for clarity.

## LLM Configuration

### Supported Providers

**OpenAI**:
- GPT-4o (default for chat)
- GPT-4o-mini
- GPT-3.5-turbo

**Google Gemini**:
- Gemini 2.0 Flash
- Gemini 1.5 Pro
- Gemini 1.5 Flash

**Anthropic**:
- Claude 3.5 Sonnet
- Claude 3 Opus
- Claude 3 Haiku

### Default Model Selection

**Chat**: `gpt-4o`
**Embeddings**: `text-embedding-3-large`

**Example Request**:
```json
{
  "query": "How do I get started?",
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

### Custom Model Configuration

Use any OpenAI-compatible endpoint with custom model configuration.

**Example Request**:
```json
{
  "query": "Explain authentication",
  "llmOptions": {
    "customModel": {
      "modelId": "custom-llm-v1",
      "baseUrl": "https://api.example.com/v1",
      "apiKey": "sk-custom-key-123"
    }
  }
}
```

**Requirements**:
- OpenAI-compatible API format
- Streaming support
- Chat completion endpoint

**Use Cases**:
- Self-hosted models
- Fine-tuned models
- Alternative LLM providers

### Model Parameters

**Temperature**: Controls randomness (0.0 to 1.0)
- Lower values: More deterministic, focused responses
- Higher values: More creative, varied responses
- Default: 0.7

**Max Tokens**: Maximum response length
- Default: 2048
- Adjustable based on use case

**Example Request**:
```json
{
  "llmOptions": {
    "model": "gpt-4o",
    "temperature": 0.3,
    "maxTokens": 1024
  }
}
```

## API Endpoints

### POST /chat/conversationWithContext

Execute multi-turn conversation with documentation context.

**Request Headers**:
```
Content-Type: application/json
Authorization: Bearer <AI_TOKEN>
```

**Request Body**:
```json
{
  "query": "How do I authenticate API requests?",
  "subdomain": "my-docs",
  "history": [
    {
      "role": "user",
      "content": "What authentication methods do you support?"
    },
    {
      "role": "assistant",
      "content": "We support API key and OAuth 2.0 authentication."
    }
  ],
  "options": {
    "answerLength": "medium",
    "customTone": "professional",
    "forbiddenWords": ["legacy"]
  },
  "llmOptions": {
    "model": "gpt-4o",
    "temperature": 0.7
  }
}
```

**Response** (streaming):
```
data: {"type":"text-delta","textDelta":"To authenticate"}
data: {"type":"text-delta","textDelta":" API requests"}
data: {"type":"text-delta","textDelta":", include your"}
data: {"type":"text-delta","textDelta":" API key in"}
data: {"type":"text-delta","textDelta":" the Authorization"}
data: {"type":"text-delta","textDelta":" header..."}
data: {"type":"sources","sources":[{"title":"Authentication","url":"https://..."}]}
data: [DONE]
```

### POST /chat/withContext

Single-turn question answering with context.

**Request Body**:
```json
{
  "query": "What are rate limits?",
  "subdomain": "my-docs",
  "options": {
    "answerLength": "short"
  }
}
```

**Response**: Same streaming format as conversationWithContext.

### POST /chat/conversation

Multi-turn conversation without documentation context.

**Request Body**:
```json
{
  "query": "Continue the previous task",
  "history": [
    {
      "role": "user",
      "content": "Convert this to MDX"
    },
    {
      "role": "assistant",
      "content": "I'll help you convert that..."
    }
  ]
}
```

### POST /chat/agentChat

Advanced chat with tool-calling capabilities.

See [AI Agent documentation](./ai-agent.md) for details.

## CLI Usage

### Interactive Chat

Start an interactive chat session:

```bash
npm run cli:chat
```

**Features**:
- Multi-turn conversations
- Documentation context
- Source citations
- Real-time streaming

**Requirements**:
- `OPENAI_KEY` environment variable
- `GOOGLE_GENERATIVE_AI_API_KEY` environment variable
- Subdomain must be vectorized

**Example Session**:
```
> How do I create an API key?

To create an API key, navigate to your dashboard...

Sources:
- Authentication Guide (https://docs.example.com/auth)

> Can I set expiration dates?

Yes, you can set expiration dates when creating API keys...
```

## Best Practices

### Optimize Context Retrieval

**Vectorize Documentation**: Ensure all documentation is indexed:
```bash
npm run cli:vectorize index <subdomain>
```

**Update Regularly**: Re-vectorize when documentation changes to keep context current.

**Monitor Similarity Scores**: Check vector search results to ensure relevant content is being retrieved.

### Conversation Design

**Clear Initial Questions**: Start conversations with specific, well-formed questions for better context retrieval.

**Maintain Context**: Use conversation history to enable natural follow-up questions.

**Reset When Needed**: Start new conversations when switching topics to avoid context confusion.

### Customization Strategy

**Set Appropriate Tone**: Match tone to your audience (technical vs. beginner-friendly).

**Control Length**: Use shorter responses for quick answers, longer for tutorials.

**Filter Carefully**: Use forbidden words sparingly—over-filtering can reduce response quality.

### Model Selection

**Balance Cost and Quality**:
- Use GPT-4o for complex questions requiring deep understanding
- Use GPT-4o-mini for simpler queries to reduce costs
- Use Gemini Flash for high-volume, fast responses

**Test Different Models**: Evaluate model performance with your specific documentation and use cases.

## Troubleshooting

### No Context Found

**Symptom**: Responses like "I don't have enough information to answer that question."

**Causes**:
- Documentation not vectorized
- Similarity threshold too high
- Query too vague or off-topic

**Solutions**:
1. Vectorize documentation:
   ```bash
   npm run cli:vectorize index <subdomain>
   ```
2. Verify vector search results manually
3. Rephrase query to be more specific
4. Check if relevant documentation exists

### Poor Response Quality

**Symptom**: Inaccurate, irrelevant, or low-quality responses.

**Causes**:
- Wrong model selected
- Inappropriate customization options
- Insufficient context
- Poor documentation quality

**Solutions**:
1. Try a more capable model (e.g., GPT-4o instead of GPT-3.5)
2. Adjust temperature (lower for more focused responses)
3. Review and improve source documentation
4. Verify vector search is retrieving relevant content

### Slow Response Times

**Symptom**: Long delays before receiving responses.

**Causes**:
- Large context size
- Slow LLM provider
- Network latency

**Solutions**:
1. Reduce top-K documents retrieved
2. Use faster models (e.g., Gemini Flash, GPT-4o-mini)
3. Implement response caching for common queries
4. Check network connectivity

### Missing Sources

**Symptom**: Responses lack source citations.

**Causes**:
- Vector search returned no results
- Context assembly failed
- Source formatting issue

**Solutions**:
1. Verify documentation is vectorized
2. Check vector search similarity threshold
3. Review logs for errors in context assembly

## Performance Considerations

### Response Time Optimization

**Factors Affecting Speed**:
- Model selection (GPT-4o vs. GPT-4o-mini)
- Context size (number of documents retrieved)
- Query complexity
- LLM provider latency

**Optimization Strategies**:
- Use faster models for simple queries
- Reduce top-K documents when possible
- Implement caching for common questions
- Use streaming for better perceived performance

### Cost Management

**Cost Factors**:
- Model pricing (GPT-4o > GPT-4o-mini > Gemini Flash)
- Token usage (input + output)
- Request volume

**Cost Reduction**:
- Use cheaper models when appropriate
- Limit context size
- Implement response caching
- Set max token limits

### Scaling Considerations

**High-Volume Scenarios**:
- Implement rate limiting
- Use load balancing across LLM providers
- Cache frequent queries
- Monitor and optimize token usage

## Related Documentation

- [AI Agent](./ai-agent.md) - Advanced tool-calling capabilities
- [Vectorization](./vectorization.md) - Documentation indexing and search
- [Linting](./linting.md) - AI-powered content analysis
