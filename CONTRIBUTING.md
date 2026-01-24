# Contributing to Auto EDA Studio Pro

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/auto_eda_chatbot.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install dev dependencies: `pip install -r requirements.txt`

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run the app
streamlit run auto_eda_chatbot/app.py
```

## Coding Standards

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Add comments for complex logic

### Example:
```python
def calculate_statistics(data):
    """
    Calculate basic statistics for numeric columns.
    
    Args:
        data (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary with statistics
    """
    return {
        'mean': data.mean(),
        'std': data.std(),
        'min': data.min(),
        'max': data.max()
    }
```

## Commit Messages

Use clear, descriptive commit messages:
- ✅ `git commit -m "Add correlation heatmap visualization"`
- ❌ `git commit -m "fix bug"`
- ❌ `git commit -m "update"`

## Pull Request Process

1. Update README.md with any new features
2. Test your changes thoroughly
3. Provide clear description of changes
4. Link any related issues
5. Wait for review and address feedback

### PR Template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation

## Testing
Describe tests performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] Comments added
- [ ] Documentation updated
- [ ] Tests pass
```

## Testing

```bash
# Run tests
pytest

# Test specific file
pytest tests/test_auth.py

# Test with coverage
pytest --cov=auto_eda_chatbot
```

## Issue Reporting

Use GitHub Issues to report bugs:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Example:
```markdown
**Describe the bug**
PDF generation fails with large datasets

**Steps to reproduce**
1. Upload CSV with >10k rows
2. Click "Generate PDF"
3. See error message

**Expected behavior**
PDF should generate successfully

**Environment**
- OS: Ubuntu 22.04
- Python: 3.11
- Streamlit: 1.31.0
```

## Feature Requests

Have an idea? Create an issue with the "enhancement" label:
- Describe the feature
- Explain use case
- Suggest implementation (optional)

## Documentation

### Adding Documentation
1. Update README.md for user-facing features
2. Add docstrings in code
3. Update comments if logic changes
4. Consider adding usage examples

### Code Comments
```python
# Bad comment
x = y + 1  # Add one to y

# Good comment
# Increment index to point to next element
current_index = next_index + 1
```

## Performance Considerations

- Avoid large loops in UI rendering
- Cache expensive computations
- Use efficient data structures
- Profile code for bottlenecks

## Security

- Never commit secrets or credentials
- Validate all user inputs
- Use secure authentication methods
- Report security issues privately

## Areas for Contribution

### High Priority
- [ ] Additional visualization types
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] Documentation improvements

### Medium Priority
- [ ] UI/UX enhancements
- [ ] New analysis features
- [ ] Code refactoring
- [ ] Test coverage

### Nice to Have
- [ ] Cloud deployment guides
- [ ] Docker support
- [ ] API endpoints
- [ ] Mobile optimization

## Project Structure

```
auto_eda_chatbot/
├── app.py              # Main app
├── auth.py             # Authentication
├── pdf_generator.py    # PDF creation
├── chat/
│   └── qa_engine.py   # Q&A logic
├── eda/
│   ├── visualizer.py  # Visualizations
│   ├── insights.py    # Analysis
│   └── profiler.py    # Data profiling
├── utils/
│   └── data_loader.py # Data utilities
└── tests/
    ├── test_auth.py
    ├── test_qa.py
    └── test_viz.py
```

## Release Process

1. Update version number
2. Update CHANGELOG
3. Create GitHub release
4. Tag commit: `git tag v1.0.0`
5. Push tags: `git push --tags`

## Questions?

- Check existing issues
- Read documentation
- Create a discussion

---

**Thank you for contributing! 🎉**
