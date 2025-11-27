# Contributing Guidelines

Welcome! We appreciate your interest in contributing to Verridian AI.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Set up** the development environment (see [Development Guide](Development-Guide))
4. **Create** a feature branch
5. **Make** your changes
6. **Test** your changes
7. **Submit** a pull request

---

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a welcoming environment

---

## Types of Contributions

### Bug Reports

File an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

```markdown
## Bug Report

**Description**: [What's wrong]

**Steps to Reproduce**:
1. Run `python script.py`
2. Enter query "..."
3. Observe error

**Expected**: [What should happen]

**Actual**: [What actually happens]

**Environment**:
- OS: Windows 11
- Python: 3.10.12
- Node: 18.17.0
```

### Feature Requests

File an issue with:
- Use case description
- Proposed solution
- Alternatives considered

### Documentation

- Fix typos or unclear explanations
- Add examples
- Improve wiki pages

### Code Contributions

- Bug fixes
- New features
- Performance improvements
- Test coverage

---

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Follow code style guidelines
- Add tests for new features
- Update documentation as needed

### 3. Test Changes

```bash
# Python tests
pytest tests/

# Type checking
mypy src/

# Frontend
cd ui && npm run lint && npm run type-check
```

### 4. Commit Changes

Use conventional commits:

```bash
git commit -m "feat(gsw): add actor relationship query"
git commit -m "fix(api): handle streaming timeout"
git commit -m "docs(wiki): add Contributing page"
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance

### 5. Push and Create PR

```bash
git push origin feature/my-feature
```

Then open a Pull Request on GitHub with:
- Clear title
- Description of changes
- Link to related issues
- Screenshots if UI changes

---

## Code Style

### Python

```python
"""
Module docstring.

Detailed description of what this module does.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel


class MyClass(BaseModel):
    """
    Class docstring.

    Attributes:
        name: Description of name
        value: Description of value
    """
    name: str
    value: int = 0

    def my_method(self, param: str) -> List[str]:
        """
        Method docstring.

        Args:
            param: Description of param

        Returns:
            Description of return value
        """
        pass
```

### TypeScript

```typescript
/**
 * Interface description.
 */
interface MyInterface {
    /** Field description */
    name: string;
    /** Optional field */
    value?: number;
}

/**
 * Function description.
 * @param param - Parameter description
 * @returns Return value description
 */
export function myFunction(param: string): MyInterface[] {
    // Implementation
}
```

---

## Testing Guidelines

### Python Tests

```python
# tests/test_gsw.py
import pytest
from src.gsw.workspace import WorkspaceManager

def test_workspace_load():
    """Test workspace loading from JSON."""
    manager = WorkspaceManager.load(Path("test_data/workspace.json"))
    assert manager.workspace is not None

def test_actor_query():
    """Test querying actors by role."""
    manager = WorkspaceManager()
    # Setup...
    results = manager.query_actors_by_role("applicant")
    assert len(results) > 0
```

### Frontend Tests

```typescript
// ui/src/components/chat/ChatMessage.test.tsx
import { render, screen } from '@testing-library/react';
import { ChatMessage } from './ChatMessage';

test('renders user message', () => {
    render(<ChatMessage message={{ role: 'user', content: 'Hello' }} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

---

## Documentation

### Wiki Pages

When adding wiki pages:
- Use clear headings
- Include code examples
- Add mermaid diagrams where helpful
- Link to related pages
- Update `_Sidebar.md` if adding new pages

### Code Comments

```python
# Good: Explains WHY
# Use TOON format for 40% token reduction in prompts
context = workspace.to_toon()

# Bad: Explains WHAT (obvious from code)
# Convert to TOON
context = workspace.to_toon()
```

---

## Review Process

1. **Automated checks** run on PR
2. **Maintainer review** within 48 hours
3. **Address feedback** if requested
4. **Approval** and merge

### What We Look For

- Code follows style guidelines
- Tests pass and cover new code
- Documentation is updated
- No breaking changes without discussion
- Performance impact considered

---

## Release Process

Releases follow semantic versioning:
- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)
- **Discussions**: GitHub Discussions (if enabled)
- **Wiki**: [Project Wiki](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki)

---

## Recognition

Contributors are recognized in:
- Release notes
- Contributors list

Thank you for contributing to Verridian AI!

---

## Related Pages

- [Development-Guide](Development-Guide) - Setup instructions
- [Quick-Start](Quick-Start) - Getting started
- [Architecture-Overview](Architecture-Overview) - System design
