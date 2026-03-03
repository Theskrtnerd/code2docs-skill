---
title: Development Workflow
slug: development-workflow
category:
  uri: Documentation
content:
  excerpt: Best practices for making changes to AI services, adding dependencies, managing the build process, and ensuring code quality through linting and testing.
---

# Development Workflow

Best practices for making changes to AI services, adding dependencies, managing the build process, and ensuring code quality through linting and testing.

## Overview

This guide covers the essential workflow for developing features, fixing bugs, and maintaining code quality in the ReadMe AI Service. Following these practices ensures consistency, reliability, and smooth collaboration across the team.

**Key Principles**:

- Always validate changes with the complete build pipeline before committing
- Never cancel long-running commands—set appropriate timeouts
- Test both unit and integration scenarios when making changes
- Maintain strict type safety and follow TypeScript best practices

## Before You Start

### Required Environment Setup

Ensure you have the following configured:

**Node.js Version**: 22.x (enforced by package.json)

**Required API Keys** (for full functionality):
- `OPENAI_KEY` - OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY` - Google Gemini API access

**Optional but Recommended**:
- `AI_TOKEN` - Authentication token (default: "secret")
- `README_DOMAIN` - ReadMe domain for integration testing
- `AI_MONGO_URI` - MongoDB Atlas connection string

**Database Setup**:
- MongoDB Atlas instance with vector search enabled
- Regular MongoDB will not work—Atlas is required for vector operations
- See main README.md for database initialization instructions

### Performance Expectations

Set timeouts appropriately for all commands:

- `npm install`: 40-60 seconds
- `npm run build`: 6-7 seconds
- `npm run lint`: 8-25 seconds (faster after first run due to caching)
- `npm test`: 9-20 seconds
- Complete workflow (`build && lint && test`): 25-45 seconds total

**Critical**: Add 50% buffer to these times for slower systems. Never cancel commands prematurely.

## Making Changes

### 1. Initial Setup

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd ai
npm install  # Wait 40-60 seconds, do not cancel
```

### 2. Development Workflow

Start the development server with hot reload:

```bash
npm run dev
```

This runs TypeScript watch mode with nodemon for automatic reloading on file changes.

**Making Code Changes**:

1. Edit files in `/src/` directory
2. Changes automatically trigger rebuild and server restart
3. Check terminal for TypeScript errors or warnings
4. Test changes using CLI tools or MCP Inspector

### 3. TypeScript Best Practices

Follow strict type safety guidelines:

**Use Explicit Types**:
```typescript
// Good: Explicit type annotation
function processUser(user: User): UserResult {
  return { id: user.id, name: user.name };
}

// Avoid: Implicit any
function processUser(user) {
  return { id: user.id, name: user.name };
}
```

**Type Imports**:
```typescript
// Good: Type-only import
import type { LLMOptions } from '../types.js';

// Avoid: Mixed import when only types are needed
import { LLMOptions } from '../types.js';
```

**Interface for Complex Parameters**:
```typescript
// Good: Interface for 3+ properties
interface CreateUserArgs {
  email: string;
  name: string;
  role: string;
}

function createUser(args: CreateUserArgs): User {
  // implementation
}

// Acceptable: Inline for 2 or fewer properties
function updateEmail(userId: string, email: string): void {
  // implementation
}
```

**Prefer Unknown Over Any**:
```typescript
// Good: Unknown forces type checking
function parseData(data: unknown): ParsedData {
  if (typeof data === 'object' && data !== null) {
    // Type narrowing
  }
}

// Avoid: Any bypasses type safety
function parseData(data: any): ParsedData {
  // No type safety
}
```

### 4. Adding Dependencies

When adding new packages:

```bash
# Install the package
npm install <package-name>

# Rebuild to ensure compatibility
npm run build

# Run tests to verify nothing broke
npm test

# Run linting to catch any issues
npm run lint
```

**Verify the dependency**:
- Check that it's compatible with Node.js 22.x
- Review its TypeScript type definitions
- Ensure it doesn't conflict with existing dependencies

### 5. Modifying AI Services

When changing core AI functionality:

**Chat Service** (`/src/ai/chat/`):
1. Update implementation in `chat.ts` or `agent.ts`
2. Test with CLI: `npm run cli:chat`
3. Verify streaming responses work correctly
4. Test with different LLM providers (OpenAI, Google)

**Vectorization** (`/src/ai/vectorize/`):
1. Update vectorization logic
2. Test with CLI: `npm run cli:vectorize index <subdomain>`
3. Verify vector search results are accurate
4. Check MongoDB Atlas indexes are used correctly

