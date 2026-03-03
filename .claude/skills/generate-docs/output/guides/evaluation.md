---
title: Evaluation and Benchmarking
slug: evaluation
category:
  uri: Documentation
content:
  excerpt: Documentation for creating evaluation datasets, running evaluations against ground truth data, and interpreting evaluation results for chat and linting features.
---

# Evaluation and Benchmarking

Complete guide to creating evaluation datasets, running evaluations against ground truth data, and interpreting evaluation results for chat and linting features in the ReadMe AI Service.

## Overview

The evaluation system provides tools to measure and improve the quality of AI-powered features by comparing AI-generated outputs against ground truth data. This enables you to:

- **Measure Quality**: Quantify AI performance with numerical scores
- **Compare Models**: Benchmark different LLM models against each other
- **Track Improvements**: Monitor performance changes over time
- **Identify Issues**: Find specific cases where AI underperforms
- **Validate Changes**: Ensure code changes don't degrade quality

The evaluation framework supports two primary features:

- **Chat Evaluation**: Measures correctness of conversational AI responses
- **Linting Evaluation**: Assesses accuracy of content analysis and rule detection

## Key Concepts

### Ground Truth Data

Ground truth represents the "correct" or expected output for a given input. For chat evaluations, this includes:

- **Question**: The user's query
- **Expected Answer**: The ideal response
- **Context**: Relevant documentation chunks used to generate the answer

For linting evaluations, ground truth includes:

- **Content**: The text to analyze
- **Rules**: The style guide or rules to check against
- **Expected Violations**: Known issues that should be detected

### Evaluation Metrics

**Chat Correctness Score**: A value from 0.0 to 5.0 indicating how well the AI-generated answer matches the expected answer:

- `5.0`: Perfect match - answer is completely correct
- `4.0`: Good - minor differences but semantically equivalent
- `3.0`: Acceptable - correct information with some gaps
- `2.0`: Partial - some correct information but missing key points
- `1.0`: Poor - mostly incorrect or irrelevant
- `0.0`: Wrong - completely incorrect or off-topic

**Linting Score**: A value from 0 to 5 indicating detection accuracy:

- `5`: Perfect detection - all violations found, no false positives
- `4`: Good - most violations found with minimal errors
- `3`: Acceptable - reasonable detection with some mistakes
- `2`: Poor - many missed violations or false positives
- `1`: Very poor - significant detection failures
- `0`: Failed - no useful detection

### Judges

Evaluations use AI models as "judges" to score outputs. Multiple judges can be used to reduce bias:

- **Primary Judge**: Main model used for scoring (e.g., `gemini-2.5-pro`)
- **Secondary Judge**: Additional model for comparison (e.g., `gpt-5.1`)
- **Judge Agreement**: Comparing scores across judges reveals consistency

## Chat Evaluation

### Creating Chat Evaluation Datasets

Generate evaluation questions and answers from vectorized documentation:

```bash
npm run cli:eval create <subdomain> [max_evals]
```

**Parameters**:

- `subdomain`: Project subdomain (must be vectorized first)
- `max_evals`: Optional limit on number of questions (for testing)

**Example**:

```bash
# Create full evaluation dataset
npm run cli:eval create developers

# Create limited dataset for testing
npm run cli:eval create developers 50
```

**Output**:

- Creates file in `evals/<subdomain>/groundtruths/`
- Filename format: `<subdomain>-evals-YYYY-MM-DD.json`
- Example: `evals/developers/groundtruths/developers-evals-2024-01-15.json`

**Dataset Structure**:

```json
[
  {
    "question": "How do I authenticate with the API?",
    "expectedAnswer": "Use Bearer token authentication by including your API key in the Authorization header...",
    "context": [
      {
        "text": "Authentication requires an API key...",
        "metadata": {
          "slug": "authentication",
          "title": "Authentication Guide"
        }
      }
    ]
  }
]
```

### Running Chat Evaluations

Execute evaluations against local AI service or production ReadMe API:

```bash
npm run cli:eval run <eval_file_path> <subdomain> [environment]
```

**Parameters**:

- `eval_file_path`: Path to ground truth JSON file
- `subdomain`: Project subdomain being evaluated
- `environment`: Optional - `prod` for production API, omit for local

**Examples**:

```bash
# Evaluate local AI service
npm run cli:eval run ./evals/developers/groundtruths/developers-evals-2024-01-15.json developers

# Evaluate production ReadMe API
npm run cli:eval run ./evals/developers/groundtruths/developers-evals-2024-01-15.json developers prod
```

**Process Flow**:

1. Load ground truth questions and expected answers
2. Send each question to the AI service
3. Collect AI-generated responses
4. Use judge models to score correctness
5. Calculate summary statistics
6. Save detailed results to JSON file

**Output Location**:

- Results saved to `evals/<subdomain>/results/`
- Filename format: `<service>-<subdomain>-YYYY-MM-DD.json`
- Example: `evals/developers/results/ai-developers-2024-01-15.json`

### Chat Evaluation Results

**Result File Structure**:

```json
{
  "summary": {
    "totalQuestions": 100,
    "averageScore": 4.23,
    "minScore": 2.5,
    "maxScore": 5.0,
    "scoreDistribution": {
      "5.0": 45,
      "4.0": 30,
      "3.0": 15,
      "2.0": 8,
      "1.0": 2
    }
  },
  "results": [
    {
      "question": "How do I authenticate?",
      "expectedAnswer": "Use Bearer token...",
      "actualAnswer": "Authentication requires a Bearer token...",
      "score": 4.5,
      "feedback": "Answer is correct and comprehensive",
      "judgeModel": "gemini-2.5-pro",
      "responseTime": 1234
    }
  ]
}
```

**Interpreting Scores**:

- **Average Score > 4.0**: Excellent performance
- **Average Score 3.0-4.0**: Good performance with room for improvement
- **Average Score 2.0-3.0**: Needs significant improvement
- **Average Score < 2.0**: Major issues requiring investigation

**Common Issues**:

- **Low scores on specific topics**: May indicate missing or poor documentation
- **Inconsistent scores**: Could suggest prompt engineering issues
- **High variance**: May indicate judge model disagreement

## Linting Evaluation

### Creating Linting Evaluation Datasets

Linting evaluations use manually created test cases with known violations:

**Directory Structure**:

```
evals/lint/test-cases/
├── single-rule/
│   ├── prompt.md          # Style guide rules
│   └── content.md         # Content with violations
├── multiple-rules/
│   ├── prompt.md
│   ├── content.md
│   └── content_2.md
└── readme-docs-errors/
    ├── prompt.md
    ├── AskAI.md
    └── security-faq-index.md
```

**Test Case Format**:

Each test case directory contains:

- `prompt.md`: Rules or style guide to check against
- One or more content files with embedded violation markers

**Violation Markers**:

Mark expected violations in content using this format:

```markdown
<<Rule Name|Description|Violating Text>>
```

**Example**:

```markdown
Don't use emojis 🤖 in documentation.

This is wrong: <<Don't Use Emojis|Emoji '🎨' found.|🎨>>
```

### Running Linting Evaluations

Execute linting evaluations to compare model performance:

```bash
npm run cli:eval lint
```

**Process**:

1. Loads all test cases from `evals/lint/test-cases/`
2. Runs each test case through multiple models
3. Compares detected violations against expected violations
4. Uses judge models to score accuracy
5. Generates comparative results

**Models Evaluated**:

The system tests multiple models simultaneously:

- OpenAI models: `gpt-4o`, `gpt-4o-mini`, `gpt-5`, `gpt-5-mini`, `gpt-5-nano`
- Google models: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`
- Anthropic models: `claude-3-5-sonnet`

### Linting Evaluation Results

**Output Location**:

- Results saved to `evals/lint/judge/YYYY-MM-DDTHH-MM-SS-MSSZ/`
- Contains `results.md` with comparative analysis

**Results Table Format**:

```markdown
| model                 | averageScore | numberOfFiles | numberOfFilesWithError | averageDurationSeconds |
| --------------------- | ------------ | ------------- | ---------------------- | ---------------------- |
| gemini-2.5-pro        | 3.0          | 15            | 0                      | 10.05                  |
| gpt-5                 | 2.87         | 15            | 0                      | 14.77                  |
| gpt-4o                | 2.37         | 15            | 0                      | 2.28                   |
```

**Key Metrics**:

- **averageScore**: Mean score across all test cases
- **numberOfFiles**: Total test cases evaluated
- **numberOfFilesWithError**: Cases that failed to process
- **averageDurationSeconds**: Mean processing time per file

**Interpreting Results**:

- **Best Score**: Model with highest average score
- **Fastest**: Model with lowest average duration
- **Most Reliable**: Model with fewest errors
- **Best Balance**: Consider score, speed, and reliability together

## Model Comparison

### Comparative Analysis

When evaluating multiple models, the system generates comparative reports:

**Rankings by Score**:

```markdown
| Model            | Avg Score | Avg Time (s) | Errors |
| ---------------- | --------- | ------------ | ------ |
| gpt-5.2          | 4.289     | 5.13         | 0      |
| gpt-5.1          | 4.228     | 4.90         | 1      |
| gemini-2.5-flash | 4.155     | 0.96         | 0      |
```

**Rankings by Speed**:

```markdown
| Model            | Avg Score | Avg Time (s) | Errors |
| ---------------- | --------- | ------------ | ------ |
| gemini-2.5-flash | 4.155     | 0.96         | 0      |
| gemini-2.5-pro   | 4.059     | 1.32         | 0      |
| gpt-5.2          | 4.289     | 5.13         | 0      |
```

### Per-Judge Breakdown

When using multiple judges, results show score variance:

```markdown
| Model            | gemini-2.5-pro | gpt-5.1       |
| ---------------- | -------------- | ------------- |
| gpt-5.2          | 4.365 (n=707)  | 4.212 (n=707) |
| gemini-2.5-flash | 4.151 (n=707)  | 4.158 (n=707) |
```

**Judge Agreement Analysis**:

- **High agreement** (scores within 0.2): Reliable evaluation
- **Moderate agreement** (scores within 0.5): Acceptable variance
- **Low agreement** (scores differ by > 0.5): May indicate ambiguous cases

### Recommendations

The system provides recommendations based on results:

```markdown
## Recommendations

