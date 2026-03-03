# Build with AI

Your docs with built-in AI features that empower readers and writers.

## Writing Tools

AI tools to help you write better docs.

<Grid columns="3" gap="20px" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
  <CoolCard header="Agent" href="https://docs.readme.com/main/docs/aiagent" icon="fa-duotone fa-solid fa-message-bot" isNew text="Edit and review your docs with AI" />

  <CoolCard header="Linter" href="https://docs.readme.com/main/docs/linter" icon="fa-duotone fa-solid fa-wand-sparkles" isNew text="Check for style guide issues as you edit" />

  <CoolCard header="Docs Audit" href="https://docs.readme.com/main/docs/docs-audit" icon="fa-duotone fa-solid fa-brain" isNew text="Score your docs against a custom style guide" />

  <CoolCard />
</Grid>

<br />

## Consuming Docs

AI tools that make your docs easier to read and access.

<Grid columns="3" gap="20px" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
  <CoolCard header="AI Dropdown" href="https://docs.readme.com/main/docs/AskAI" icon="fa-duotone fa-solid fa-square-arrow-up-right" text="Convenient links to leverage AI assistants" />

  <CoolCard header="llms.txt" href="https://docs.readme.com/main/docs/LLMstxt" icon="fa-duotone fa-solid fa-file-magnifying-glass" text="Make your docs LLM-friendly" />

  <CoolCard header="MCP Servers" href="https://docs.readme.com/main/docs/mcp-servers" icon="fa-duotone fa-solid fa-robot" isNew text="Create an MCP server" />

  <CoolCard header="Ask AI" href="https://docs.readme.com/main/docs/ask-ai" icon="fa-duotone fa-solid fa-comment-captions" isNew text="Ask questions about the docs" />
</Grid>

<br />

## FAQ

<Accordion title="Are AI features enabled by default, or do I need to activate them manually?" icon="fa-toggle-off">
  You have full control over enabling or disabling AI features such as Ask AI, MCP, and LLMs.txt. Agent, Linter, and Docs Audit features do not process or ingest any of your documentation unless they are actively used.
</Accordion>

<Accordion title="What happens to my data when using AI features?" icon="fa-chart-simple">
  Our Ask AI and Agent features are powered by OpenAI’s APIs. When used, your Markdown content and API definitions are sent to OpenAI to generate answers. OpenAI retains logs of these API requests for 30 days, but this data is not used to train their AI models.

  Our Linter and Docs Audit use Gemini 2.5 Flash and do not use your data for training.
</Accordion>