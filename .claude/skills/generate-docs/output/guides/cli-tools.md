---
title: CLI Tools
slug: cli-tools
category:
  uri: Documentation
content:
  excerpt: Reference for all command-line interfaces including chat CLI, vectorization CLI, linting CLI, evaluation CLI, and MCP Inspector for testing.
---

# CLI Tools

Command-line interface tools for the ReadMe AI Service, including chat, vectorization, linting, evaluation, and MCP server inspection.

## Overview

The ReadMe AI Service provides several CLI tools for interacting with AI features, managing documentation vectors, evaluating content quality, and testing integrations. These tools are designed for developers, technical writers, and DevOps teams working with ReadMe's AI-powered documentation platform.

**Available CLI Tools:**

- **Chat CLI** - Interactive conversational AI for testing chat features
- **Vectorization CLI** - Index and manage documentation in vector databases
- **Linting CLI** - AI-powered content analysis and style checking
- **Evaluation CLI** - Test and benchmark AI service performance
- **MCP Inspector** - Debug and test Model Context Protocol integrations

## Prerequisites

### Required Environment Variables

Different CLI tools require different environment variables. Set these before running commands:

**For Chat CLI:**
```bash
OPENAI_KEY=your_openai_api_key
GOOGLE_GENERATIVE_AI_API_KEY=your_google_api_key
```

**For Vectorization CLI:**
```bash
AI_TOKEN=your_auth_token
README_DOMAIN=http://dash.readme.local:3000  # or production domain
AI_MONGO_URI=your_mongodb_atlas_connection_string
```

**For Linting CLI:**
```bash
OPENAI_KEY=your_openai_api_key
GOOGLE_GENERATIVE_AI_API_KEY=your_google_api_key
```

**For Evaluation CLI:**
```bash
OPENAI_KEY=your_openai_api_key
GOOGLE_GENERATIVE_AI_API_KEY=your_google_api_key
README_API_KEY=your_readme_api_key
AI_MONGO_URI=your_mongodb_atlas_connection_string
```

**For MCP Inspector:**
```bash
OPENAI_KEY=your_openai_api_key
GOOGLE_GENERATIVE_AI_API_KEY=your_google_api_key
```

### Database Setup

Most CLI tools require a MongoDB Atlas instance with vector search enabled. Regular MongoDB will not work.

**Options:**

1. **Use staging MongoDB** - Get connection string from 1Password
2. **Use your own MongoDB Atlas** - Set `AI_MONGO_URI` to your connection string
3. **Start local MongoDB Atlas container** - Run `./start-mongo.sh` (requires Docker)

**Initialize database (first-time setup only):**
```bash
npm run cli:vectorize initdb
```

## Chat CLI

Interactive conversational AI for testing chat functionality with your documentation.

### Usage

```bash
npm run cli:chat
```

### Requirements

- `OPENAI_KEY` - OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access
- MongoDB Atlas connection (for RAG features)
- Subdomain must be vectorized for best results

### Features

- Interactive chat session with AI
- Retrieval-Augmented Generation (RAG) using vectorized docs
- Multi-turn conversations with context
- Real-time streaming responses
- Source citations from documentation

### Example Session

```bash
$ npm run cli:chat

Welcome to AI Chat CLI
Type your questions (or 'exit' to quit)

> How do I authenticate API requests?

Searching documentation...
Found 5 relevant sources

Based on your documentation, you can authenticate API requests using an API key 
in the Authorization header:

Authorization: Bearer YOUR_API_KEY

Sources:
- Authentication Guide (https://docs.example.com/auth)
- API Reference (https://docs.example.com/api)

> exit
```

### Tips

- Vectorize your subdomain first: `npm run cli:vectorize index <subdomain>`
- Use specific questions for better results
- Check vector search results if answers seem off

## Vectorization CLI

Index documentation pages into a vector database for semantic search and RAG.

### Usage

**Initialize database:**
```bash
npm run cli:vectorize initdb
```

**Index a project:**
```bash
npm run cli:vectorize index <subdomain>
```

### Requirements

- `AI_TOKEN` - Authentication token
- `README_DOMAIN` - ReadMe domain URL
- `AI_MONGO_URI` - MongoDB Atlas connection string

### Commands

#### `initdb`

Creates required MongoDB collections and indexes. Run once per database instance.

```bash
npm run cli:vectorize initdb
```

**Creates:**
- `readme-ai-vector-collection` - Vector embeddings storage
- `vectorizeQueue` - Job queue for async processing
- Vector search indexes for similarity matching

**Note:** Only run on an empty database. Running on an existing database may cause errors.

#### `index <subdomain>`

