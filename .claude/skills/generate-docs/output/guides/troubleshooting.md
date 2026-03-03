---
title: Troubleshooting
slug: troubleshooting
category:
  uri: Documentation
content:
  excerpt: Common issues and solutions including server startup problems, build failures, test failures, MCP integration issues, and performance expectations.
---

# Troubleshooting

This guide covers common issues you may encounter when working with the ReadMe AI Service and their solutions.

## Server Startup Problems

### Server Won't Start

**Symptom**: Server crashes immediately on startup or fails to initialize.

**Common Causes**:

1. **Missing API Keys**: The most common issue. The application requires `OPENAI_KEY` and `GOOGLE_GENERATIVE_AI_API_KEY` to be set.
2. **Invalid Node.js Version**: The application requires Node.js version 22.x.
3. **Port Already in Use**: Default port 9563 may be occupied by another process.
4. **Database Connection Issues**: MongoDB connection string may be invalid or database may be unreachable.

**Solutions**:

**For Missing API Keys**:

```bash
# Set required environment variables
export OPENAI_KEY=your_openai_key_here
export GOOGLE_GENERATIVE_AI_API_KEY=your_google_key_here

# For testing server startup only (not for actual use)
OPENAI_KEY=dummy GOOGLE_GENERATIVE_AI_API_KEY=dummy npm start
```

**For Node.js Version Issues**:

```bash
# Check your Node.js version
node --version

# Should output v22.x.x
# If not, install Node.js 22.x using nvm or your package manager
nvm install 22
nvm use 22
```

**For Port Conflicts**:

```bash
# Use a different port
PORT=9564 npm start

# Or find and kill the process using port 9563
lsof -ti:9563 | xargs kill -9
```

**For Database Connection Issues**:

```bash
# Verify MongoDB connection string is set
echo $AI_MONGO_URI

# If empty or invalid, set it to staging or your local instance
export AI_MONGO_URI="mongodb://your-connection-string"

# For local development without database features
export AI_MONGO_URI=""
```

### Server Starts But Crashes During Operation

**Symptom**: Server starts successfully but crashes when handling requests.

**Common Causes**:

1. **Invalid Environment Configuration**: Missing or incorrectly formatted environment variables.
2. **Database Connection Lost**: MongoDB Atlas connection dropped or timed out.
3. **API Rate Limits**: Exceeded rate limits on OpenAI or Google APIs.

**Solutions**:

**Check Environment Variables**:

```bash
# Verify all required variables are set
echo $OPENAI_KEY
echo $GOOGLE_GENERATIVE_AI_API_KEY
echo $AI_TOKEN
echo $README_DOMAIN
```

**Monitor Database Connection**:

- Check MongoDB Atlas dashboard for connection issues
- Verify IP whitelist includes your current IP
- Ensure connection string includes correct credentials

**Monitor API Usage**:

- Check OpenAI dashboard for rate limit status
- Review Google Cloud Console for API quota
- Implement exponential backoff in your requests

---

## Build Failures

### Build Command Fails

**Symptom**: `npm run build` exits with errors.

**Common Causes**:

1. **TypeScript Compilation Errors**: Type errors in the codebase.
2. **Missing Dependencies**: Node modules not installed or corrupted.
3. **Outdated Dependencies**: Package versions incompatible with current code.

**Solutions**:

**For TypeScript Errors**:

```bash
# Run TypeScript compiler to see detailed errors
npx tsc --noEmit

# Fix type errors in reported files
# Common issues:
# - Missing type imports
# - Incorrect type annotations
# - Unused variables or imports
```

**For Dependency Issues**:

```bash
# Clean install dependencies
rm -rf node_modules package-lock.json
npm install

# Verify Node.js version matches requirements
node --version  # Should be 22.x

# If issues persist, clear npm cache
npm cache clean --force
npm install
```

**For Build Timeout**:

```bash
# Increase timeout for slow systems
# Build typically takes 6-7 seconds
# Allow 15-20 seconds for slower systems
timeout 20s npm run build
```

### Linting Failures

**Symptom**: `npm run lint` reports errors.

**Common Causes**:

1. **Code Style Violations**: Code doesn't match Biome configuration.
2. **Formatting Issues**: Prettier formatting not applied.
3. **Type Errors**: TypeScript strict mode violations.

**Solutions**:

```bash
# Auto-fix most linting issues
npm run lint:fix

# Check specific file
npx biome check path/to/file.ts

# Format code
npx biome format --write .

# If errors persist, review biome.jsonc configuration
cat biome.jsonc
```

---

## Test Failures

### Unit Tests Fail

