# Security Policy

## Account compromise

Suspected account takeover, credential theft, suspicious access, or unauthorized privileged activity is a security-sensitive case and must be escalated.

## API secrets

CloudDesk never displays an existing private API secret to support agents or customers after creation.

If a key is lost:
1. Authenticate normally.
2. Revoke the compromised/lost key if appropriate.
3. Create a replacement key.
4. Update the integration.

## Identity verification

Before sensitive changes such as ownership changes, security-setting changes, or privileged account modifications, the requester must be verified through the supported account-verification process.

## Enterprise security

Requests involving SAML, audit logs, retention controls, contractual security requirements, or security incidents for Enterprise customers should be escalated when they require privileged or contractual action.
