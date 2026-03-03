---
title: Testing and Validation
slug: testing
category:
  uri: Documentation
content:
  excerpt: Guide to running unit tests, integration tests, manual testing scenarios, and required pre-commit validation including linting and type checking.
---

# Testing and Validation

A comprehensive guide to running tests, performing manual validation, and ensuring code quality through pre-commit checks for the ReadMe AI Service.

## Overview

The ReadMe AI Service employs multiple layers of testing and validation to ensure code quality, reliability, and maintainability. This guide covers unit tests, integration tests, manual testing scenarios, and required pre-commit validation including linting and type checking.

**Key Testing Principles**:

- **Never cancel builds or tests** - Set timeouts to 120+ seconds for all commands
- **Test before committing** - Always run the full validation suite before pushing code
- **Validate MCP integration** - Test MCP server functionality when touching server or protocol code
- **Use appropriate test types** - Unit tests for business logic, integration tests for external services

## Unit Tests

Unit tests verify the correctness of business logic without external dependencies. They run quickly and don't require API keys or database connections.

### Running Unit Tests

```bash
npm test
```

**Expected Duration**: 10-20 seconds (never cancel)

**Coverage**: 54 tests across 8 files covering core functionality

### Test Structure

Unit tests are located in `src/ai/__tests__/` and focus on:

- Business logic validation
- Function behavior verification
- Edge case handling
- Error conditions

**Important**: Unit tests should **not** use the aiClient. Instead, mock external dependencies to isolate the code under test.

### Writing Unit Tests

When writing unit tests:

1. **Mock external dependencies** - Database calls, API requests, file system operations
2. **Test business logic only** - Focus on the correctness of algorithms and data transformations
3. **Use descriptive test names** - Clearly indicate what behavior is being tested
4. **Test edge cases** - Include tests for error conditions, empty inputs, and boundary values

**Example Test Structure**:

```typescript
import { describe, it, expect, vi } from 'vitest';
import { myFunction } from '../myModule.js';

describe('myFunction', () => {
  it('should return expected result for valid input', () => {
    const result = myFunction('valid input');
    expect(result).toBe('expected output');
  });

  it('should throw error for invalid input', () => {
    expect(() => myFunction(null)).toThrow('Invalid input');
  });
});
```

## Integration Tests

Integration tests verify functionality against live external services including ReadMe API, AI service endpoints, and MongoDB. These tests ensure the system works correctly when all components are connected.

### Prerequisites

**Required Environment Variables**:

- `README_API_KEY` - Token for ReadMe API access
  - Local: Get from your project's API key page
  - Next: https://dash.next.readme.ninja/project/developers/v3.0/api-key
  - Stage: https://dash.readmestaging.com/project/developers/v3.0/api-key
  - Prod: https://dash.readme.com/project/developers/v3.0/api-key

- `AI_TOKEN` - Authentication token for AI service
  - Local default: `secret`
  - Stage/Next: Get from Render dashboard
  - Prod: Get from Render dashboard

- `README_DOMAIN` - ReadMe service URL
  - Local default: `http://dash.readme.local:3000`
  - Next: `https://dash.next.readme.ninja`
  - Stage: `https://dash.readmestaging.com`
  - Prod: `https://dash.readme.com`

- `AI_SERVER_URL` - AI service URL
  - Local default: `http://localhost:9563`
  - Next: `https://readme-ai-next.onrender.com`
  - Stage: `https://readme-ai-stage.onrender.com`
  - Prod: `https://readme-ai.onrender.com`

### Running Integration Tests

```bash
npm run test:integration
```

**Expected Duration**: Variable depending on network and service response times

### Integration Test Guidelines

Integration tests should:

1. **Use random IDs** - Prevent conflicts with other tests
2. **Clean up after themselves** - Delete created resources
3. **Test against live services** - Verify real-world behavior
4. **Be high-quality and focused** - Only test critical integration points

**Test Location**: `src/aiClient/__tests__/`

**Purpose**: Verify the HTTP layer and client-server communication

## Manual Testing Scenarios

Always test these scenarios after making changes to ensure functionality remains intact.

### 1. Build Validation

Verify the complete build and test pipeline:

```bash
npm run build && npm run lint && npm test
```

**Expected Duration**: 25-45 seconds total

**What This Tests**:
- TypeScript compilation succeeds
- Code meets linting standards
- All unit tests pass

### 2. MCP Server Testing

Test the Model Context Protocol server integration (requires API keys):

**Step 1: Start AI Server**

```bash
npm run dev
```

**Step 2: Start ReadMe Main Server**

In a separate terminal, start the ReadMe main application server.

**Step 3: Run MCP Inspector**

```bash
npm run inspect
```

This launches the MCP Inspector dashboard at http://localhost:6274

**Step 4: Configure Inspector**

1. Navigate to the pre-filled URL containing the session token
2. Set Transport Type to "Streamable HTTP"
3. Change URL to `http://<project-subdomain>.readme.local:9563/mcp`
4. Optional: Add `?branch=<branch-name>` to test specific documentation branches
5. Open configuration panel and input the proxy address
6. Press Connect

**What This Tests**:
- MCP server starts correctly
- Project identification via host headers
- Tool registration based on project configuration
- MCP protocol implementation
- Branch parameter handling

### 3. CLI Tool Validation

Test command-line interface functionality:

**Test Help Output** (no API keys required):

```bash
npm run cli:lint
```

**Expected Output**: Usage information and command options

**Test With API Keys**:

```bash
npm run cli:lint rules ./fixtures/example-rules-errors.md ./fixtures/example-content.md
```

