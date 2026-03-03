---
title: Getting Started
slug: getting-started
category:
  uri: Documentation
content:
  excerpt: Step-by-step guide to setting up the AI service locally, including prerequisites (Node.js 22.x, API keys), installation, building, and running the development server.
---

# Getting Started

This guide will walk you through setting up the ReadMe AI Service locally, from installing prerequisites to running your first development server.

## Overview

The ReadMe AI Service is a Node.js TypeScript application that powers AI features in ReadMe. It runs an MCP (Model Context Protocol) server and serves as a proxy to AI models (OpenAI, Google Gemini) for chat, vectorization, and content evaluation features.

**What you'll accomplish:**

- Install required dependencies
- Configure API keys and environment variables
- Build the project
- Start the development server
- Verify your setup is working

**Time to complete:** 10-15 minutes

---

## Prerequisites

Before you begin, ensure you have the following installed and configured:

### Node.js 22.x

The AI service requires Node.js version 22.x (enforced by `engines` in `package.json`).

**Check your Node.js version:**

```bash
node --version
```

**Expected output:**

```
v22.x.x
```

If you need to install or upgrade Node.js, download it from [nodejs.org](https://nodejs.org/) or use a version manager like [nvm](https://github.com/nvm-sh/nvm):

```bash
nvm install 22
nvm use 22
```

### API Keys

You'll need API keys to access AI models. Obtain these from your team or the appropriate service providers:

**Required for full functionality:**

- `OPENAI_KEY` - OpenAI API access (required for chat and vectorization)
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access

**Optional but recommended:**

- `AI_TOKEN` - Authentication token for AI service (default: `"secret"`)
- `README_DOMAIN` - ReadMe domain for integration (default: `http://dash.readme.local:3000`)

> **Warning:** The application will crash immediately if required API keys are not set when importing AI modules.

**For testing server startup only**, you can use dummy values:

```bash
OPENAI_KEY=dummy GOOGLE_GENERATIVE_AI_API_KEY=dummy npm start
```

### Database (Optional)

For vector search and chat features, you'll need a MongoDB Atlas instance. By default, the MongoDB connection string is set to an empty string (`""`), which allows the server to start but database operations will fail.

**Options:**

- **Run without MongoDB:** Fine if you're not using database features
- **Use staging MongoDB:** Get connection string from 1Password
- **Use your own MongoDB Atlas:** Set `AI_MONGO_URI` to your connection string
- **Start local MongoDB Atlas container:** Run `./start-mongo.sh` (requires Docker)

See the main README for detailed database setup instructions.

---

## Installation

### 1. Clone the Repository

If you haven't already, clone the AI service repository:

```bash
git clone <repository-url>
cd ai
```

### 2. Install Dependencies

Install all required Node.js packages:

```bash
npm install
```

**Expected duration:** 40-60 seconds

> **Important:** Never cancel this command. Set your timeout to 120+ seconds and wait for completion.

**What this does:**

- Installs all dependencies listed in `package.json`
- Sets up TypeScript, testing frameworks, and build tools
- Prepares the project for development

---

## Configuration

### Set Environment Variables

Create a `.env` file in the project root or set environment variables in your shell:

**Minimum configuration for testing:**

```bash
# .env
OPENAI_KEY=your_openai_api_key_here
GOOGLE_GENERATIVE_AI_API_KEY=your_google_api_key_here
AI_TOKEN=secret
```

**Full configuration example:**

```bash
# .env
OPENAI_KEY=sk-...
GOOGLE_GENERATIVE_AI_API_KEY=...
AI_TOKEN=secret
README_DOMAIN=http://dash.readme.local:3000
AI_SERVER_URL=http://localhost:9563
AI_MONGO_URI=mongodb://127.0.0.1:27017
PORT=9563
```

**Configuration notes:**

- All environment variables are defined in `config/custom-environment-variables.json`
- Not all variables are required; defaults are provided for many
- See `config/default.json` for default values

---

## Building the Project

Build the TypeScript project to JavaScript:

```bash
npm run build
```

**Expected duration:** 6-7 seconds

> **Important:** Never cancel this command. Wait for completion.

**What this does:**

- Compiles TypeScript files from `/src` to JavaScript in `/dist`
- Performs type checking
- Generates source maps for debugging

**Expected output:**

```
> ai@1.0.0 build
> tsc
```

If you see TypeScript errors, resolve them before proceeding. Run `npm run lint` to check for code issues.

---

## Running the Development Server

### Start in Development Mode

Start the server with hot reload for development:

```bash
npm run dev
```

**What this does:**

- Starts TypeScript watch mode
- Runs nodemon for automatic restarts on file changes
- Starts the server on port 9563 (configurable via `PORT` environment variable)

**Expected output:**

```
[nodemon] starting `node dist/server.js`
Server listening on port 9563
MCP server initialized
```

**Server startup time:** 2-5 seconds (with valid environment)

### Start in Production Mode

To run the compiled application without hot reload:

```bash
npm start
```

This runs the built JavaScript files from `/dist` without watching for changes.

---

## Verifying Your Setup

### 1. Check Server Health

Once the server is running, verify it's responding:

```bash
curl http://localhost:9563/health
```

**Expected response:**

```json
{
  "status": "ok"
}
```

### 2. Test MCP Endpoint

Test the MCP server connection:

```bash
curl -X POST http://localhost:9563/mcp \
  -H "Content-Type: application/json" \
  -H "x-forwarded-host: your-project.readme.local:3000" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

This should return a list of available MCP tools.

### 3. Run Tests

Verify the installation by running the test suite:

```bash
npm test
```

**Expected duration:** 10-20 seconds

> **Important:** Never cancel this command. Wait for completion.

**Expected output:**

```
 ✓ src/ai/__tests__/... (54 tests)

Test Files  8 passed (8)
     Tests  54 passed (54)
```

Tests run successfully without API keys, as external dependencies are mocked.

### 4. Run Linting

Check code quality and formatting:

```bash
npm run lint
```

**Expected duration:** 12-25 seconds (faster after first run due to caching)

**What this checks:**

- TypeScript type errors
- Code formatting (Prettier + Biome)
- Code quality issues

**Expected output:**

```
✔ No linting errors found
```

---

## Next Steps

Now that your development environment is set up, you can:

### Explore CLI Tools

**Chat CLI** - Interactive conversational AI:

```bash
npm run cli:chat
```

**Vectorization CLI** - Index documentation:

```bash
npm run cli:vectorize index <subdomain>
```

**Linting CLI** - Analyze content:

```bash
npm run cli:lint rules
```

See the main README for detailed CLI usage.

### Test MCP Integration

For full MCP testing with the ReadMe main application:

1. Start the ReadMe main server (separate repository)
2. Keep the AI service running
3. Launch MCP Inspector:

```bash
npm run inspect
```

4. Navigate to `http://localhost:6274` to test the MCP protocol implementation

### Make Your First Changes

1. Create a new branch for your work
2. Make changes to TypeScript files in `/src`
3. The dev server will automatically reload
4. Run tests: `npm test`
5. Run linting: `npm run lint`
6. Commit your changes

---

## Troubleshooting

### Server Won't Start

**Problem:** Server crashes on startup

**Common causes:**

- Missing `OPENAI_KEY` environment variable
- Invalid API keys
- Port 9563 already in use

**Solutions:**

1. Verify all required environment variables are set
2. Check API key validity
3. Change the port: `PORT=9564 npm run dev`
4. Verify Node.js version is 22.x: `node --version`

### Build Failures

**Problem:** TypeScript compilation errors

**Solutions:**

1. Run `npm run lint` to identify issues
2. Check for TypeScript errors in your code
3. Ensure all dependencies are installed: `npm install`
4. Clear build cache: `rm -rf dist && npm run build`

### Test Failures

**Problem:** Tests fail when running `npm test`

**Solutions:**

1. Run individual test files to isolate issues:
   ```bash
   npm test src/ai/__tests__/specific-test.test.ts
   ```
2. Check if tests require specific environment setup
3. Verify mock configurations in test files
4. Ensure you're on the correct Node.js version

### Database Connection Issues

**Problem:** MongoDB connection errors

**Solutions:**

1. Verify `AI_MONGO_URI` is set correctly
2. Check MongoDB Atlas instance is running
3. Ensure network access is configured in MongoDB Atlas
4. Test connection string separately
5. For local development, you can run without MongoDB (database operations will fail but server will start)

---

## Performance Expectations

When running commands, expect these durations (add 50% buffer for timeouts):

| Command | Expected Duration |
|---------|-------------------|
| `npm install` | 40-60 seconds |
| `npm run build` | 6-7 seconds |
| `npm run lint` | 12-25 seconds |
| `npm test` | 10-20 seconds |
| Complete workflow (`build && lint && test`) | 25-45 seconds |
| Server startup | 2-5 seconds |

**Critical reminder:** Never cancel long-running commands. Always set appropriate timeouts and wait for completion.

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the main README for detailed documentation
2. Review the `.github/copilot-instructions.md` for development guidelines
3. Search existing issues in the repository
4. Contact the team for API key access
5. Consult the documentation in `/docs` for specific features

---

## Summary

You've successfully:

- ✅ Installed Node.js 22.x
- ✅ Obtained and configured API keys
- ✅ Installed project dependencies
- ✅ Built the TypeScript project
- ✅ Started the development server
- ✅ Verified your setup with tests

You're now ready to develop AI features for ReadMe. Happy coding!
