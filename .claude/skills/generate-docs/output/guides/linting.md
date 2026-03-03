---
title: AI Linting
slug: linting
category:
  uri: Documentation
content:
  excerpt: Guide to AI-powered content analysis for markdown documentation, including rule validation, style guide compliance scoring, and pattern detection.
---

# AI Linting

Guide to AI-powered content analysis for markdown documentation, including rule validation, style guide compliance scoring, and pattern detection.

## Overview

AI Linting provides intelligent content analysis for markdown documentation using large language models. It validates content against custom rules, scores adherence to style guidelines, and detects patterns to suggest improvements. This feature helps maintain consistent, high-quality documentation at scale.

**Key Capabilities**:

- **Rule Validation**: Check content against custom writing rules with detailed violation reporting
- **Style Guide Compliance**: Score content adherence to style guidelines on a 0-10 scale
- **Pattern Detection**: Automatically identify common issues and suggest new rules
- **Batch Processing**: Analyze multiple files or entire directories
- **Structured Output**: Receive detailed feedback with line numbers and suggestions

## How It Works

The linting system uses AI models to analyze markdown content against provided guidelines:

```
Content + Rules/Style Guide
    ↓
AI Analysis (GPT, Gemini, Claude)
    ↓
Structured Results
    ↓
Violations/Scores + Suggestions
```

### Analysis Process

1. **Input Processing**: Content and rules are formatted into prompts
2. **AI Analysis**: LLM analyzes content against guidelines
3. **Result Extraction**: Structured data extracted from AI response
4. **Reporting**: Violations, scores, and suggestions returned

## Getting Started

### Prerequisites

- **API Keys**: At least one LLM provider key required
  - `OPENAI_KEY` for GPT models
  - `GOOGLE_GENERATIVE_AI_API_KEY` for Gemini models
  - `ANTHROPIC_API_KEY` for Claude models

### CLI Usage

The linting CLI provides two analysis modes: rules validation and style guide scoring.

#### Basic Syntax

```bash
npm run cli:lint <action> [prompt-file] [content-file-or-folder] [options]
```

**Actions**:
- `rules` - Validate content against specific rules
- `styleguide` - Score content against style guide principles

**Options**:
- `--hide-results` - Suppress detailed output to console
- `--write-to-file` - Save results to JSONL file

#### Examples

**Using Default Files**:
```bash
npm run cli:lint rules
```

**Custom Rules File**:
```bash
npm run cli:lint rules ./my-rules.md ./content/
```

**Style Guide Analysis**:
```bash
npm run cli:lint styleguide ./style-guide.md ./docs/
```

**Save Results to File**:
```bash
npm run cli:lint rules ./rules.md ./content/ --write-to-file
```

**Suppress Console Output**:
```bash
npm run cli:lint rules ./rules.md ./content/ --hide-results
```

## Rule Validation

Rule validation checks content against specific writing guidelines and reports violations.

### Creating Rules

Rules should be clear, specific, and actionable. Write them in markdown format:

```markdown
### Smart Quotes

Use curly quotes `"` `"` instead of straight quotes `"`.

### Em Dash Usage

Use em dash `—` instead of hyphen `-` for parenthetical phrases.

### Internal Lingo

Don't use internal terms like 'hub' or 'SuperHub'. Use 'dashboard' or 'platform' instead.
```

### Rule Validation Output

The system returns structured violations with:

- **Rule Name**: Which rule was violated
- **Message**: Description of the issue
- **Violation Text**: The exact problematic content
- **Line Number**: Where the violation occurs (when available)
- **Suggestion**: How to fix the issue

**Example Output**:

```json
{
  "violations": [
    {
      "ruleName": "Smart Quotes",
      "message": "Straight quotes used instead of curly quotes",
      "violationText": "\"documentation\"",
      "lineNumber": 15,
      "suggestion": "Use curly quotes: "documentation""
    }
  ]
}
```

## Style Guide Scoring

Style guide scoring evaluates overall adherence to documentation principles and best practices.

### Creating Style Guides

Style guides should articulate principles rather than specific rules:

```markdown
### Clarity and Simplicity

Our style guide aims for simplicity. Guidelines should be easy to apply to a range of scenarios.

### User-Focused Decisions

Decisions aren't about what's right or wrong according to grammar rules, but about what's best for our users.

### Consistency

Consistency and grammatical correctness are important, but not as important as clarity and meaning.

### Context Awareness