**Symptom**: `npm test` reports failing tests.

**Common Causes**:

1. **Environment Variables**: Tests expect certain environment setup.
2. **Mock Configuration**: Mocks not properly configured for test scenarios.
3. **Timing Issues**: Async operations timing out or racing.

**Solutions**:

**Run Individual Test Files**:

```bash
# Run specific test file to isolate issue
npm test -- src/ai/chat/__tests__/chat.test.ts

# Run tests in watch mode for debugging
npm test -- --watch

# Run with verbose output
npm test -- --reporter=verbose
```

**Check Test Environment**:

```bash
# Tests should run without API keys
# Verify mocks are working correctly
# Check test files in __tests__ directories
```

**For Timeout Issues**:

```bash
# Increase test timeout in vitest.config.ts
# Default timeout is usually sufficient
# Check for infinite loops or hanging promises
```

### Integration Tests Fail

**Symptom**: `npm run test:integration` fails.

**Common Causes**:

1. **Missing Environment Variables**: Integration tests require live service credentials.
2. **Service Unavailable**: External services (ReadMe, MongoDB) unreachable.
3. **Test Data Conflicts**: Previous test runs left stale data.

**Solutions**:

**Set Required Environment Variables**:

```bash
# For local testing
export README_API_KEY=your_api_key
export AI_TOKEN=secret
export README_DOMAIN=http://dash.readme.local:3000
export AI_SERVER_URL=http://localhost:9563

# For staging testing
export README_DOMAIN=https://dash.readmestaging.com
export AI_SERVER_URL=https://readme-ai-stage.onrender.com
```

**Verify Service Availability**:

```bash
# Check ReadMe service
curl $README_DOMAIN/api/health

# Check AI service
curl $AI_SERVER_URL/health

# Check MongoDB connection
# Use MongoDB Compass or mongosh to verify
```

**Clean Test Data**:

- Integration tests should clean up after themselves
- Check for orphaned test documents in MongoDB
- Verify test uses random IDs to avoid conflicts

---

## MCP Integration Issues

### MCP Server Not Responding

**Symptom**: MCP Inspector shows connection errors or timeout.

**Common Causes**:

1. **Server Not Running**: AI service or ReadMe main server not started.
2. **Incorrect URL**: MCP endpoint URL misconfigured.
3. **Missing Host Header**: Project identification failing.
4. **Authentication Issues**: API tokens not properly configured.

**Solutions**:

**Verify Both Servers Running**:

```bash
# Terminal 1: Start ReadMe main server
cd readme && make start

# Terminal 2: Start AI service
cd ai && npm run dev

# Terminal 3: Start MCP Inspector
cd ai && npm run inspect
```

**Check MCP Endpoint**:

```bash
# Test MCP endpoint directly
curl -X POST http://my-docs.readme.local:9563/mcp \
  -H "x-forwarded-host: my-docs.readme.local:3000" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

**Verify Host Header**:

- MCP Inspector should set URL to: `http://<subdomain>.readme.local:9563/mcp`
- Check proxy address in inspector configuration
- Ensure project exists and has MCP enabled

**Test with Branch Parameter**:

```bash
# Connect to specific branch
http://my-docs.readme.local:9563/mcp?branch=next

# Verify branch exists in ReadMe project
```

### Tools Not Available

**Symptom**: Expected tools missing from MCP tools list.

**Common Causes**:

1. **Tools Disabled**: Project settings disable specific tools.
2. **No API Specs**: Reference page tools require OpenAPI specs.
3. **Cache Issues**: Stale cache returning old tool list.
4. **Branch Mismatch**: Different branches have different specs.

**Solutions**:

**Check Project Configuration**:

- Verify API specs uploaded to ReadMe project
- Check `disabled_tools` in project settings
- Ensure MCP feature enabled for project

**Clear Cache**:

```bash
# Cache key format: readme:getInfo:<host>:<branch>
# Clear specific cache entry in Redis or MongoDB
# Or restart AI service to clear in-memory cache
```

**Verify Spec Availability**:

```bash
# Check if specs returned in project info
curl -X POST $README_DOMAIN/api-next/v2/mcp/info \
  -H "Authorization: Bearer $AI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"subdomain":"my-docs","branch":"stable"}'
```

### MCP Connection Drops

**Symptom**: MCP connection works initially but disconnects.

**Common Causes**:

1. **Timeout Issues**: Long-running operations timing out.
2. **Memory Issues**: Server running out of memory.
3. **Network Issues**: Connection interrupted.

**Solutions**:

**Monitor Server Resources**:

