---
title: Vectorization
slug: vectorization
category:
  uri: Documentation
content:
  excerpt: Documentation for indexing documentation into vector embeddings for semantic search and RAG, including the vectorization process, CLI usage, and troubleshooting.
---

# Vectorization

Complete guide to indexing documentation into vector embeddings for semantic search and Retrieval-Augmented Generation (RAG).

## Overview

Vectorization transforms documentation content into mathematical vector representations that capture semantic meaning. This enables:

- **Semantic Search**: Find relevant content by meaning, not just keywords
- **RAG Support**: Provide contextual information for AI chat responses
- **Similarity Matching**: Discover related documentation automatically
- **Multi-Project Search**: Search across multiple documentation sets simultaneously

The vectorization process converts text into high-dimensional vectors using OpenAI's embedding models, then stores them in MongoDB Atlas with vector search indexes for efficient retrieval.

## How Vectorization Works

### Process Overview

```
Documentation Pages (from ReadMe API)
    ↓
Text Chunking (RecursiveCharacterTextSplitter)
    ↓
Content Hashing (for change detection)
    ↓
Embedding Generation (OpenAI text-embedding-3-large)
    ↓
Vector Storage (MongoDB Atlas)
    ↓
Vector Search Index (for similarity queries)
```

### Text Chunking

Documentation is split into manageable chunks to optimize embedding quality and retrieval accuracy:

- **Chunk Size**: 1000 characters (configurable)
- **Overlap**: 200 characters between chunks
- **Method**: RecursiveCharacterTextSplitter preserves semantic boundaries
- **Metadata**: Each chunk retains page title, URL, and position information

### Embedding Generation

Chunks are converted to vectors using OpenAI's embedding model:

- **Model**: text-embedding-3-large
- **Dimensions**: 3072
- **Quality**: High semantic accuracy for technical documentation
- **Cost**: Optimized batch processing to minimize API calls

### Change Detection

Content hashing prevents unnecessary re-vectorization:

- **Hash Algorithm**: SHA-256 of chunk content
- **Comparison**: New hashes compared against stored hashes
- **Update Strategy**: Only changed chunks are re-embedded
- **Efficiency**: Reduces API costs and processing time

## Database Setup

### Prerequisites

You need a MongoDB Atlas instance with vector search capabilities. **Regular MongoDB will not work.**

#### Local Development Options

**Option 1: Run without MongoDB**

By default, `AI_MONGO_URI` is set to an empty string. The server will start, but vectorization operations will fail. This is acceptable if you're not working on vectorization features.

**Option 2: Use Staging MongoDB**

Obtain the connection string from 1Password and set:

```bash
export AI_MONGO_URI="mongodb+srv://..."
```

**Option 3: Use Your Own MongoDB Atlas Instance**

1. Create a MongoDB Atlas cluster with vector search enabled
2. Set `AI_MONGO_URI` to your connection string
3. Initialize the database (see below)

**Option 4: Start Local MongoDB Atlas Container**

```bash
./start-mongo.sh
```

This script will:

1. Start a MongoDB Atlas container using Docker
2. Wait for the container to be healthy
3. Output a connection string like:
   ```
   connection_string=mongodb://127.0.0.1:55008
   ```

Copy the connection string and set it as your environment variable:

```bash
export AI_MONGO_URI="mongodb://127.0.0.1:55008"
```

Then initialize the database (see below).

### Initialize Database

**Only required for new MongoDB instances.** Skip this step if connecting to an existing database.

```bash
npm run cli:vectorize initdb
```

This command creates:

- `readme-ai-vector-collection` collection
- `vectorizeQueue` collection for job management
- Vector search indexes with proper configuration

Run this once per database instance.

## CLI Usage

### Index Entire Project

Index all documentation for a subdomain:

```bash
npm run cli:vectorize index <subdomain>
```

**Example**:

```bash
npm run cli:vectorize index developers
```

**Output**:

```
Fetching documentation...
Found 25 guides, 10 references
Creating vectorization jobs...
Vectorization started. Job count: 35
Processing chunks...
✓ Vectorization complete
```

**What Gets Indexed**:

- All published guide pages
- All API reference pages
- Page metadata (titles, URLs, categories)
- Custom content (if configured)

**What Doesn't Get Indexed**:

- Hidden or draft pages
- Changelog entries
- Custom pages (unless explicitly configured)

### Process Flow

When you run the index command:

1. **Fetch Documentation**: Retrieves all pages from ReadMe API
2. **Create Jobs**: Generates vectorization jobs for each page
3. **Queue Processing**: Jobs are processed sequentially
4. **Chunk & Embed**: Each page is chunked and embedded
5. **Store Vectors**: Embeddings saved to MongoDB with metadata
6. **Index Update**: Vector search index automatically updated

### Performance Considerations

**Time Estimates**:

- Small project (10-20 pages): 1-2 minutes
- Medium project (50-100 pages): 5-10 minutes
- Large project (200+ pages): 15-30 minutes

**Factors Affecting Speed**:

- Number of pages
- Page length
- API rate limits
- Network latency
- Database performance

## Vector Storage Schema

### Document Structure

Each vector document in MongoDB contains:

```json
{
  "_id": "ObjectId",
  "subdomain": "developers",
  "pageId": "page_123",
  "pageTitle": "Getting Started",
  "pageUrl": "https://developers.example.com/docs/getting-started",
  "chunkIndex": 0,
  "content": "This is the documentation content...",
  "contentHash": "sha256_hash_of_content",
  "embedding": [0.123, -0.456, ...], // 3072 dimensions
  "metadata": {
    "category": "Guides",
    "version": "v1.0",
    "lastUpdated": "2024-01-15T10:30:00Z"
  }
}
```

### Vector Search Index

The MongoDB Atlas vector search index configuration:

- **Index Name**: `vector_index`
- **Path**: `embedding`
- **Dimensions**: 3072
- **Similarity**: cosine
- **Type**: vectorSearch

## Integration with Chat

Vectorized content powers the RAG system in Ask AI Chat:

### Query Flow

```
User Question
    ↓
Query Embedding (same model as documents)
    ↓
Vector Similarity Search (MongoDB Atlas)
    ↓
Top K Most Relevant Chunks (default: 10)
    ↓
Context Assembly (combine chunks)
    ↓
LLM Prompt (system + context + query)
    ↓
AI Response with Citations
```

### Similarity Threshold

- **Default**: 0.75
- **Range**: 0.0 to 1.0
- **Higher**: More strict, fewer but more relevant results
- **Lower**: More lenient, more results but potentially less relevant

### Context Window

- **Max Chunks**: 10 (configurable)
- **Total Context**: ~10,000 characters
- **Prioritization**: Highest similarity scores first
- **Page Context**: If user is on a specific page, that page's content is prioritized

## Troubleshooting

### Vectorization Fails

**Symptom**: Error during indexing process

**Common Causes**:

1. **Missing API Keys**
   - Ensure `OPENAI_KEY` is set
   - Verify key is valid and has credits

2. **Database Connection Issues**
   - Check `AI_MONGO_URI` is correct
   - Verify MongoDB Atlas cluster is running
   - Ensure network connectivity

3. **ReadMe API Issues**
   - Verify `AI_TOKEN` is set
   - Check `README_DOMAIN` is correct
   - Ensure subdomain exists and is accessible

**Solutions**:

```bash
# Verify environment variables
echo $OPENAI_KEY
echo $AI_MONGO_URI
echo $AI_TOKEN
echo $README_DOMAIN

# Test database connection
npm run cli:vectorize initdb

# Try indexing with verbose logging
DEBUG=* npm run cli:vectorize index <subdomain>
```

### Search Returns No Results

**Symptom**: Chat returns "I don't have enough information..."

**Causes**:

- Documentation not vectorized
- Similarity threshold too high
- Query too vague or unrelated

**Solutions**:

1. **Verify Vectorization**:
   ```bash
   npm run cli:vectorize index <subdomain>
   ```

2. **Check Vector Count**:
   Query MongoDB to verify vectors exist:
   ```javascript
   db.getCollection('readme-ai-vector-collection').countDocuments({
     subdomain: 'your-subdomain'
   })
   ```

3. **Test with Specific Queries**:
   Use exact phrases from your documentation to verify retrieval works

### Outdated Results

**Symptom**: Chat returns information from old documentation

**Cause**: Documentation updated but not re-vectorized

**Solution**:

Re-index the subdomain to update vectors:

```bash
npm run cli:vectorize index <subdomain>
```

**Note**: The system uses content hashing, so only changed pages will be re-processed.

### Slow Vectorization

**Symptom**: Indexing takes longer than expected

**Causes**:

- Large number of pages
- Network latency
- API rate limiting
- Database performance

**Solutions**:

1. **Monitor Progress**: Check logs for bottlenecks
2. **Optimize Network**: Ensure stable connection
3. **Database Performance**: Verify MongoDB Atlas cluster size is adequate
4. **Batch Processing**: The system already batches requests, but you can adjust batch sizes in code if needed

### Memory Issues

**Symptom**: Process crashes with out-of-memory errors

**Cause**: Processing too many large documents simultaneously

**Solutions**:

1. **Increase Node Memory**:
   ```bash
   NODE_OPTIONS="--max-old-space-size=4096" npm run cli:vectorize index <subdomain>
   ```

2. **Process in Batches**: Index smaller subsets of pages at a time

## Best Practices

### When to Re-Vectorize

Re-index your documentation when:

- **Content Changes**: Major updates to documentation
- **New Pages**: After adding significant new content
- **Structure Changes**: After reorganizing documentation
- **Model Updates**: When upgrading embedding models

