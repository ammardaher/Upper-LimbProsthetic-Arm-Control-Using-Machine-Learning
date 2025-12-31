# Contributing to EMG-Based Prosthesis Control

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow
- Report issues constructively

## How to Contribute

### 1. Report Bugs
- Use GitHub Issues with descriptive titles
- Include reproduction steps
- Attach relevant logs or data
- Specify your hardware/OS configuration

**Bug Report Template:**
```
## Description
[Clear description of the bug]

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [Windows/Linux/Mac]
- Python Version: 3.x.x
- Arduino Board: [Uno/Mega]
- MYO SDK Version: x.x.x

## Logs/Error Messages
[Paste relevant error output]
```

### 2. Suggest Features
- Use GitHub Discussions for major features
- Provide use cases and examples
- Consider performance implications
- Explain why it would be beneficial

**Feature Request Template:**
```
## Feature Description
[Clear description]

## Use Case
[What problem does it solve?]

## Implementation Approach
[Suggested approach, if any]

## Alternatives Considered
[Other solutions]
```

### 3. Submit Code Changes

#### Setup Development Environment
```bash
# Clone your fork
git clone https://github.com/yourusername/emg-prosthesis-control.git
cd emg-prosthesis-control

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in development mode
pip install -e ".[dev]"
pip install -r requirements.txt
```

#### Make Changes
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make focused, logical commits
3. Write clear commit messages
4. Add tests for new functionality
5. Update documentation as needed

#### Commit Message Guidelines
```
Short summary (50 chars or less)

More detailed explanation if necessary. Wrap at 72 characters.

Fixes #issue_number
```

Examples:
```
Add EMG signal normalization feature
Improves classification accuracy by 2-3%

Fixes #42
```

```
Fix servo motor jitter during transitions
Implement smoothing algorithm for angle changes

Closes #38
```

#### Write Tests
- Add unit tests for new functionality
- Ensure all tests pass: `pytest tests/`
- Aim for >80% code coverage: `pytest --cov=python tests/`
- Test both happy path and edge cases

**Test Example:**
```python
import pytest
from python.emg_classifier import EMGClassifier

def test_classifier_accuracy():
    clf = EMGClassifier()
    clf.load_model('models/decision_tree_model.pkl')
    
    # Test data
    predictions = clf.predict(test_signals)
    accuracy = (predictions == test_labels).mean()
    
    assert accuracy > 0.97
```

#### Create Pull Request
1. Push to your fork: `git push origin feature/your-feature-name`
2. Open a Pull Request on GitHub
3. Use the PR template and fill in all sections
4. Reference related issues: `Fixes #123`
5. Wait for reviews and address feedback

**PR Template:**
```
## Description
[What changes are being made?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Tested manually
- [ ] All tests pass

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commits are clean

## Screenshots/Logs (if applicable)
[Attach images or output]
```

### 4. Documentation Contributions

#### Python Code
- Use clear variable and function names
- Add docstrings in Google style format
- Include type hints

```python
def extract_emg_features(signal: np.ndarray, 
                         sampling_rate: int = 200) -> np.ndarray:
    """
    Extract features from raw EMG signal.
    
    Args:
        signal: Raw EMG signal array (N samples,)
        sampling_rate: Signal sampling rate in Hz (default: 200)
    
    Returns:
        Feature vector of shape (n_features,)
    
    Raises:
        ValueError: If signal is empty
    """
```

#### Markdown Files
- Use clear headings
- Include code examples where relevant
- Keep sentences concise
- Check for typos

#### Arduino Code
- Add inline comments for non-obvious logic
- Use meaningful variable names
- Follow Arduino style guide

### 5. Code Style

**Python**
- Follow PEP 8
- Use `black` for formatting: `black python/`
- Use `flake8` for linting: `flake8 python/`
- Use `isort` for imports: `isort python/`

**Arduino**
- Follow Arduino style guide
- Use camelCase for variables
- Add header comments to sketches

## Development Workflow

```
1. Create issue/discussion
2. Fork repository
3. Create feature branch
4. Make changes + tests
5. Run full test suite
6. Submit PR with description
7. Address review feedback
8. Merge when approved
```

## Pull Request Review Process

- At least 1 approval required
- CI/CD pipeline must pass
- All conversations resolved
- Documentation updated

## Community

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Email**: For private concerns

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Credited in release notes
- Mentioned in acknowledgments

## Questions?

- Check existing Issues/PRs
- Read the documentation
- Start a Discussion
- Open an Issue with your question

---

Thank you for making this project better! 🙏
