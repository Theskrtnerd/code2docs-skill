---
title: MCP Server
slug: mcp-server
category:
  uri: Documentation
content:
  excerpt: Comprehensive guide to the Model Context Protocol server implementation, including project identification, tool registration, caching strategy, and integration with AI assistants like Claude and Cursor.
---

# MCP Server

Complete guide to the Model Context Protocol (MCP) server implementation in the ReadMe AI Service, including project identification, tool registration, caching strategy, and integration with AI assistants like Claude and Cursor.

## Overview

The MCP server enables AI assistants to interact with ReadMe documentation and APIs through a standardized protocol. It provides tools for searching documentation, querying API specifications, and executing requests directly from AI development environments.

**Key Features**:

- **Dynamic Tool Registration**: Tools are automatically registered based on project configuration
- **Smart Caching**: Specifications are cached with background refresh for optimal performance
- **Project Identification**: Projects are identified via HTTP host headers
- **Branch Support**: Access different documentation versions through query parameters
- **Custom Tools**: Support for project-specific tool definitions

## Architecture

The MCP server follows a request-response flow that identifies projects, retrieves specifications, and handles tool calls:

```
MCP Client (Cursor / Claude Desktop / VS Code)
    ↓
HTTP Request with Host Header
    ↓
AI Service (/mcp endpoint)
    ↓
Project Identification (via host header)
    ↓
Cache Check (readme:getInfo:<host>:<branch>)
    ├─ Cache Hit → Return cached data + refresh in background
    └─ Cache Miss → Fetch from ReadMe server
         ↓
    POST /api-next/v2/mcp/info
         ↓
    ReadMe Server Response
         ↓
    Store in Cache (stale-while-revalidate)
    ↓
MCP Server Creation
    ↓
Tool Registration (based on available specs)
    ↓
Handle MCP Protocol Request
    ↓
Response to Client
```

## Project Identification

### Host Header Matching

The MCP server identifies which ReadMe project to serve based on HTTP headers. This allows multiple projects to be served from the same endpoint.

**Primary Header**: `x-forwarded-host`  
**Fallback Header**: `host`

**Implementation** (`src/server.ts:33-56`):

The server extracts the host from incoming requests and uses it to determine which project's documentation to serve.

### Header Format

**For ReadMe Projects**:

```
x-forwarded-host: <subdomain>.<domain>
```

**Examples**:

```
# Production
x-forwarded-host: my-docs.readme.com

# Staging
x-forwarded-host: my-docs.readmestaging.com

# Local development
x-forwarded-host: my-docs.readme.local:3000

# Multi-project (SuperHub)
x-forwarded-host: main-project.readme.com
```

### URL Format

**MCP Endpoint**:

```
POST http://<subdomain>.<domain>:<port>/mcp?branch=<branch>
```

**Examples**:

```bash
# Local development (default branch)
http://my-docs.readme.local:9563/mcp

# Local development (specific branch)
http://my-docs.readme.local:9563/mcp?branch=next

# Production
https://readme-ai.onrender.com/mcp
  Headers: x-forwarded-host: my-docs.readme.com
```

## Spec Retrieval and Caching

### Cache Strategy: Stale-While-Revalidate

The MCP server implements a stale-while-revalidate caching strategy that optimizes for both speed and freshness:

1. **Cache Hit**: Returns cached data immediately for fast response times
2. **Background Refresh**: Triggers asynchronous cache update in the background
3. **Cache Miss**: Fetches from ReadMe server and stores in cache

This approach ensures users always get fast responses while keeping data current.

**Implementation** (`src/lib/readmeApi.ts:185-204`):

The cache layer sits between the MCP server and the ReadMe API, reducing latency and server load.

### Cache Key Format

Cache keys are structured to support multiple projects and branches:

```
readme:getInfo:<host>:<branch>
```

**Examples**:

```
readme:getInfo:my-docs.readme.com:stable
readme:getInfo:my-docs.readme.com:next
readme:getInfo:my-docs.readmestaging.com:stable
```

Each unique combination of host and branch maintains its own cache entry.

## ReadMe Server Integration

### Endpoint

The MCP server fetches project information from the ReadMe API:

**URL**: `POST /api-next/v2/mcp/info`  
**Full URL**: `${readmeDomain}/api-next/v2/mcp/info`

**readmeDomain Examples**:

- Local: `http://dash.readme.local:3000`
- Staging: `https://dash.readmestaging.com`
- Production: `https://dash.readme.com`