Indexes all documentation for a subdomain into the vector database.

```bash
npm run cli:vectorize index developers
```

**Process:**
1. Fetches all guides and reference pages from ReadMe API
2. Splits content into chunks using RecursiveCharacterTextSplitter
3. Generates embeddings using OpenAI text-embedding-3-large (3072 dimensions)
4. Stores vectors in MongoDB Atlas with metadata
5. Creates vector search index for similarity queries

**Output:**
```
Fetching documentation...
Found 25 guides, 10 references
Creating vectorization jobs...
Vectorization started. Job count: 35
Processing chunks...
✓ Indexed 35 pages successfully
```

### How Vectorization Works

**Embedding Model:** OpenAI text-embedding-3-large
**Dimensions:** 3072
**Similarity Threshold:** 0.75
**Top-K Results:** 10 documents

**Process Flow:**
```
Documentation Pages
    ↓
Split into Chunks (RecursiveCharacterTextSplitter)
    ↓
Generate Content Hash (for change detection)
    ↓
Create Embeddings (OpenAI API)
    ↓
Store in MongoDB Atlas Vector Collection
    ↓
Available for Semantic Search
```

### Troubleshooting

**No search results:**
- Ensure documentation is vectorized: `npm run cli:vectorize index <subdomain>`
- Check MongoDB connection string is correct
- Verify vector search index exists in MongoDB Atlas

**Vectorization fails:**
- Check `AI_TOKEN` is valid
- Verify `README_DOMAIN` is accessible
- Ensure MongoDB Atlas (not regular MongoDB) is being used

## Linting CLI

AI-powered content analysis for markdown documentation, checking rule compliance and style consistency.

### Usage

```bash
npm run cli:lint <action> [prompt-file] [content-file-or-folder] [--hide-results] [--write-to-file]
```

### Requirements

- `OPENAI_KEY` - OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access

**Note:** CLI shows help without API keys, but requires them for actual linting.

### Actions

**`rules`** - Check content against custom rules
**`styleguide`** - Score adherence to style guidelines (0-10 scale)

### Arguments

- `prompt-file` - Path to rules or style guide file (markdown)
- `content-file-or-folder` - Path to content to analyze
- `--hide-results` - Suppress detailed output (optional)
- `--write-to-file` - Save results to JSONL file (optional)

### Examples

**Use default example files:**
```bash
npm run cli:lint rules
```

**Check custom rules:**
```bash
npm run cli:lint rules ./my-rules.md ./content/
```

**Check style guide compliance:**
```bash
npm run cli:lint styleguide ./style-guide.md ./docs/
```

**Hide detailed results:**
```bash
npm run cli:lint rules ./rules.md ./content/ --hide-results
```

**Write results to file:**
```bash
npm run cli:lint rules ./rules.md ./content/ --write-to-file
```

### Output Format

**Console Output:**
```
Analyzing content against rules...

File: getting-started.md
✓ No issues found

File: api-reference.md
⚠ 2 violations found:
  - Line 15: Use curly quotes instead of straight quotes
  - Line 42: Avoid using internal term 'hub'

Summary:
- Files analyzed: 2
- Total violations: 2
- Files with issues: 1
```

**JSONL Output (with `--write-to-file`):**
```jsonl
{"file":"getting-started.md","violations":[],"score":10}
{"file":"api-reference.md","violations":[{"line":15,"rule":"Smart Quotes","message":"Use curly quotes"},{"line":42,"rule":"Internal Lingo","message":"Avoid 'hub'"}],"score":8}
```

### Rule File Format

Rules should be written in markdown with clear descriptions:

```markdown
### Smart Quotes

Use curly quotes `"` `"` instead of straight quotes `"`.

### Internal Lingo

Don't use internal language like SuperHub, Dash, or Hub. Dashboard is okay.

### Em Dash Usage

Use em dash `—` like a semicolon, not hyphen `-`.
```

### Style Guide Format

Style guides should outline principles and guidelines:

```markdown
# Style Guide

Our style guide aims for simplicity and clarity.

## Principles

- Consistency and grammatical correctness are important, but not as important as clarity
- Focus on high-impact, high-value scenarios
- Be flexible and open to change while maintaining consistency

## Guidelines

### Contractions
Use contractions to keep pages short, unless the tone would be too casual.

