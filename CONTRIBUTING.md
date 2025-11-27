# Contributing to Verridian AI

Thank you for your interest in contributing to Verridian AI! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Functional-Structure-of-Episodic-Memory.git
   cd Functional-Structure-of-Episodic-Memory
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
   ```

## How to Contribute

### Reporting Bugs

- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include steps to reproduce
- Include expected vs actual behavior
- Include environment details (OS, Python version, etc.)

### Suggesting Features

- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the problem you're trying to solve
- Describe your proposed solution
- Consider alternatives you've thought of

### Contributing Code

1. Check existing issues or create a new one
2. Comment on the issue to claim it
3. Fork and create a feature branch
4. Write your code with tests
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Frontend Setup

```bash
cd ui
npm install
npm run dev
```

### Environment Variables

```bash
cp .env.example .env
# Add your API keys
```

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Run tests**:
   ```bash
   pytest tests/
   cd ui && npm test
   ```

3. **Check code style**:
   ```bash
   # Python
   black src/
   flake8 src/

   # TypeScript
   cd ui && npm run lint
   ```

### PR Requirements

- [ ] Clear description of changes
- [ ] Tests for new functionality
- [ ] Documentation updates if needed
- [ ] All tests passing
- [ ] Code follows style guidelines
- [ ] Signed-off commits (DCO)

### Commit Message Format

```
type(scope): brief description

Longer description if needed.

Signed-off-by: Your Name <your.email@example.com>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(gsw): add batch extraction support
fix(vsa): correct similarity calculation
docs(readme): update installation instructions
```

### Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -s -m "Your commit message"
```

This certifies you have the right to submit the code under the project's license.

## Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for public functions

```python
def extract_actors(text: str, context: Optional[str] = None) -> List[Actor]:
    """
    Extract actors from legal text.

    Args:
        text: The legal document text
        context: Optional context for extraction

    Returns:
        List of extracted Actor objects
    """
```

### TypeScript

- Use TypeScript strict mode
- Use functional components with hooks
- Use meaningful variable names

```typescript
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
```

## Architecture Guidelines

When contributing to core modules:

- **GSW (`src/gsw/`)**: Follow the 6-task extraction pattern
- **TEM (`src/tem/`)**: Maintain PyTorch module structure
- **VSA (`src/vsa/`)**: Keep hypervector operations pure
- **Agency (`src/agency/`)**: Follow Active Inference principles

## Questions?

- Open a [Discussion](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/discussions)
- Check the [Wiki](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki)

---

Thank you for contributing!
