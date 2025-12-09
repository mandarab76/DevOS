# DevOS Configuration Validation Tests

This directory contains comprehensive validation tests for the DevOS project configuration files.

## Overview

The test suite validates:

- **YAML Configuration** (`agents.yaml`): Agent definitions, routing rules, tool specifications
- **JSON Schema** (`Tool-schema.json`): Tool definitions, argument types, return types
- **Documentation** (`.github/copilot-instructions.md`): Completeness, accuracy, required sections
- **Repository Structure**: Directory layout, required files, .gitkeep files
- **Configuration Consistency**: Cross-file references, tool definitions match usage

## Running Tests

### Install Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
python tests/run_tests.py
```

### Run Specific Test Class

```bash
python -m unittest tests.test_configuration_files.TestYAMLConfiguration
```

### Run Specific Test Method

```bash
python -m unittest tests.test_configuration_files.TestYAMLConfiguration.test_yaml_file_is_valid
```

## Test Categories

### TestYAMLConfiguration
Validates the `agents.yaml` file structure, agent definitions, tools, constraints, and routing rules.

**Key Tests:**
- YAML syntax validation
- Required agents (supervisor, code_consultant, test_consultant) are defined
- Agent structure includes model, role, description, tools, constraints
- Supervisor can call other agents
- Routing configuration is valid
- Task sequences reference valid agents

### TestJSONSchema
Validates the `Tool-schema.json` file structure and tool definitions.

**Key Tests:**
- JSON syntax validation
- Required tools (read_file, propose_patch, run_tests, call_agent) are defined
- Each tool has args and returns specifications
- Tool schemas match expected structure

### TestDocumentation
Validates documentation completeness and accuracy.

**Key Tests:**
- Copilot instructions exist and have required sections
- Web/browser support is documented
- Security guidelines are present
- README exists and mentions DevOS
- Orchestration algorithm defines key functions

### TestRepositoryStructure
Validates the directory structure and required files.

**Key Tests:**
- Required directories exist (Config, Docs, Mobile, Server, server/devos_core)
- Required files exist (README.md, LICENSE, agents.yaml, Tool-schema.json)
- LICENSE is MIT license
- .gitkeep files exist in empty directories

### TestConfigurationConsistency
Validates consistency between different configuration files.

**Key Tests:**
- Tools referenced in agents.yaml match Tool-schema.json definitions
- Documentation references match actual file structure

### TestEdgeCases
Tests edge cases and potential error conditions.

**Key Tests:**
- YAML handles special characters properly
- JSON has no syntax errors
- File paths use forward slashes consistently

## Test Coverage

The test suite provides comprehensive validation of:

- **Configuration Syntax**: Ensures all config files are syntactically valid
- **Schema Compliance**: Verifies configurations follow expected schemas
- **Cross-References**: Validates references between files are correct
- **Documentation Accuracy**: Ensures docs match actual implementation
- **Security**: Checks for security-related documentation
- **Edge Cases**: Tests error handling and special cases

## Continuous Integration

These tests are designed to run in CI/CD pipelines to catch configuration errors early.

## Adding New Tests

When adding new configuration files or features:

1. Add validation tests to `test_configuration_files.py`
2. Update this README with test descriptions
3. Ensure tests cover happy paths, edge cases, and error conditions
4. Use descriptive test names that explain what is being validated

## Test Principles

- **Comprehensive**: Cover all configuration files and cross-references
- **Maintainable**: Clear test names and good documentation
- **Fast**: Tests should run quickly for rapid feedback
- **Isolated**: Each test should be independent
- **Informative**: Failures should clearly indicate what's wrong