```bash
# Check memory usage
node --max-old-space-size=4096 src/server.ts

# Monitor process
top -p $(pgrep -f "node.*server.ts")
```

**Check Server Logs**:

- Look for timeout errors
- Check for memory warnings
- Review connection error messages

**Restart Services**:

```bash
# Restart AI service
npm run dev

# Restart MCP Inspector
npm run inspect
```

---

## Performance Expectations

### Command Timing Guidelines

Understanding expected execution times helps identify performance issues:

**Build and Development Commands**:

| Command | Expected Time | Timeout Recommendation |
|---------|---------------|------------------------|
| `npm install` | 40-60 seconds | 120 seconds |
| `npm run build` | 6-7 seconds | 15 seconds |
| `npm run lint` | 8-25 seconds | 60 seconds |
| `npm test` | 9-20 seconds | 60 seconds |
| Complete workflow | 25-45 seconds | 120 seconds |

**Server Operations**:

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Server startup | 2-5 seconds | With valid environment |
| MCP connection | 1-3 seconds | First connection may be slower |
| Vector search | 100-500ms | Depends on query complexity |
| Chat response | 2-10 seconds | Streaming starts immediately |

**Important Notes**:

- **Never cancel long-running commands** - Always wait for completion
- Add 50% buffer to timeouts for slower systems
- First-time operations (cache warming) take longer
- Linting is faster after first run due to caching

### Slow Performance

**Symptom**: Operations taking significantly longer than expected.

**Common Causes**:

1. **System Resources**: Insufficient CPU or memory.
2. **Network Latency**: Slow connection to external APIs.
3. **Database Performance**: MongoDB queries slow or timing out.
4. **Large Context**: Processing very large documents or conversations.

**Solutions**:

**Optimize System Resources**:

```bash
# Increase Node.js memory limit
node --max-old-space-size=4096 src/server.ts

# Close unnecessary applications
# Ensure adequate disk space
df -h
```

**Monitor Network Performance**:

```bash
# Test API latency
time curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_KEY"

# Check MongoDB connection speed
# Use MongoDB Compass connection diagnostics
```

**Optimize Database Queries**:

- Ensure vector search indexes exist
- Check MongoDB Atlas performance metrics
- Review slow query logs
- Consider upgrading MongoDB tier

**Reduce Context Size**:

- Limit conversation history length
- Reduce number of retrieved documents
- Use shorter prompts when possible

---

## CLI Tool Issues

### Chat CLI Not Working

**Symptom**: `npm run cli:chat` fails or produces errors.

**Solutions**:

```bash
# Ensure API keys are set
export OPENAI_KEY=your_key
export GOOGLE_GENERATIVE_AI_API_KEY=your_key

# Verify subdomain is vectorized
npm run cli:vectorize index <subdomain>

# Check database connection
echo $AI_MONGO_URI
```

### Vectorization CLI Fails

**Symptom**: `npm run cli:vectorize index <subdomain>` fails.

**Solutions**:

```bash
# Verify environment variables
export AI_TOKEN=secret
export README_DOMAIN=http://dash.readme.local:3000

# Check ReadMe service is running
curl $README_DOMAIN/api/health

# Verify database connection
# MongoDB Atlas must be accessible

# Initialize database if first time
npm run cli:vectorize initdb
```

### Linting CLI Issues

**Symptom**: `npm run cli:lint` produces unexpected results.

**Solutions**:

```bash
# View help and usage
npm run cli:lint

# Test with example files
npm run cli:lint rules

# Verify API keys for actual processing
export OPENAI_KEY=your_key
export GOOGLE_GENERATIVE_AI_API_KEY=your_key
```

---

## Getting Help

If you encounter issues not covered in this guide:

1. **Check Server Logs**: Review console output for error messages
2. **Search Documentation**: Look through other docs in `/docs` directory
3. **Review GitHub Issues**: Check for similar reported issues
4. **Contact Team**: Reach out via internal support channels
5. **Check Status Pages**: Verify external service status (OpenAI, MongoDB Atlas)

### Useful Debugging Commands

```bash
# Check all environment variables
env | grep -E 'OPENAI|GOOGLE|AI_|README'

# Verify server health
curl http://localhost:9563/health

# Test MCP endpoint
curl -X POST http://localhost:9563/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Check Node.js and npm versions
node --version
npm --version

# View recent logs
tail -f logs/server.log  # If logging to file
```

### Pre-Commit Checklist

Before committing changes, always run:

```bash
# Complete validation workflow
npm run build && npm run lint && npm test

# Should complete in 25-45 seconds
# All checks must pass before committing
```