**What This Tests**:
- CLI argument parsing
- Help text display
- Actual linting functionality with example files

### 4. Chat CLI Testing

Test conversational AI functionality:

```bash
npm run cli:chat
```

**Prerequisites**:
- `OPENAI_KEY` environment variable
- `GOOGLE_GENERATIVE_AI_API_KEY` environment variable
- Subdomain already vectorized

**What This Tests**:
- OpenAI integration
- Chat prompt handling
- Response generation
- Context retrieval from vector database

### 5. Vectorization Testing

Test documentation indexing:

```bash
npm run cli:vectorize index <subdomain>
```

**Prerequisites**:
- `AI_TOKEN` environment variable
- `README_DOMAIN` environment variable
- MongoDB connection configured

**What This Tests**:
- Documentation fetching from ReadMe API
- Text chunking and embedding generation
- Vector storage in MongoDB Atlas
- Index creation and updates

## Pre-Commit Validation

**Critical**: Always run these checks before committing code. CI will fail if any of these checks fail.

### Linting

Run the complete linting suite:

```bash
npm run lint
```

**Expected Duration**: 8-25 seconds (faster after first run due to caching)

**What This Checks**:
- Code formatting (Prettier + Biome)
- TypeScript type checking
- Code style violations
- Import organization

**Configuration Files**:
- `biome.jsonc` - Linting and formatting rules
- `tsconfig.json` - TypeScript configuration
- `.prettierrc` - Prettier formatting rules

### Type Checking

TypeScript type checking is included in the lint command, but you can run it separately:

```bash
npx tsc --noEmit
```

**What This Checks**:
- Type safety violations
- Missing type definitions
- Type compatibility issues
- Strict mode compliance

### Format Checking

Verify code formatting without making changes:

```bash
npx biome check .
```

**Auto-fix formatting issues**:

```bash
npx biome check --write .
```

## Complete Pre-Commit Workflow

Before committing code, run this complete validation sequence:

```bash
# 1. Build the project
npm run build

# 2. Run linting and type checking
npm run lint

# 3. Run unit tests
npm test

# 4. Optional: Run integration tests if touching external integrations
npm run test:integration
```

**Expected Total Duration**: 30-50 seconds (excluding integration tests)

**If any step fails**:
1. Review the error messages
2. Fix the issues
3. Re-run the failed step
4. Continue with remaining steps

## Testing Best Practices

### General Guidelines

1. **Set appropriate timeouts** - Never cancel long-running commands; add 50% buffer to expected durations
2. **Test incrementally** - Run tests frequently during development, not just before committing
3. **Use descriptive test names** - Make it clear what behavior is being tested
4. **Mock external dependencies** - Keep unit tests fast and reliable
5. **Clean up test data** - Ensure integration tests don't leave artifacts

### Performance Expectations

Add 50% buffer to these timings when setting timeouts:

- `npm install`: 40-60 seconds
- `npm run build`: 6-7 seconds
- `npm run lint`: 8-25 seconds
- `npm test`: 9-20 seconds
- Complete workflow: 25-45 seconds

### When to Run Each Test Type

**Unit Tests**:
- After every code change
- Before committing
- During CI/CD pipeline

**Integration Tests**:
- When modifying external integrations
- Before major releases
- When testing end-to-end workflows

**Manual Testing**:
- After significant feature changes
- When modifying MCP server code
- Before deploying to production

## Troubleshooting

### Build Failures

**Symptom**: TypeScript compilation errors

**Solutions**:
1. Run `npm run lint` to identify issues
2. Check for missing type definitions
3. Verify all imports use `.js` extensions
4. Ensure strict TypeScript settings are satisfied

### Test Failures

**Symptom**: Unit or integration tests fail

**Solutions**:
1. Run individual test files to isolate issues
2. Check if tests require specific environment setup
3. Verify mock configurations in test files
4. Ensure database is initialized for integration tests

### Linting Errors

**Symptom**: Biome or Prettier errors

**Solutions**:
1. Run `npx biome check --write .` to auto-fix formatting
2. Review `biome.jsonc` for linting rules
3. Check for unused imports or variables
4. Verify code follows project style guidelines

### MCP Integration Issues

**Symptom**: MCP Inspector connection fails

**Solutions**:
1. Ensure both ReadMe and AI servers are running
2. Verify authentication tokens match
3. Check host header configuration
4. Test with known working project subdomains
5. Review MCP server logs for errors

### Environment Variable Issues

**Symptom**: Missing or invalid API keys

**Solutions**:
1. Verify all required environment variables are set
2. Check variable names match `custom-environment-variables.json`
3. For testing only, use dummy values: `OPENAI_KEY=dummy`
4. Ensure API keys have proper permissions

## Continuous Integration

The CI pipeline runs automatically on pull requests and includes:

1. **Dependency Installation** - `npm install`
2. **Build Verification** - `npm run build`
3. **Linting** - `npm run lint`
4. **Unit Tests** - `npm test`
5. **Integration Tests** - `npm run test:integration` (on specific branches)

**CI Configuration**: `.github/workflows/`

**Pull Request Requirements**:
- All checks must pass
- Code must be reviewed
- Branch must be up to date with main

## Additional Resources

- **Unit Test Examples**: `src/ai/__tests__/`
- **Integration Test Examples**: `src/aiClient/__tests__/`
- **CLI Tools Documentation**: `README.md` in project root
- **MCP Server Guide**: `docs/mcp-server.md`
- **Linting Configuration**: `biome.jsonc`
