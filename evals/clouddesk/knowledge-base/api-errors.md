# API Errors

401 means authentication is missing or invalid.

403 means authentication succeeded but the caller lacks authorization.

429 means the rate limit was exceeded.

500 indicates a server-side error.

Customers should never include private API keys in support tickets. If credentials may be compromised, rotate them.
