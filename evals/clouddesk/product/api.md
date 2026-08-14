# CloudDesk API

## Authentication

The REST API uses API keys in the `Authorization` header.

Example:

`Authorization: Bearer <API_KEY>`

Never ask a customer to paste a private API key into a support ticket.

## Rate limits

- Starter: 2,000 requests/day
- Professional: 10,000 requests/day
- Enterprise: 100,000 requests/day by default

A rate-limit response is HTTP 429.

## Common errors

- 400: invalid request
- 401: missing/invalid authentication
- 403: authenticated but not authorized
- 404: resource not found
- 409: conflicting state
- 429: rate limit exceeded
- 500: server-side error

## API key rotation

If a key may be compromised:
1. Revoke the affected key.
2. Generate a replacement.
3. Update the calling application.
4. Verify requests succeed.

## Pagination

List endpoints use cursor-based pagination. Clients should follow the documented `next_cursor` value until it is absent.

## Webhooks

Webhook delivery failures should be investigated using endpoint status, response codes, delivery logs, and signing configuration.