**Linting** (`/src/ai/lint/`):
1. Update linting rules or prompts
2. Test with CLI: `npm run cli:lint rules`
3. Verify structured output matches schema
4. Test with multiple content files

**MCP Server** (`/src/mcp/`):
1. Update tool definitions or server logic
2. Test with MCP Inspector: `npm run inspect`
3. Verify tool registration works correctly
4. Test with actual MCP clients (Cursor, Claude Desktop)

## Build Process

### Running the Build

Build the TypeScript project:

```bash
npm run build  # Wait 6-7 seconds, do not cancel
```

**What happens during build**:
- TypeScript files compiled to JavaScript
- Type checking performed
- Output written to `/dist/` directory
- Source maps generated for debugging

**Common Build Errors**:

**TypeScript Errors**:
```
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'
```
Fix: Correct the type mismatch in your code

**Missing Type Definitions**:
```
error TS7016: Could not find a declaration file for module 'some-package'
```
Fix: Install `@types/some-package` or add type declarations

**Import Path Errors**:
```
error TS2307: Cannot find module './types.js'
```
Fix: Ensure `.js` extension is included in TypeScript imports

## Code Quality

### Linting

Run the linter to check code quality:

```bash
npm run lint  # Wait 8-25 seconds, do not cancel
```

**What the linter checks**:
- Code formatting (Prettier + Biome)
- TypeScript type errors
- Code style violations
- Import organization

**Fixing Lint Errors**:

Most formatting issues can be auto-fixed:
```bash
npm run lint:fix
```

**Common Lint Errors**:

**Formatting Issues**:
```
[error] Code style issues found
```
Fix: Run `npm run lint:fix`

**Unused Variables**:
```
'variable' is declared but never used
```
Fix: Remove the variable or prefix with underscore: `_variable`

**Missing Return Types**:
```
Missing return type on function
```
Fix: Add explicit return type annotation

### Required Pre-Commit Validation

**Always run before committing**:

```bash
npm run lint
```

This ensures:
- Code is properly formatted
- No TypeScript errors exist
- Code style is consistent
- CI pipeline will pass

**CI will fail** if linting errors exist, so fix them locally first.

## Testing

### Unit Tests

Run the test suite:

```bash
npm test  # Wait 10-20 seconds, do not cancel
```

**Test Coverage**:
- 54 tests across 8 files
- Core functionality coverage
- Tests run successfully without API keys

**Writing Tests**:

Tests should focus on business logic, not HTTP layer:

```typescript
// Good: Test business logic
describe('vectorize', () => {
  it('should chunk content correctly', () => {
    const chunks = chunkContent(longText, 1000);
    expect(chunks.length).toBeGreaterThan(1);
  });
});

// Avoid: Testing HTTP in unit tests
describe('vectorize', () => {
  it('should return 200', async () => {
    const response = await fetch('/vectorize');
    expect(response.status).toBe(200);
  });
});
```

**Test Location**:
- Unit tests: `/src/**/__tests__/` (test business logic)
- Integration tests: `/src/aiClient/__tests__/` (test HTTP layer)

### Integration Tests

Test against live external services:

```bash
npm run test:integration
```

**Required Environment Variables**:
- `README_API_KEY` - ReadMe API access token
- `AI_TOKEN` - AI service authentication
- `README_DOMAIN` - ReadMe service URL
- `AI_SERVER_URL` - AI service URL

**Integration Test Guidelines**:
- Use random IDs to avoid conflicts
- Clean up after each test
- Test high-value scenarios only
- Keep test count minimal

### Manual Testing Scenarios

**After making changes, always test**:

**1. Build Validation**:
```bash
npm run build && npm run lint && npm test
```

**2. MCP Server Testing** (requires API keys):
```bash
# Terminal 1: Start AI service
npm run dev

# Terminal 2: Start ReadMe main server (separate repo)
cd ../readme && make start

# Terminal 3: Run MCP Inspector
npm run inspect
# Navigate to http://localhost:6274
# Test connection with project subdomain URL
```

**3. CLI Tool Validation**:
```bash
# Test help output (no API keys needed)
npm run cli:lint

# Test with API keys
npm run cli:chat
npm run cli:vectorize index <subdomain>
npm run cli:lint rules ./fixtures/example-rules-errors.md ./fixtures/example-content.md
```

**4. Server Startup**:
```bash
# With dummy keys (test startup only)
OPENAI_KEY=dummy GOOGLE_GENERATIVE_AI_API_KEY=dummy npm start

# With real keys (full functionality)
npm start
```

## Common Development Tasks

### Adding a New AI Feature