**Response Structure**:

The endpoint returns project configuration including:

- Available API specifications (OpenAPI schemas)
- Project metadata and settings
- Custom tool definitions
- Disabled tool list

## Tool Registration

### Dynamic Tool Registration

Tools are registered dynamically based on what's available in each project. This allows different projects to expose different capabilities through the MCP server.

**Process**:

1. Fetch project information from ReadMe (with caching)
2. Determine available tools based on project configuration
3. Merge tools across all projects (for multi-project setups)
4. Register tools with the MCP server instance

**Implementation** (`src/lib/mcpServer.ts:49-97`):

The registration process filters out disabled tools and ensures only relevant tools are exposed to clients.

### Available Tools

**Reference Page Tools** (API-related):

- `list-specs` - List all available API specifications
- `list-endpoints` - List endpoints within a specification
- `get-endpoint` - Get detailed information about an endpoint
- `get-request-body` - Get request schema for an endpoint
- `get-response-schema` - Get response schema for an endpoint
- `list-security-schemes` - List authentication methods
- `search-specs` - Search across API specifications
- `execute-request` - Execute API calls directly
- `get-code-snippet` - Generate code examples in various languages
- `get-server-variables` - Get server configuration variables

**Guide Page Tools** (Documentation-related):

- `search-guides` - Search documentation pages
- `fetch-guide` - Fetch complete guide content

**Custom Tools**:

Projects can define custom tools in ReadMe that return predefined text content.

### Tool Filtering

Projects can disable specific tools to control what capabilities are exposed:

**Configuration** (in ReadMe project settings):

```json
{
  "disabled_tools": ["execute-request", "list-security-schemes"]
}
```

**Effect**: These tools will not be available to MCP clients connecting to this project.

**Common Reasons to Disable**:

- `execute-request`: Prevent API calls from being executed through AI assistants
- `list-security-schemes`: Hide authentication implementation details
- `search-specs`: Limit API exploration capabilities

## Branch Support

### Branch Parameter

Access different documentation branches using the optional `branch` query parameter:

**URL Format**:

```
POST /mcp?branch=<branch-name>
```

**Examples**:

```bash
# Stable branch (default)
POST /mcp

# Staging branch
POST /mcp?branch=next

# Feature branch
POST /mcp?branch=v2.0_feature
```

### Branch Behavior

**Cache Keys**: Each branch maintains separate cache entries

```
readme:getInfo:my-docs.readme.com:stable
readme:getInfo:my-docs.readme.com:next
```

**Tool Availability**: May differ per branch based on:

- Different API specifications
- Different documentation pages
- Different custom tool definitions

### Use Cases

**Testing Unreleased Documentation**:

```bash
# Connect to staging documentation
http://my-docs.readme.local:9563/mcp?branch=staging
```

**Multi-Version API Support**:

```bash
# v1 API documentation
http://my-docs.readme.local:9563/mcp?branch=v1

# v2 API documentation
http://my-docs.readme.local:9563/mcp?branch=v2
```

## MCP Request Handling

### Request Flow

The complete request handling flow:

1. **Client sends MCP request** to the `/mcp` endpoint
2. **Extract host header** (`x-forwarded-host` or `host`)
3. **Extract branch parameter** (defaults to `stable` if not provided)
4. **Fetch project info** using cache (stale-while-revalidate)
5. **Create MCP server instance** with project configuration
6. **Register tools** based on available specs and disabled tools list
7. **Connect transport** to handle MCP protocol communication
8. **Handle MCP protocol request** (tool calls, resource requests, etc.)
9. **Return response** to client

## Multi-Project Support

### Multi-Project Configuration

For organizations with multiple projects, the MCP server supports aggregating tools across projects:

**Example Response**:

```json
{
  "projects": [
    {
      "subdomain": "main-docs",
      "schemas": [...]
    },
    {
      "subdomain": "api-docs",
      "schemas": [...]
    }
  ]
}
```

### Tool Aggregation

Tools are merged across all projects to provide unified access:

**Example**:

```
Project A has: ["Payments API", "Users API"]
Project B has: ["Orders API"]

Available tools:
- list-endpoints (schemas: ["Payments API", "Users API", "Orders API"])
- get-endpoint (schemas: ["Payments API", "Users API", "Orders API"])
```

**Benefits**:

- Single MCP connection for all projects
- Unified tool interface across documentation sets
- Centralized documentation access point