### Emphasis
Use bold to emphasize important UI terms. Avoid overuse.
```

## Evaluation CLI

Test and benchmark AI service performance using evaluation datasets.

### Usage

**Create evaluation dataset:**
```bash
npm run create-evals <subdomain> [max_evals]
```

**Run evaluation:**
```bash
npm run eval <eval_file_path> <subdomain> [prod]
```

### Requirements

- `OPENAI_KEY` - OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access
- `README_API_KEY` - ReadMe API access
- `AI_MONGO_URI` - MongoDB Atlas connection string
- Subdomain must be vectorized

### Creating Evaluation Datasets

Generate evaluation questions and answers from vectorized documentation:

```bash
npm run create-evals developers 50
```

**Arguments:**
- `subdomain` - Subdomain to create evals for (must be vectorized)
- `max_evals` - Optional limit on number of evals (for testing)

**Output:**
- Creates file in `/evals/<subdomain>/groundtruths/`
- Format: `<subdomain>-evals-YYYY-MM-DD.json`

**Example:**
```bash
$ npm run create-evals docs-staging 50

Fetching vectorized chunks for docs-staging...
Found 1,234 chunks
Generating evaluation questions...
Created 50 evaluation pairs
Saved to: /evals/docs-staging/groundtruths/docs-staging-evals-2024-01-15.json
```

### Running Evaluations

Evaluate AI service performance against ground truth data:

```bash
# Evaluate local AI chat service
npm run eval ./evals/docs-staging/groundtruths/docs-staging-evals-2024-01-15.json docs-staging

# Evaluate production ReadMe chat API
npm run eval ./evals/docs-staging/groundtruths/docs-staging-evals-2024-01-15.json docs-staging prod
```

**Arguments:**
- `eval_file_path` - Path to evaluation JSON file
- `subdomain` - Subdomain being evaluated
- `prod` - Optional flag to evaluate production API instead of local service

**Output:**
- Saves results to `/evals/<subdomain>/results/`
- Format: `<ai|readme>-<subdomain>-YYYY-MM-DD.json`

### Evaluation Output

**Console Output:**
```
Running evaluation for docs-staging...
Progress: 50/50 questions

Results:
- Average score: 0.87
- Min score: 0.45
- Max score: 1.00
- Questions evaluated: 50

Saved to: /evals/docs-staging/results/ai-docs-staging-2024-01-15.json
```

**Result File Format:**
```json
{
  "question": "How do I authenticate API requests?",
  "expected_answer": "Use an API key in the Authorization header...",
  "ai_answer": "You can authenticate by including your API key...",
  "score": 0.92,
  "feedback": "Answer is accurate and includes correct header format"
}
```

**Scores:**
- `1.0` - Perfect match
- `0.8-0.9` - Very good, minor differences
- `0.6-0.7` - Acceptable, some inaccuracies
- `0.4-0.5` - Poor, significant issues
- `0.0-0.3` - Incorrect or irrelevant

### Evaluation Workflow

1. **Vectorize documentation:**
   ```bash
   npm run cli:vectorize index <subdomain>
   ```

2. **Create evaluation dataset:**
   ```bash
   npm run create-evals <subdomain> 100
   ```

3. **Run evaluation:**
   ```bash
   npm run eval ./evals/<subdomain>/groundtruths/<file>.json <subdomain>
   ```

4. **Review results:**
   - Check average scores
   - Identify low-scoring questions
   - Analyze feedback for improvements

## MCP Inspector

Debug and test Model Context Protocol (MCP) server integration.

### Usage

```bash
npm run inspect
```

### Requirements

- `OPENAI_KEY` - OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access
- Both ReadMe main repo and AI repo servers must be running

### Setup

**Terminal 1 - Start ReadMe server:**
```bash
cd readme
make start
```

**Terminal 2 - Start AI service:**
```bash
cd ai
npm run dev
```

**Terminal 3 - Run MCP Inspector:**
```bash
cd ai
npm run inspect
```

### Inspector Dashboard

The inspector launches at `http://localhost:6274` with a pre-filled authentication token.

**Output:**
```
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: 9cd052878105cd0eb06cc9300b25a394e85fd846c796a7d6702e88dfec3d8006

🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=9cd052878105cd0eb06cc9300b25a394e85fd846c796a7d6702e88dfec3d8006

🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

### Connecting to MCP Server

1. Navigate to the pre-filled URL in your browser
2. Set **Transport Type** to `Streamable HTTP`
3. Change URL to `http://<project-subdomain>.readme.local:9563/mcp`
4. Optional: Add `?branch=<branch-name>` for specific documentation branch
5. Open configuration panel and input proxy address (shown in terminal)
6. Click **Connect**
7. Verify tools list appears

**Example URLs:**
```
# Default (stable branch)
http://developers.readme.local:9563/mcp

# Specific branch
http://developers.readme.local:9563/mcp?branch=next

# Feature branch
http://project.readme.local:9563/mcp?branch=v2.0_myfeature
```

