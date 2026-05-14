# Repository Self-Sufficiency and Surgical Cleanup Guidelines

## Objectives
This repository supports independent, efficient, and high-quality development. All work follows a meticulous, Linear-driven process.

## Automated Commit Message Generation (Implemented)

We now use **Conventional Commits** enforced by commitlint + husky, with Commitizen for interactive generation.

### Setup (One-time)
```bash
npm install
```

### Usage
- Interactive commits: `npm run commit` or `npx git-cz`
- Normal commits are validated automatically via husky pre-commit hook.

All commits must follow the format:
```
[KIM-xxx] <type>: <description>
```

This ensures traceability and professional clarity across the workflow.