## Custom Tools

### Custom Tool Support

Projects can define custom tools in ReadMe that return predefined text content. These tools appear alongside built-in tools and can provide project-specific functionality or information.

**Use Cases**:

- Return company-specific guidelines
- Provide onboarding instructions
- Share internal documentation links

## Integration with AI Assistants

### Cursor

**Supported Versions**: 1.1+

**Configuration**:

1. Open Cursor Settings
2. Navigate to "Tools & Integrations"
3. Click "New MCP Server"
4. Add configuration:

```json
{
  "mcpServers": {
    "ReadMeAPI": {
      "url": "https://docs.readme.com/mcp"
    }
  }
}
```

### VS Code

**Supported Versions**: 1.101+

**Configuration**:

1. Open Command Palette
2. Select "MCP: Add Server..."
3. Select "HTTP (HTTP or Server-Sent Events)"
4. Enter URL: `https://docs.readme.com/mcp`
5. Enter identifier: "ReadMe API"

### Claude Desktop

**Supported Versions**: 0.11.6+

**Configuration**:

1. Click "Search & Tools"
2. Click "Manage connectors"
3. Click "Add custom connector"
4. Enter integration name: "ReadMe API"
5. Enter URL: `https://docs.readme.com/mcp`

## Testing

### Local Testing

**1. Start Services**:

```bash
# Terminal 1: Start ReadMe server
cd readme && make start

# Terminal 2: Start AI service
cd ai && make start
```

**2. Test MCP Endpoint**:

```bash
curl -X POST http://my-docs.readme.local:9563/mcp \
  -H "x-forwarded-host: my-docs.readme.local:3000" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

**3. Test with MCP Inspector**:

```bash
npm run inspect
# Navigate to http://localhost:6274
# Set URL: http://my-docs.readme.local:9563/mcp
```

### Testing Workflow

1. **Verify Server Startup**: Ensure both ReadMe and AI services are running
2. **Check Project Configuration**: Verify project exists and has MCP enabled
3. **Test Tool Listing**: Confirm expected tools are available
4. **Test Tool Execution**: Execute sample tool calls
5. **Verify Caching**: Check cache behavior with repeated requests

## Troubleshooting

### Tools Not Available

**Symptom**: Expected tools not appearing in `tools/list` response

**Possible Causes**:

- Tools disabled in project settings
- No API specifications uploaded for project
- Branch doesn't contain specifications
- Project not properly configured

**Solutions**:

1. Check `disabled_tools` configuration in ReadMe project settings
2. Verify API specifications exist: check `info.projects[0].schemas`
3. Confirm branch parameter matches existing documentation branch
4. Review project configuration in ReadMe dashboard

### Connection Errors

**Symptom**: Unable to connect to MCP server

**Possible Causes**:

- Incorrect host header
- Server not running
- Network connectivity issues
- Invalid branch parameter

**Solutions**:

1. Verify host header matches project subdomain
2. Confirm AI service is running on expected port
3. Check network connectivity and firewall settings
4. Validate branch name exists in project

### Cache Issues

**Symptom**: Stale data being returned or cache not updating

**Possible Causes**:

- Cache not expiring properly
- Background refresh failing
- Redis connection issues

**Solutions**:

1. Check Redis connection and health
2. Verify background refresh is executing
3. Clear cache manually if needed
4. Review cache key format and TTL settings

### Performance Issues

**Symptom**: Slow response times

**Possible Causes**:

- Cache misses requiring API calls
- Large specification files
- Network latency to ReadMe server

**Solutions**:

1. Monitor cache hit rates
2. Optimize specification file sizes
3. Review network performance
4. Consider adjusting cache TTL values

## Best Practices

### Security

- Never expose API keys in MCP configuration files
- Use environment variables for sensitive credentials
- Implement proper authentication for production deployments
- Review disabled tools list to prevent unintended API access

### Performance

- Leverage caching to minimize API calls
- Monitor cache hit rates and adjust TTL as needed
- Use branch parameters to separate environments
- Consider specification file sizes when designing APIs

### Maintenance

- Regularly review and update disabled tools configuration
- Monitor MCP server logs for errors and warnings
- Test MCP integration after ReadMe updates
- Document custom tools and their purposes

### Development

- Test locally before deploying to production
- Use MCP Inspector for debugging
- Validate tool responses match expected schemas
- Keep AI assistant integrations up to date