**Frequency Recommendations**:

- **Active Development**: Daily or after major updates
- **Stable Documentation**: Weekly or bi-weekly
- **Mature Projects**: Monthly or as needed

### Optimizing Search Quality

**Improve Retrieval Accuracy**:

1. **Clear Page Titles**: Use descriptive, keyword-rich titles
2. **Structured Content**: Organize content with clear headings
3. **Consistent Terminology**: Use standard terms throughout documentation
4. **Comprehensive Coverage**: Ensure all important topics are documented

**Avoid Common Pitfalls**:

- Don't duplicate content across pages (creates noise)
- Avoid overly long pages (split into logical sections)
- Don't use vague headings (be specific)
- Avoid jargon without definitions

### Cost Management

**Minimize Embedding Costs**:

1. **Incremental Updates**: Only re-vectorize changed content
2. **Content Hashing**: Automatically skips unchanged chunks
3. **Batch Processing**: Reduces API overhead
4. **Optimize Chunk Size**: Balance between granularity and cost

**Monitor Usage**:

- Track OpenAI API usage in dashboard
- Set up billing alerts
- Review vectorization logs for efficiency

## Advanced Configuration

### Custom Chunk Sizes

Modify chunk parameters in `src/ai/vectorize/vectorize.ts`:

```typescript
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,      // Adjust for your content
  chunkOverlap: 200,    // Adjust for context preservation
});
```

**Considerations**:

- **Larger Chunks**: Better context, but less precise retrieval
- **Smaller Chunks**: More precise, but may lose context
- **Overlap**: Ensures important information isn't split

### Multi-Subdomain Search

For enterprise users searching across multiple projects:

```typescript
const results = await searchVectors({
  query: "How do I authenticate?",
  subdomains: ["project-a", "project-b", "project-c"],
  topK: 10
});
```

**Benefits**:

- Unified search across all documentation
- Cross-project knowledge retrieval
- Consistent answers across products

### Custom Metadata

Add custom metadata to vectors for enhanced filtering:

```typescript
{
  metadata: {
    category: "API Reference",
    version: "v2.0",
    audience: "developers",
    tags: ["authentication", "security"]
  }
}
```

**Use Cases**:

- Filter by documentation version
- Target specific audiences
- Organize by topic or category

## Monitoring and Maintenance

### Health Checks

Verify vectorization system health:

1. **Database Connection**: Ensure MongoDB Atlas is accessible
2. **Vector Count**: Monitor number of vectors per subdomain
3. **Index Status**: Verify vector search index is active
4. **Embedding Quality**: Spot-check search results

### Logs and Debugging

Enable verbose logging:

```bash
DEBUG=vectorize:* npm run cli:vectorize index <subdomain>
```

**Log Levels**:

- `vectorize:info` - General progress
- `vectorize:debug` - Detailed operations
- `vectorize:error` - Errors and failures

### Performance Metrics

Track these metrics:

- **Vectorization Time**: Total time to index a project
- **Chunk Count**: Number of chunks per page
- **Embedding Latency**: Time to generate embeddings
- **Search Latency**: Time to retrieve results
- **Search Accuracy**: Relevance of retrieved chunks

## Migration and Backup

### Exporting Vectors

Currently, there's no built-in export functionality. To backup vectors:

1. Use MongoDB Atlas backup features
2. Export collection using `mongodump`
3. Store backups in secure location

### Re-Vectorizing After Migration

If migrating to a new database:

1. Set up new MongoDB Atlas instance
2. Initialize database: `npm run cli:vectorize initdb`
3. Re-index all subdomains: `npm run cli:vectorize index <subdomain>`

### Version Upgrades

When upgrading embedding models:

1. Update model configuration in code
2. Re-vectorize all content with new model
3. Verify search quality with test queries
4. Monitor performance and accuracy

## API Reference

### Vectorization Endpoints

While primarily used via CLI, vectorization can be triggered via API:

**POST /vectorize/index**

Trigger vectorization for a subdomain.

**Request**:

```json
{
  "subdomain": "developers",
  "force": false
}
```

**Response**:

```json
{
  "status": "started",
  "jobCount": 35,
  "subdomain": "developers"
}
```

**POST /vectorize/search**

Search vectors directly.

**Request**:

```json
{
  "query": "How do I authenticate?",
  "subdomain": "developers",
  "topK": 10,
  "threshold": 0.75
}
```

**Response**:

```json
{
  "results": [
    {
      "pageTitle": "Authentication Guide",
      "pageUrl": "https://developers.example.com/docs/auth",
      "content": "To authenticate, use your API key...",
      "score": 0.92
    }
  ]
}
```

## Support

For issues or questions about vectorization:

1. Check this documentation first
2. Review error logs for specific issues
3. Test with minimal examples
4. Contact the team via support channels

**Common Support Requests**:

- Database connection issues
- API key configuration
- Performance optimization
- Search quality improvements
