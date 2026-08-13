# @supportpilot/prompts

Version-controlled AI prompts for SupportPilot.

## Purpose

This package holds prompt templates and versions independently from application code. Prompts evolve on a different lifecycle than API routes or UI components — they need review, versioning, and evaluation without redeploying the entire stack.

## Structure

```
prompts/
  └── *.md    # Prompt template files
```

## Usage (future)

In later development steps, the AI engine and API orchestration layer will load prompts from this package. For now, this package contains placeholder content only.

## Guidelines

- One prompt per file, named by purpose (e.g. `ticket-classification.md`).
- Include a brief comment block at the top describing intent and expected inputs.
- Do not embed secrets or customer data in prompt files.
