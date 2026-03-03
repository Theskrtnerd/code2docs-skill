> ## Documentation Index
> Fetch the complete documentation index at: https://www.mintlify.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Playground

> Let developers test API endpoints directly in your documentation.

## Overview

The API playground is an interactive environment that lets users test and explore your API endpoints. Developers can craft API requests, submit them, and view responses without leaving your documentation.

See [Trigger an update](/api/update/trigger) for an example of the API playground in action.

<Frame>
  <img src="https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=f83551b5d84cf27a44ed1d9418ca61be" alt="API playground for the trigger an update endpoint." className="block dark:hidden" data-og-width="2534" width="2534" data-og-height="1022" height="1022" data-path="images/playground/API-playground-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=280&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=87a778f73c13b231ae61b3b3e4ead063 280w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=560&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=fb0ce88ecd599c819dd780738b87c24d 560w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=840&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=e7cf7572fa5fcd7205c8ebcfda839f64 840w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=1100&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=81337643c958f66b3962e16ac569afcd 1100w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=1650&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=94ab7ee928898ec25390934c8897a867 1650w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?w=2500&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=440d9f8a2d8dcbbf55d665d20e6408ed 2500w" />

  <img src="https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=5a0dc3fd3ca0a5766c599c00a5910dba" alt="API playground for the trigger an update endpoint." className="hidden dark:block" data-og-width="2534" width="2534" data-og-height="1022" height="1022" data-path="images/playground/API-playground-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=280&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=e3ffd7bdd28940bc42bff50ffac5b169 280w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=560&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=fdf601c84aeb05836c8e711722fbd2ee 560w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=840&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=45b0f029d05636ca86b99b4d1590ddb3 840w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=1100&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=5e7389355d83faf84d9625c84396868f 1100w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=1650&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=f826d034daefdb906bed0ed0ac6b668e 1650w, https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?w=2500&fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=a530b0340d9ad9a29b72a164fc7dabe5 2500w" />
</Frame>

The playground generates interactive pages for your endpoints based on your OpenAPI specification or AsyncAPI schema. If you modify your API, the playground automatically updates the relevant pages.

We recommend generating your API playground from an OpenAPI specification. However, you can manually create API reference pages after defining a base URL and authentication method in your `docs.json`.

## Get started

