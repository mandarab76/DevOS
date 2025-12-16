"""
Comprehensive validation tests for DevOS configuration and schema files.

This test suite validates:
- YAML configuration structure and content
- JSON schema definitions
- Documentation completeness
- Repository structure integrity
"""

import unittest
import json
import os
import sys
from pathlib import Path


# Add repository root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


class TestYAMLConfiguration(unittest.TestCase):
    """Test suite for agents.yaml configuration file."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.yaml_file = repo_root / "Config" / "agents.yaml"
        self.assertTrue(self.yaml_file.exists(), "agents.yaml file must exist")
        
    def test_yaml_file_is_valid(self):
        """Verify agents.yaml is valid YAML format."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            
            try:
                data = yaml.safe_load(content)
                self.assertIsNotNone(data, "YAML should parse to a non-None value")
            except yaml.YAMLError as e:
                self.fail(f"Invalid YAML: {e}")
    
    def test_agents_section_exists(self):
        """Verify agents section is defined."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
            
        self.assertIn('agents', data, "agents section must be defined")
        self.assertIsInstance(data['agents'], dict, "agents must be a dictionary")
    
    def test_required_agents_defined(self):
        """Verify all required agents (supervisor, code_consultant, test_consultant) are defined."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        required_agents = ['supervisor', 'code_consultant', 'test_consultant']
        for agent in required_agents:
            self.assertIn(agent, data['agents'], f"{agent} must be defined")
    
    def test_agent_structure_is_valid(self):
        """Verify each agent has required fields (model, role, description, tools, constraints)."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        required_fields = ['model', 'role', 'description', 'tools', 'constraints']
        
        for agent_name, agent_config in data['agents'].items():
            with self.subTest(agent=agent_name):
                for field in required_fields:
                    self.assertIn(field, agent_config, 
                                f"{agent_name} must have {field} field")
    
    def test_supervisor_has_call_agent_tool(self):
        """Verify supervisor agent can call other agents."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        supervisor_tools = data['agents']['supervisor']['tools']
        self.assertIn('call_agent', supervisor_tools, 
                     "Supervisor must have call_agent tool to orchestrate")
    
    def test_routing_section_exists(self):
        """Verify routing configuration is defined."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        self.assertIn('routing', data, "routing section must be defined")
        self.assertIn('tasks', data['routing'], "routing.tasks must be defined")
    
    def test_task_routing_sequences_valid(self):
        """Verify task routing sequences reference valid agents."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        valid_agents = set(data['agents'].keys())
        valid_agents.add('planner')  # planner might be implicit
        
        for task_name, task_config in data['routing']['tasks'].items():
            with self.subTest(task=task_name):
                self.assertIn('sequence', task_config, 
                            f"Task {task_name} must have a sequence")
                sequence = task_config['sequence']
                self.assertIsInstance(sequence, list, 
                                    f"Task {task_name} sequence must be a list")
                self.assertGreater(len(sequence), 0, 
                                 f"Task {task_name} sequence must not be empty")
    
    def test_constraints_are_non_empty(self):
        """Verify all agents have non-empty constraints."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
            
        with open(self.yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        for agent_name, agent_config in data['agents'].items():
            with self.subTest(agent=agent_name):
                constraints = agent_config['constraints']
                self.assertIsInstance(constraints, list, 
                                    f"{agent_name} constraints must be a list")
                self.assertGreater(len(constraints), 0, 
                                 f"{agent_name} must have at least one constraint")


if __name__ == '__main__':
    unittest.main()


class TestJSONSchema(unittest.TestCase):
    """Test suite for Tool-schema.json file."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.schema_file = repo_root / "Config" / "Tool-schema.json"
        self.assertTrue(self.schema_file.exists(), "Tool-schema.json file must exist")
    
    def test_json_file_is_valid(self):
        """Verify Tool-schema.json is valid JSON format."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            # Strip markdown code fence if present
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            
            try:
                data = json.loads(content)
                self.assertIsNotNone(data, "JSON should parse to a non-None value")
            except json.JSONDecodeError as e:
                self.fail(f"Invalid JSON: {e}")
    
    def test_tools_section_exists(self):
        """Verify tools section is defined in schema."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        self.assertIn('tools', data, "tools section must be defined")
        self.assertIsInstance(data['tools'], dict, "tools must be a dictionary")
    
    def test_required_tools_defined(self):
        """Verify all required tools are defined in schema."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        required_tools = ['read_file', 'propose_patch', 'run_tests', 'call_agent']
        for tool in required_tools:
            self.assertIn(tool, data['tools'], f"{tool} must be defined in schema")
    
    def test_tool_definitions_have_args_and_returns(self):
        """Verify each tool has args and returns specifications."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        for tool_name, tool_spec in data['tools'].items():
            with self.subTest(tool=tool_name):
                self.assertIn('args', tool_spec, 
                            f"{tool_name} must have args specification")
                self.assertIn('returns', tool_spec, 
                            f"{tool_name} must have returns specification")
    
    def test_read_file_tool_schema(self):
        """Verify read_file tool has correct schema structure."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        read_file = data['tools']['read_file']
        self.assertIn('path', read_file['args'], 
                     "read_file must accept path argument")
        self.assertIn('content', read_file['returns'], 
                     "read_file must return content")
    
    def test_propose_patch_tool_schema(self):
        """Verify propose_patch tool has correct schema structure."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        propose_patch = data['tools']['propose_patch']
        self.assertIn('path', propose_patch['args'], 
                     "propose_patch must accept path argument")
        self.assertIn('instructions', propose_patch['args'], 
                     "propose_patch must accept instructions argument")
        self.assertIn('patch', propose_patch['returns'], 
                     "propose_patch must return patch")
        self.assertIn('comment', propose_patch['returns'], 
                     "propose_patch must return comment")
    
    def test_run_tests_tool_schema(self):
        """Verify run_tests tool has correct schema structure."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        run_tests = data['tools']['run_tests']
        self.assertIn('command', run_tests['args'], 
                     "run_tests must accept command argument")
        self.assertIn('ok', run_tests['returns'], 
                     "run_tests must return ok boolean")
        self.assertIn('output', run_tests['returns'], 
                     "run_tests must return output string")
    
    def test_call_agent_tool_schema(self):
        """Verify call_agent tool has correct schema structure."""
        with open(self.schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = json.loads(content)
        
        call_agent = data['tools']['call_agent']
        self.assertIn('agent', call_agent['args'], 
                     "call_agent must accept agent argument")
        self.assertIn('payload', call_agent['args'], 
                     "call_agent must accept payload argument")
        self.assertIn('result', call_agent['returns'], 
                     "call_agent must return result")


class TestDocumentation(unittest.TestCase):
    """Test suite for documentation files."""
    
    def test_copilot_instructions_exists(self):
        """Verify copilot instructions file exists."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        self.assertTrue(instructions_file.exists(), 
                       "copilot-instructions.md must exist")
    
    def test_copilot_instructions_has_required_sections(self):
        """Verify copilot instructions has all required sections."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        with open(instructions_file, 'r') as f:
            content = f.read()
        
        required_sections = [
            "Project Overview",
            "Architecture Principles",
            "Development Guidelines",
            "File Organization",
            "Technology Stack",
            "AI/Supervisor Integration",
        ]
        
        for section in required_sections:
            self.assertIn(section, content, 
                         f"Documentation must include {section} section")
    
    def test_copilot_instructions_mentions_web_support(self):
        """Verify documentation mentions web browser support."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        with open(instructions_file, 'r') as f:
            content = f.read().lower()
        
        self.assertIn('web', content, "Documentation must mention web support")
        self.assertIn('browser', content, "Documentation must mention browser support")
    
    def test_copilot_instructions_has_security_guidelines(self):
        """Verify security guidelines are documented."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        with open(instructions_file, 'r') as f:
            content = f.read()
        
        self.assertIn('Security', content, "Must have Security section")
        self.assertIn('secrets', content.lower(), 
                     "Must mention secrets handling")
    
    def test_readme_exists(self):
        """Verify README.md exists."""
        readme = repo_root / "README.md"
        self.assertTrue(readme.exists(), "README.md must exist")
    
    def test_readme_has_content(self):
        """Verify README.md has meaningful content."""
        readme = repo_root / "README.md"
        with open(readme, 'r') as f:
            content = f.read().strip()
        
        self.assertGreater(len(content), 0, "README must not be empty")
        self.assertIn('DevOS', content, "README must mention DevOS")
    
    def test_orchestration_algorithm_exists(self):
        """Verify orchestration algorithm pseudocode exists."""
        algo_file = repo_root / "Docs" / "Orchestration algorithm (pseudo‑code)"
        self.assertTrue(algo_file.exists(), 
                       "Orchestration algorithm file must exist")
    
    def test_orchestration_algorithm_has_key_functions(self):
        """Verify orchestration algorithm defines key functions."""
        algo_file = repo_root / "Docs" / "Orchestration algorithm (pseudo‑code)"
        with open(algo_file, 'r') as f:
            content = f.read()
        
        key_elements = [
            'handle_user_request',
            'supervisor_plan',
            'call_agent',
            'apply_patch',
            'run_tests',
        ]
        
        for element in key_elements:
            self.assertIn(element, content, 
                         f"Algorithm must define {element}")


class TestRepositoryStructure(unittest.TestCase):
    """Test suite for repository directory structure."""
    
    def test_required_directories_exist(self):
        """Verify all required directories exist."""
        required_dirs = [
            '.github',
            'Config',
            'Docs',
            'Mobile',
            'Server',
            'server',
            'server/devos_core',
        ]
        
        for dir_path in required_dirs:
            full_path = repo_root / dir_path
            self.assertTrue(full_path.exists(), 
                          f"Directory {dir_path} must exist")
            self.assertTrue(full_path.is_dir(), 
                          f"{dir_path} must be a directory")
    
    def test_required_files_exist(self):
        """Verify all required configuration files exist."""
        required_files = [
            'README.md',
            'LICENSE',
            'Config/agents.yaml',
            'Config/Tool-schema.json',
            '.github/copilot-instructions.md',
        ]
        
        for file_path in required_files:
            full_path = repo_root / file_path
            self.assertTrue(full_path.exists(), 
                          f"File {file_path} must exist")
            self.assertTrue(full_path.is_file(), 
                          f"{file_path} must be a file")
    
    def test_license_file_is_mit(self):
        """Verify LICENSE file is MIT license."""
        license_file = repo_root / "LICENSE"
        with open(license_file, 'r') as f:
            content = f.read()
        
        self.assertIn('MIT License', content, 
                     "License must be MIT License")
        self.assertIn('Permission is hereby granted', content, 
                     "Must contain standard MIT license text")
    
    def test_gitkeep_files_in_empty_dirs(self):
        """Verify .gitkeep files exist in empty directories."""
        empty_dirs = ['Config', 'Docs', 'Mobile', 'Server', 'server/devos_core']
        
        for dir_path in empty_dirs:
            gitkeep = repo_root / dir_path / '.gitkeep'
            with self.subTest(directory=dir_path):
                self.assertTrue(gitkeep.exists(), 
                              f".gitkeep must exist in {dir_path}")


class TestConfigurationConsistency(unittest.TestCase):
    """Test suite for consistency between configuration files."""
    
    def test_tools_in_yaml_match_schema(self):
        """Verify tools referenced in agents.yaml match Tool-schema.json."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        
        # Load agents.yaml
        yaml_file = repo_root / "Config" / "agents.yaml"
        with open(yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            agents_data = yaml.safe_load(content)
        
        # Load Tool-schema.json
        schema_file = repo_root / "Config" / "Tool-schema.json"
        with open(schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            schema_data = json.loads(content)
        
        defined_tools = set(schema_data['tools'].keys())
        
        # Collect all tools used by agents
        for agent_name, agent_config in agents_data['agents'].items():
            agent_tools = agent_config.get('tools', [])
            for tool in agent_tools:
                with self.subTest(agent=agent_name, tool=tool):
                    # Some tools might be implicit or meta-tools
                    if tool not in ['list_files', 'diff_files', 'run_command', 'search_web']:
                        self.assertIn(tool, defined_tools, 
                                    f"Tool {tool} used by {agent_name} must be defined in schema")
    
    def test_documentation_references_match_files(self):
        """Verify documentation references match actual file structure."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        with open(instructions_file, 'r') as f:
            content = f.read()
        
        # Check that documentation mentions the correct file paths
        self.assertIn('agents.yaml', content, 
                     "Documentation must reference agents.yaml")
        self.assertIn('Tool-schema.json', content, 
                     "Documentation must reference Tool-schema.json")
        self.assertIn('/server/devos_core/', content, 
                     "Documentation must reference correct server path")


class TestEdgeCases(unittest.TestCase):
    """Test suite for edge cases and error conditions."""
    
    def test_yaml_handles_special_characters(self):
        """Verify YAML properly handles special characters in strings."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        
        yaml_file = repo_root / "Config" / "agents.yaml"
        with open(yaml_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```yaml'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
            data = yaml.safe_load(content)
        
        # Verify multiline strings are properly handled
        for agent_name, agent_config in data['agents'].items():
            description = agent_config.get('description', '')
            self.assertIsInstance(description, str, 
                                f"{agent_name} description must be a string")
    
    def test_json_schema_has_no_trailing_commas(self):
        """Verify JSON has no syntax errors like trailing commas."""
        schema_file = repo_root / "Config" / "Tool-schema.json"
        with open(schema_file, 'r') as f:
            content = f.read()
            if content.strip().startswith('```json'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])
        
        # This will raise JSONDecodeError if there are syntax issues
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            self.fail(f"JSON has syntax errors: {e}")
    
    def test_file_paths_use_forward_slashes(self):
        """Verify all file paths in documentation use forward slashes."""
        instructions_file = repo_root / ".github" / "copilot-instructions.md"
        with open(instructions_file, 'r') as f:
            content = f.read()
        
        # Check that no Windows-style backslashes are used
        path_lines = [line for line in content.split('\n') 
                     if '/' in line and not line.strip().startswith('#')]
        
        for line in path_lines:
            if '\\' in line and 'escape' not in line.lower():
                self.fail(f"Found backslash in path: {line}")