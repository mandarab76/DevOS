# DevOS - Developer Operating System

## Project Overview

DevOS is a mobile-first, AI-powered development environment that enables full-featured coding on mobile devices and in the browser. The project consists of:

- **IDE Interface**: A tab-based IDE optimized for phones, tablets, and web browsers
- **Backend Server**: DevOS Core that handles Git, language toolchains, builds, and AI orchestration
- **Supervisor Agent**: Perplexity/Comet-powered AI agent that acts as a guardian and code reviewer

## Architecture Principles

### Core Concepts

1. **Mobile-First Design**: The phone/tablet is a first-class development device, not a toy
2. **Tab-Based UX**: Each function (Editor, Terminal, Git, Supervisor) gets its own tab instead of cramming everything into one screen
3. **Supervisor Pattern**: Comet/Perplexity acts as an always-on reviewer that intervenes when code deviates from best practices
4. **Agent-Based Architecture**: Multiple specialized agents (Supervisor, Code Consultant, Test Consultant) work together

### System Components

- **Client Layer**: Tab-based IDE with offline project storage (mobile via Android/Kotlin, web via browser)
- **DevOS Core** (Backend): Runs on laptop/server/VPS, handles toolchains and AI integration
- **Supervisor Layer**: Perplexity/Comet API integration for reasoning and guardrails

## Development Guidelines

### Code Style

- Write clean, minimal, surgical changes
- Prefer established patterns over novel approaches
- Keep mobile UI responsive and touch-friendly
- Use structured data formats (JSON/YAML) for configuration

### Client Development (Mobile & Web)

- Design for tab-based navigation (swipe between Editor, Terminal, Git, Supervisor tabs)
- Optimize for small screens on mobile - avoid cramming UI elements
- Ensure web version works across modern browsers
- Consider offline-first capabilities
- Use touch-friendly controls on mobile (no tiny buttons)

### Backend Development

- Keep API surface minimal and well-documented
- Use structured prompts and schemas for AI interactions
- Separate project context from web context
- Return typed actions (`{action: "create_file", path: "...", content: "..."}`) not free-form text

### Agent Development

- Agents should have clear, focused roles (refer to `agents.yaml`)
- Use tool schemas defined in `Tool-schema.json`
- Agents should propose changes, not auto-apply them
- Maintain strong system prompts with constraints

### Security

- Never commit secrets to source code
- Use OS keychain or `.env` files for API keys (add to `.gitignore`)
- Validate user actions before execution
- Supervisor should block dangerous operations (e.g., dropping prod DB)

## File Organization

```
/Config          - Configuration files and settings
/Docs            - Documentation and specifications
/Mobile          - Mobile client (Android/Kotlin)
/Server          - Backend DevOS Core service (unused)
/server          - Active backend DevOS Core implementation
  /devos_core    - Core server functionality
/agents.yaml     - Agent definitions and routing rules
/Tool-schema.json - Tool and action schemas
```

## Technology Stack

- **Client**: Android (Kotlin, Jetpack Compose) and Web (browser-based)
- **Backend**: Python or Node.js (implementation in `/server/devos_core/`)
- **AI**: Perplexity/Comet API for reasoning and search
- **Communication**: HTTP/WebSocket between clients and backend
- **Version Control**: Git (built-in integration)

## AI/Supervisor Integration

### Supervisor Role

The Supervisor agent:
- Acts as a blunt, opinionated code reviewer
- Intervenes when code goes off-track
- Triggers on: file saves, test failures, big diffs, explicit review requests
- Provides: critiques, patch proposals, and guardrails

### Intervention Types

1. **Critique**: Points out contract violations or anti-patterns
2. **Patch Proposals**: Structured diffs for auto-apply
3. **Guardrails**: Blocks dangerous operations before execution

### Agent Communication

- Send structured context: current file, recent edits, git diff, test output, user goal
- Expect typed responses with actionable suggestions
- Use tools defined in `Tool-schema.json`
- Route tasks according to `agents.yaml` rules

## Development Workflow

1. **Local Development**: Work in appropriate subdirectory (Mobile, server, etc.)
2. **Testing**: Test changes locally before committing
3. **Agent Testing**: Validate agent prompts and responses
4. **Client Testing**: Test on actual devices/browsers for mobile and web support
5. **Integration**: Ensure clients and backend communicate properly

## Special Considerations

- **Phone Constraints**: Limited screen space, touch input, battery life
- **Browser Compatibility**: Support modern web browsers for the web IDE
- **Offline Support**: IDE should work without constant backend connection
- **Latency**: Minimize round-trips between clients and backend
- **Context Size**: Be mindful of prompt/context limits for AI agents

## Documentation

- Keep README.md updated with setup instructions
- Document API endpoints and schemas
- Maintain agent definitions in `agents.yaml`
- Update tool schemas in `Tool-schema.json` when adding capabilities

## Goals

- Enable professional development on mobile devices and in browsers
- Provide intelligent, context-aware code assistance
- Create a seamless workflow between IDE clients and backend
- Make AI supervision helpful, not intrusive
- Build a system that scales from hobby projects to serious development