1. **Create feature files** in appropriate directory (`/src/ai/chat/`, `/src/ai/vectorize/`, etc.)
2. **Add route handler** in `/src/routes/operations/`
3. **Register route** in `/src/server.ts`
4. **Add types** in feature's `types.ts` file
5. **Write tests** in `__tests__/` directory
6. **Update documentation** in `/docs/`
7. **Test with CLI** if applicable
8. **Validate complete workflow**:
   ```bash
   npm run build && npm run lint && npm test
   ```

### Modifying MCP Tools

1. **Update tool definition** in `/src/mcp/tools/`
2. **Test with MCP Inspector**:
   ```bash
   npm run inspect
   ```
3. **Verify tool registration** in inspector dashboard
4. **Test with actual MCP client** (Cursor, Claude Desktop)
5. **Update documentation** in `/docs/mcp-server.md`

### Changing Database Schema

1. **Update MongoDB model** in `/src/models/`
2. **Create migration script** if needed
3. **Test with local MongoDB Atlas instance**
4. **Update vector indexes** if necessary
5. **Run integration tests**:
   ```bash
   npm run test:integration
   ```

### Updating Dependencies

1. **Check for updates**:
   ```bash
   npm outdated
   ```
2. **Update specific package**:
   ```bash
   npm update <package-name>
   ```
3. **Test thoroughly**:
   ```bash
   npm run build && npm run lint && npm test
   ```
4. **Check for breaking changes** in package changelog
5. **Update code** if API changes occurred

## Troubleshooting

### Server Won't Start

**Symptom**: Server crashes immediately on startup

**Common Causes**:
- Missing `OPENAI_KEY` environment variable
- Missing `GOOGLE_GENERATIVE_AI_API_KEY`
- Invalid MongoDB connection string
- Port 9563 already in use

**Solutions**:
1. Verify all required environment variables are set
2. Check Node.js version is 22.x: `node --version`
3. Use dummy keys for startup testing:
   ```bash
   OPENAI_KEY=dummy GOOGLE_GENERATIVE_AI_API_KEY=dummy npm start
   ```
4. Check if port is in use: `lsof -i :9563`

### Build Failures

**Symptom**: `npm run build` fails with errors

**Solutions**:
1. Run linter to check for issues:
   ```bash
   npm run lint
   ```
2. Check for TypeScript errors in terminal output
3. Verify all imports use `.js` extension
4. Ensure all type definitions are available
5. Clear build cache and rebuild:
   ```bash
   rm -rf dist/
   npm run build
   ```

### Test Failures

**Symptom**: Tests fail unexpectedly

**Solutions**:
1. Run individual test files to isolate issues:
   ```bash
   npm test -- path/to/test.test.ts
   ```
2. Check if tests require specific environment setup
3. Verify mock configurations in test files
4. Ensure test database is properly initialized
5. Check for race conditions in async tests

### MCP Integration Issues

**Symptom**: MCP Inspector can't connect or tools don't appear

**Solutions**:
1. Ensure both ReadMe and AI servers are running
2. Check MCP Inspector connection settings
3. Verify authentication tokens match
4. Test with known working project subdomains
5. Check browser console for errors
6. Verify project has MCP enabled in ReadMe settings

### Linting Errors

**Symptom**: `npm run lint` reports errors

**Solutions**:
1. Auto-fix formatting issues:
   ```bash
   npm run lint:fix
   ```
2. Check specific error messages in terminal
3. Review Biome configuration in `biome.jsonc`
4. Ensure code follows TypeScript best practices
5. Check for unused imports or variables

## Best Practices Summary

### Before Committing

**Always run**:
```bash
npm run build && npm run lint && npm test
```

**Checklist**:
- [ ] All tests pass
- [ ] No linting errors
- [ ] Build succeeds
- [ ] TypeScript types are correct
- [ ] Changes tested manually
- [ ] Documentation updated if needed
- [ ] Environment variables documented

### Code Quality

- Use explicit types, avoid `any`
- Write meaningful test cases
- Keep functions focused and small
- Document complex logic with comments
- Follow existing code patterns
- Use type imports for types-only imports

### Performance

- Set appropriate command timeouts (add 50% buffer)
- Never cancel long-running commands
- Monitor build and test times
- Optimize slow operations
- Use caching where appropriate

### Collaboration

- Write clear commit messages
- Update documentation with changes
- Test MCP integration when touching server code
- Communicate breaking changes to team
- Review PR checklist before submitting

## Additional Resources

- **Main README**: Setup and installation instructions
- **Documentation**: `/docs/` directory for feature guides
- **Examples**: `/fixtures/` directory for sample files
- **Evaluations**: `/evals/` directory for testing datasets
- **Configuration**: `/config/` directory for environment settings