- **Best Score:** gpt-5.2 (4.289 avg score)
- **Fastest:** gemini-2.5-flash (0.96s avg response time)
- **Best Balance:** gpt-5.1 (4.228 score, 4.90s)
```

**Selection Criteria**:

- **Quality-focused**: Choose highest scoring model
- **Speed-focused**: Choose fastest model
- **Cost-focused**: Balance quality, speed, and API costs
- **Production use**: Consider reliability (error rate) heavily

## Best Practices

### Creating Quality Evaluation Datasets

**For Chat Evaluations**:

1. **Ensure comprehensive vectorization**: Vectorize all documentation before creating evals
2. **Review generated questions**: Manually verify questions are clear and answerable
3. **Validate expected answers**: Ensure ground truth answers are accurate and complete
4. **Cover edge cases**: Include questions about complex, ambiguous, or rarely-asked topics
5. **Update regularly**: Regenerate evals when documentation changes significantly

**For Linting Evaluations**:

1. **Use realistic content**: Test cases should resemble actual documentation
2. **Mark violations precisely**: Ensure violation markers are accurate and complete
3. **Test rule combinations**: Include cases with multiple rule violations
4. **Include negative cases**: Add content with no violations to test false positives
5. **Document expectations**: Clearly explain what each test case validates

### Running Evaluations Effectively

**Frequency**:

- **Before releases**: Validate changes don't degrade quality
- **After model updates**: Verify new models maintain or improve performance
- **Monthly baseline**: Track performance trends over time
- **After documentation changes**: Ensure AI adapts to new content

**Environment Considerations**:

- **Local testing**: Use for development and debugging
- **Production validation**: Compare against live API periodically
- **Staging environment**: Test changes before production deployment

**Resource Management**:

- **Limit concurrent evaluations**: Avoid rate limiting by spacing out runs
- **Use max_evals parameter**: Test with small datasets first
- **Monitor API costs**: Track usage across different models
- **Cache results**: Reuse evaluation results when possible

### Interpreting Results

**Score Trends**:

- **Improving scores**: Positive changes in prompts, models, or documentation
- **Declining scores**: May indicate documentation drift or model issues
- **Stable scores**: Consistent performance, good baseline

**Error Analysis**:

- **Systematic errors**: Patterns in low-scoring questions indicate specific issues
- **Random errors**: Isolated low scores may be acceptable
- **Judge disagreement**: High variance suggests ambiguous cases

**Action Items**:

- **Score < 3.0**: Investigate and fix immediately
- **Score 3.0-4.0**: Review and improve
- **Score > 4.0**: Monitor and maintain
- **High error rate**: Check API connectivity and model availability

## Troubleshooting

### Common Issues

**"No ground truth file found"**:

- **Cause**: Evaluation file doesn't exist or path is incorrect
- **Solution**: Verify file path and ensure dataset was created successfully

**"Subdomain not vectorized"**:

- **Cause**: Documentation hasn't been indexed
- **Solution**: Run `npm run cli:vectorize index <subdomain>` first

**"Rate limit exceeded"**:

- **Cause**: Too many API requests in short time
- **Solution**: Reduce concurrent evaluations or add delays between requests

**"Judge model failed"**:

- **Cause**: Judge model API error or invalid response
- **Solution**: Check API keys and model availability, retry evaluation

**"Low scores across all questions"**:

- **Cause**: Prompt issues, poor documentation, or model problems
- **Solution**: Review prompts, check documentation quality, test different models

### Debugging Evaluation Runs

**Enable verbose logging**:

```bash
DEBUG=ai:* npm run cli:eval run <eval_file> <subdomain>
```

**Check individual results**:

- Open result JSON file
- Review low-scoring questions
- Compare expected vs. actual answers
- Read judge feedback

**Validate test cases**:

- Manually verify ground truth answers
- Ensure violation markers are correct
- Test with single question first

## Advanced Usage

### Custom Evaluation Workflows

**Automated CI/CD Integration**:

```bash
# Run evaluation and fail if score drops below threshold
npm run cli:eval run ./evals/developers/groundtruths/latest.json developers
# Parse results and exit with error if avgScore < 4.0
```

**Comparative Testing**:

```bash
# Test local changes against production
npm run cli:eval run ./evals/developers/groundtruths/latest.json developers
npm run cli:eval run ./evals/developers/groundtruths/latest.json developers prod
# Compare results to measure impact
```

### Custom Judge Configuration

Modify judge models in evaluation scripts to test different combinations:

- Use multiple judges for consensus scoring
- Test new models as judges
- Compare judge performance and agreement

### Result Analysis Scripts

Create custom scripts to analyze evaluation results:

- Calculate score distributions
- Identify common failure patterns
- Track performance over time
- Generate visualization charts

## Reference

### File Locations

**Chat Evaluations**:

- Ground truth: `evals/<subdomain>/groundtruths/<subdomain>-evals-YYYY-MM-DD.json`
- Results: `evals/<subdomain>/results/<service>-<subdomain>-YYYY-MM-DD.json`

**Linting Evaluations**:

- Test cases: `evals/lint/test-cases/<test-name>/`
- Results: `evals/lint/judge/YYYY-MM-DDTHH-MM-SS-MSSZ/results.md`

### CLI Commands

**Chat**:

```bash
# Create evaluation dataset
npm run cli:eval create <subdomain> [max_evals]

# Run evaluation (local)
npm run cli:eval run <eval_file> <subdomain>

# Run evaluation (production)
npm run cli:eval run <eval_file> <subdomain> prod
```

**Linting**:

```bash
# Run linting evaluation
npm run cli:eval lint
```

### Environment Variables

Required for evaluations:

- `OPENAI_KEY`: OpenAI API access
- `GOOGLE_GENERATIVE_AI_API_KEY`: Google Gemini API access
- `AI_MONGO_URI`: MongoDB connection string (for vectorization)
- `README_DOMAIN`: ReadMe API domain (for production evals)
- `AI_TOKEN`: Authentication token