<Steps>
  <Step title="Add your OpenAPI specification file.">
    <Tip>
      Validate your OpenAPI specification file using the [Swagger Editor](https://editor.swagger.io/) or [Mint CLI](https://www.npmjs.com/package/mint) command `mint openapi-check <filename>`.
    </Tip>

    ```bash {3} theme={null}
    /your-project
      |- docs.json
      |- openapi.json
    ```
  </Step>

  <Step title="Generate endpoint pages.">
    Update your `docs.json` to reference your OpenAPI specification.

    **To automatically generate pages for all endpoints in your OpenAPI specification**, add an `openapi` property to any navigation element.

    This example generates a page for each endpoint specified in `openapi.json` and organizes the pages in the "API reference" group.

    ```json Generate all endpoint pages theme={null}
    "navigation": {
      "groups": [
        {
          "group": "API reference",
          "openapi": "openapi.json"
        }
      ]
    }
    ```

    **To generate pages for only specific endpoints**, list the endpoints in the `pages` property of the navigation element.

    This example generates pages for only the `GET /users` and `POST /users` endpoints. To generate other endpoint pages, add additional endpoints to the `pages` array.

    ```json Generate specific endpoint pages theme={null}
    "navigation": {
      "groups": [
          {
            "group": "API reference",
            "openapi": "openapi.json",
            "pages": [
              "GET /users",
              "POST /users"
            ]
          }
      ]
    }
    ```
  </Step>
</Steps>

## Customize your playground

Customize your API playground by defining the following properties in your `docs.json`.

<ResponseField name="playground" type="object">
  Configurations for the API playground.

  <Expandable title="playground" defaultOpen="True">
    <ResponseField name="display" type="&#x22;interactive&#x22; | &#x22;simple&#x22; | &#x22;none&#x22; | &#x22;auth&#x22;">
      The display mode of the API playground.

      * `"interactive"`: Display the interactive playground.
      * `"simple"`: Display a copyable endpoint with no playground.
      * `"none"`: Display nothing.
      * `"auth"`: Display the interactive playground only to authenticated users. Unauthenticated users or users not in the required groups see no playground.

      Defaults to `interactive`.
    </ResponseField>

    <ResponseField name="proxy" type="boolean" defaultOpen="True">
      Whether to pass API requests through a proxy server. Defaults to `true`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="examples" type="object">
  Configurations for the autogenerated API examples.

  <Expandable title="examples" defaultOpen="True">
    <ResponseField name="languages" type="array of string">
      Example languages for the autogenerated API snippets.

      Languages display in the order specified.
    </ResponseField>

    <ResponseField name="defaults" type="&#x22;required&#x22; | &#x22;all&#x22;">
      Whether to show optional parameters in API examples. Defaults to `all`.
    </ResponseField>

    <ResponseField name="prefill" type="boolean">
      Whether to prefill the API playground with data from schema examples. When enabled, the playground automatically populates request fields with example values from your OpenAPI specification. Defaults to `false`.
    </ResponseField>

    <ResponseField name="autogenerate" type="boolean">
      Whether to generate code samples for endpoints from API specifications. Defaults to `true`. When set to `false`, only manually-written code samples (from `x-codeSamples` in OpenAPI specifications or `<RequestExample>` components in MDX) appear in the API playground.
    </ResponseField>
  </Expandable>
</ResponseField>

### Example configuration

This example configures the API playground to be interactive with example code snippets for cURL, Python, and JavaScript. Only required parameters are shown in the code snippets, and the playground prefills the request body with example values.

```json  theme={null}
{
 "api": {
   "playground": {
     "display": "interactive"
   },
   "examples": {
     "languages": ["curl", "python", "javascript"],
     "defaults": "required",
     "prefill": true
   }
 }
}
```

### Auth-based playground display

Use the `auth` display mode to show the interactive playground only to authenticated users. This is useful when you want to let users view your API documentation publicly while restricting playground access to logged-in users.

When `display` is set to `auth`:

* Authenticated users see the interactive playground.
* Unauthenticated users see no playground (equivalent to `none`).

You can also combine `auth` with the `groups` property in page frontmatter to restrict playground access to specific user groups.

```mdx Page with group-restricted playground theme={null}
---
title: "Create user"
openapi: POST /users
playground: auth
groups: ["admin", "developer"]
public: true
---
```

In this example:

* The page is publicly visible (anyone can view the documentation).
* Only authenticated users in the `admin` or `developer` groups see the interactive playground.
* Users not in those groups see no playground.

If the page has no `groups` property, all authenticated users see the interactive playground.

<Note>
  The `auth` display mode requires [authentication](/deploy/authentication-setup) to be configured for your documentation.
</Note>

### Custom endpoint pages

When you need more control over your API documentation, use the `x-mint` extension in your OpenAPI specification or create individual MDX pages for your endpoints.

Both options allow you to:

* Customize page metadata
* Add additional content like examples
* Control playground behavior per page

The `x-mint` extension is recommended so that all of your API documentation is automatically generated from your OpenAPI specification and maintained in one file.

Individual MDX pages are recommended for small APIs or when you want to experiment with changes on a per-page basis.

## Further reading

* [OpenAPI setup](/api-playground/openapi-setup) for more information on creating your OpenAPI document.
* [x-mint extension](/api-playground/openapi-setup#x-mint-extension) for more information on customizing your endpoint pages.
* [MDX setup](/api-playground/mdx-setup) for more information on manually creating individual API reference pages.
* [AsyncAPI setup](/api-playground/asyncapi-setup) for more information on creating your AsyncAPI schema to generate WebSocket reference pages.
