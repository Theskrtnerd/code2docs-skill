> ## Documentation Index
> Fetch the complete documentation index at: https://www.mintlify.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

> Start using the agent in your dashboard to create documentation updates.

## Open the agent panel

On desktop, the agent panel is resizable. On mobile devices, the agent opens in full-screen.

To open the agent panel:

* From any page in your dashboard, use the keyboard shortcut <kbd>⌘</kbd>+<kbd>I</kbd> (macOS) or <kbd>Ctrl</kbd>+<kbd>I</kbd> (Windows/Linux).
* On the [Overview](https://dashboard.mintlify.com/) page, click **Ask agent**.

### Agent panel views

<Frame>
  <img src="https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=1681b4b6cd03cf695f5dd6467965acaf" alt="Views in the agent panel: new chat, suggestions, history, and settings." className="block dark:hidden" data-og-width="988" width="988" data-og-height="164" height="164" data-path="images/agent/views-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=280&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=1c3a54c25af66621b73dc0d1ec4ce503 280w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=560&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=9c725ca91b34979cc4faa73fc8fcd66b 560w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=840&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=04687e16f44108d4319b5c27315f8b71 840w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=1100&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=41f1e5aab64480492938984635f33805 1100w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=1650&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=b627bf124483938150819b651eb4b74a 1650w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?w=2500&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=9e0d504ad307e9459422f7ad17ffbc62 2500w" />

  <img src="https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=25f8bac336a0a4bb0624ed8f70303fc3" alt="Views in the agent panel: new chat, suggestions, history, and settings." className="hidden dark:block" data-og-width="988" width="988" data-og-height="166" height="166" data-path="images/agent/views-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=280&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=ce62526f196e7e064e191beb22f05527 280w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=560&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=71ed62f49401c1c1edff9ac069e504f1 560w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=840&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=e44fdd569f5db3e215fb619b41c99571 840w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=1100&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=cd7e750f9d192893267b560e51b18faf 1100w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=1650&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=b5b1e8796ddc94a9c1da6e79e385e99c 1650w, https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?w=2500&fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=e4b369491380e679a40a4dfd8f47c4eb 2500w" />
</Frame>

* **Chat**: Click the plus icon, <Icon icon="plus" />, to start a new chat. In the chat view, send prompts to the agent to update or ask questions about your documentation. The agent creates pull requests based on your instructions and displays links to view the pull requests or open the changes in the web editor.
* **Suggestions**: If enabled, the suggestions panel shows suggested updates to your documentation based on pull request changes and users' conversations with the assistant.
* **History**: Click the history icon, <Icon icon="clock" />, to browse past conversations and continue working on previous requests. Click any conversation to load it in the chat view.
* **Settings**: Click the settings icon, <Icon icon="settings" />, to configure the agent's integrations and repository access.

<Tip>
  Start a new conversation with the agent for each task. This keeps the agent's context focused and helps you associate conversations with specific projects.
</Tip>

## Connect your GitHub account

By default, the agent opens pull requests attributed to the Mintlify bot. To attribute pull requests to you, connect your GitHub account on the [My profile](https://dashboard.mintlify.com/settings/account) page of the dashboard.

## Connect repositories as context

The agent can only access repositories that you connect through the Mintlify GitHub App. Configure which repositories the agent can access in the agent panel **Settings** or in the [GitHub App settings](https://github.com/apps/mintlify/installations/new).