When making a style or structure decision, we consider the flow of information and the context.
```

### Style Guide Output

The system returns:

- **Score**: 0-10 rating of adherence
- **Feedback**: Detailed explanation of the score
- **Suggestions**: Specific improvements to align with style guide

**Example Output**:

```json
{
  "score": 7.5,
  "feedback": "The content demonstrates good clarity and user focus. However, some sections could be more concise, and there are opportunities to improve consistency in terminology.",
  "suggestions": [
    "Simplify complex sentences in the 'Getting Started' section",
    "Use consistent terminology for 'project' vs 'workspace'",
    "Add more context for technical decisions"
  ]
}
```

## API Integration

The linting service can be integrated programmatically via HTTP endpoints.

### Rules Validation Endpoint

**POST** `/lint/rules`

**Request Body**:

```json
{
  "prompt": "### Smart Quotes\n\nUse curly quotes instead of straight quotes.",
  "content": "This is a \"test\" document.",
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Response**:

```json
{
  "violations": [
    {
      "ruleName": "Smart Quotes",
      "message": "Straight quotes used",
      "violationText": "\"test\"",
      "suggestion": "Use curly quotes: "test""
    }
  ]
}
```

### Style Guide Endpoint

**POST** `/lint/styleguide`

**Request Body**:

```json
{
  "prompt": "Our style guide emphasizes clarity and simplicity...",
  "content": "# Documentation\n\nThis guide explains...",
  "llmOptions": {
    "model": "gpt-4o"
  }
}
```

**Response**:

```json
{
  "score": 8.5,
  "feedback": "Content aligns well with style guide principles...",
  "suggestions": ["Consider adding more examples", "Simplify technical jargon"]
}
```

## Model Selection

Different models offer varying performance characteristics:

### Recommended Models

Based on evaluation results (see `evals/lint/judge/`):

**Best Overall Quality**:
- `gemini-2.5-pro` - Highest average score (3.0/5)
- `gpt-4.1-mini` - Strong performance (2.9/5)
- `gpt-5` - Good quality (2.87/5)

**Best Speed**:
- `gemini-2.0-flash` - Fastest (0.0053s per character)
- `gemini-2.5-flash` - Fast with good quality (0.0056s per character)

**Best Balance**:
- `gpt-4.1-mini` - Good quality with reasonable speed (0.0085s per character)

### Model Configuration

Specify model in `llmOptions`:

```json
{
  "llmOptions": {
    "model": "gpt-4o",
    "temperature": 0.3
  }
}
```

**Supported Models**:
- OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-5`, `gpt-5-mini`, `gpt-5-nano`
- Google: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.0-flash`
- Anthropic: `claude-3-5-sonnet-20241022`

## Best Practices

### Writing Effective Rules

1. **Be Specific**: Clearly define what to check
   - Good: "Use em dash `—` for parenthetical phrases"
   - Bad: "Use proper punctuation"

2. **Provide Examples**: Show correct and incorrect usage
   ```markdown
   ### Contractions
   Use contractions for casual tone.
   - Good: "You'll find this helpful"
   - Bad: "You will find this helpful"
   ```

3. **Keep Rules Focused**: One rule per guideline
   - Separate "Smart Quotes" from "Em Dash Usage"

4. **Make Rules Actionable**: Include clear fix instructions
   - "Replace straight quotes `"` with curly quotes `"` `"`"

### Writing Effective Style Guides

1. **Focus on Principles**: Articulate why, not just what
   - "Clarity is more important than grammatical perfection"

2. **Provide Context**: Explain when to apply guidelines
   - "Use technical terms when writing for developers"

3. **Balance Flexibility**: Allow for judgment calls
   - "Consistency is important, but context matters"

4. **Include Examples**: Show principles in action

### Optimizing Performance

1. **Batch Processing**: Process multiple files together
2. **Model Selection**: Use faster models for initial checks
3. **Caching**: Reuse results for unchanged content
4. **Incremental Analysis**: Only check modified sections

## Troubleshooting

### No Violations Found

**Symptom**: Analysis returns empty violations array

**Possible Causes**:
- Rules are too vague
- Content actually complies with rules
- Model misunderstood the rules

**Solutions**:
1. Make rules more specific and concrete
2. Test with known violations
3. Try a different model

### Inconsistent Results

**Symptom**: Same content produces different results

**Possible Causes**:
- Model temperature too high
- Rules are ambiguous
- Content is edge case

**Solutions**:
1. Lower temperature in `llmOptions`
2. Clarify rule definitions
3. Add explicit examples to rules

### Performance Issues

**Symptom**: Analysis takes too long

**Solutions**:
1. Use faster models (Gemini Flash, GPT-4o-mini)
2. Process smaller content chunks
3. Reduce content length before analysis
4. Enable `--hide-results` for batch processing

### API Key Errors

**Symptom**: Authentication failures

**Solutions**:
1. Verify API keys are set correctly
2. Check key has sufficient permissions
3. Ensure key is for the correct provider
4. Verify key hasn't expired

## Advanced Usage

### Custom Model Configuration

Use custom LLM endpoints:

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

### Batch Processing with JSONL Output

Process multiple files and save results:

```bash
npm run cli:lint rules ./rules.md ./docs/ --write-to-file
```

Results saved to: `./linting-results-YYYY-MM-DD-HH-mm-ss.jsonl`

Each line contains results for one file:

```jsonl
{"file":"doc1.md","violations":[...],"timestamp":"2024-01-15T10:30:00Z"}
{"file":"doc2.md","violations":[...],"timestamp":"2024-01-15T10:30:01Z"}
```

### Programmatic Integration

Use the AI client for programmatic access:

```typescript
import { AiClient } from './src/aiClient/index.js';

const client = new AiClient({
  url: 'http://localhost:9563',
  authToken: 'your-token'
});

const result = await client.lintRules({
  prompt: rulesContent,
  content: documentContent,
  llmOptions: { model: 'gpt-4o' }
});

console.log(result.violations);
```

## Key Files

- `src/ai/lint/routes.ts` - API endpoint definitions
- `src/ai/lint/prompts.ts` - Analysis prompt templates
- `src/ai/lint/cli.ts` - CLI interface implementation
- `src/routes/operations/lint/` - Route handlers
- `evals/lint/` - Evaluation datasets and results
- `fixtures/example-rules-*.md` - Example rule files
- `fixtures/example-styleguide.md` - Example style guide

## Related Documentation

- [AI Agent](./docs/ai-agent.md) - Tool-augmented AI capabilities
- [Ask AI Chat](./docs/ask-ai-chat.md) - Conversational AI features
- [Vectorization](./docs/vectorization.md) - Document indexing for RAG