### Testing MCP Tools

Once connected, you can test available tools:

**Reference Page Tools:**
- `list-specs` - List API specifications
- `list-endpoints` - List endpoints in a spec
- `get-endpoint` - Get endpoint details
- `search-specs` - Search API specs
- `execute-request` - Execute API calls

**Guide Page Tools:**
- `search-guides` - Search documentation
- `fetch-guide` - Fetch guide content

### Troubleshooting

**Connection errors:**
- Verify both servers are running
- Check project subdomain exists
- Ensure MCP is enabled for the project
- Verify proxy address is correct

**No tools available:**
- Check project has API specs uploaded
- Verify branch exists (if using branch parameter)
- Ensure tools aren't disabled in project settings

**Authentication issues:**
- Use the pre-filled URL with token
- Check session token in terminal output
- Verify proxy server is listening

## Performance Expectations

**Command Timing (add 50% buffer for timeouts):**

- `npm install` - 40-60 seconds
- `npm run build` - 6-7 seconds
- `npm run lint` - 8-25 seconds
- `npm test` - 9-20 seconds
- `npm run cli:chat` - 2-5 seconds startup
- `npm run cli:vectorize index` - Varies by project size
- `npm run cli:lint` - 1-3 seconds per file
- `npm run inspect` - 2-3 seconds startup

**Important:** Never cancel long-running commands. Always set appropriate timeouts and wait for completion.

## Common Issues

### API Key Errors

**Symptom:** Server crashes immediately on startup

**Cause:** Missing required API keys

**Solution:** Set required environment variables before running commands:
```bash
export OPENAI_KEY=your_key
export GOOGLE_GENERATIVE_AI_API_KEY=your_key
```

### Database Connection Errors

**Symptom:** "Connection refused" or "Authentication failed"

**Cause:** Invalid MongoDB connection string or wrong database type

**Solution:**
- Verify `AI_MONGO_URI` is set correctly
- Ensure using MongoDB Atlas (not regular MongoDB)
- Check connection string format: `mongodb://...` or `mongodb+srv://...`

### Vectorization Fails

**Symptom:** "Failed to fetch documentation" or "No pages found"

**Cause:** Invalid subdomain or authentication issues

**Solution:**
- Verify subdomain exists in ReadMe
- Check `AI_TOKEN` matches between AI service and ReadMe
- Ensure `README_DOMAIN` is accessible

### Chat Returns No Context

**Symptom:** "I don't have enough information..."

**Cause:** Documentation not vectorized or similarity threshold too high

**Solution:**
1. Vectorize documentation: `npm run cli:vectorize index <subdomain>`
2. Check vector search results manually
3. Use more specific queries

### MCP Inspector Won't Connect

**Symptom:** Connection error in inspector dashboard

**Cause:** Servers not running or incorrect configuration

**Solution:**
1. Verify both ReadMe and AI servers are running
2. Check project subdomain in URL
3. Ensure proxy address matches terminal output
4. Verify project has MCP enabled

## Best Practices

### Before Running CLI Tools

1. **Set environment variables** - Check requirements for each tool
2. **Build the project** - Run `npm run build` after code changes
3. **Verify database connection** - Test MongoDB Atlas connectivity
4. **Check API keys** - Ensure all required keys are valid

### Vectorization

1. **Initialize database once** - Only run `initdb` on empty databases
2. **Vectorize before chat** - Always vectorize before using chat CLI
3. **Re-vectorize on updates** - Run `index` command when docs change
4. **Monitor progress** - Watch for errors during vectorization

### Linting

1. **Start with examples** - Use default files to understand output
2. **Iterate on rules** - Refine rules based on results
3. **Batch process** - Lint entire folders for consistency
4. **Review violations** - Don't auto-fix without review

### Evaluation

1. **Vectorize first** - Ensure documentation is indexed
2. **Create diverse evals** - Cover different question types
3. **Run regularly** - Track performance over time
4. **Compare environments** - Test both local and production

### MCP Inspector

1. **Start both servers** - ReadMe and AI service must run
2. **Use correct URLs** - Match project subdomain exactly
3. **Test incrementally** - Verify connection before testing tools
4. **Check logs** - Monitor terminal output for errors

## Additional Resources

- **Chat Documentation** - `docs/ask-ai-chat.md`
- **Vectorization Guide** - `docs/vectorization.md`
- **Linting Guide** - `docs/linting.md`
- **MCP Server Guide** - `docs/mcp-server.md`
- **Main README** - `README.md`

For technical support or questions, contact the ReadMe team or refer to the project documentation.
