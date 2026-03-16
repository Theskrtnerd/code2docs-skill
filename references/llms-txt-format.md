# llms.txt Format Reference

The llms.txt format is a standard way to provide documentation indexes optimized for LLMs.

## Structure

```
# {Project Name} Documentation

## {Section Title}
{Optional section description paragraph}

- [{Guide Title}]({path/to/guide.md}): {Brief description of what the guide covers}
- [{Guide Title}]({path/to/guide.md})
```

## Rules

- Top-level `#` heading with project name
- `##` headings for sections (Docs, API Reference, Guides, etc.)
- Optional description paragraph after section headings
- Each entry is a markdown list item with `[Title](url): description` format
- Description after `:` is optional but recommended
- URLs point to `.md` files
- Sections group related guides logically

## Examples

### Minimal
```
# Acme Documentation

## Docs

- [Overview](guides/overview.md): High-level introduction to Acme.
- [Getting Started](guides/getting-started.md): Set up and run Acme for the first time.
- [Authentication](guides/authentication.md): Configure API keys and OAuth flows.
```

### With Multiple Sections
```
# Stripe Documentation

## Docs
- [Testing](https://docs.stripe.com/testing.md): Simulate payments to test your integration.
- [API Reference](https://docs.stripe.com/api.md)

## Payment Methods
Acquire more customers by offering popular payment methods.

- [Payment Methods API](https://docs.stripe.com/payments/payment-methods.md): Learn about the API that powers global payment methods.
- [Bank Debits](https://docs.stripe.com/payments/bank-debits.md): Learn how to accept bank debits.
```
