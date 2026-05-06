# Contributing to CyberSense

Thank you for considering contributing to CyberSense! This document provides guidelines for contributing to the project.

---

## 🤝 How to Contribute

### 1. Fork the Repository

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/yourusername/CyberSense-CSE445.git
cd CyberSense-CSE445
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-description
```

### 3. Make Your Changes

Follow the coding standards and best practices outlined below.

### 4. Test Your Changes

```bash
# Backend tests
cd backend
python -m pytest tests/

# Manual testing
python app/main.py
# Test in browser
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
# Follow conventional commits format
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
# Create PR on GitHub
```

---

## 📋 Contribution Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters
- Use meaningful variable names

Example:
```python
def predict_text(text: str) -> dict:
    """
    Predict if text contains cyberbullying.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with prediction and confidence
    """
    # Implementation
    pass
```

#### JavaScript (Frontend)
- Use ES6+ features
- Use const/let instead of var
- Add comments for complex logic
- Use meaningful function names

Example:
```javascript
/**
 * Analyze text for cyberbullying
 * @param {string} text - Text to analyze
 * @returns {Promise<Object>} Prediction result
 */
async function analyzeText(text) {
    // Implementation
}
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add batch prediction endpoint
fix: resolve CORS issue with Vercel
docs: update deployment instructions
test: add preprocessing unit tests
```

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why
3. **Tests**: Include tests for new features
4. **Documentation**: Update docs if needed
5. **Screenshots**: For UI changes

PR Template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

---

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Test on latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 96]
- Python Version: [e.g., 3.11]
- Backend URL: [e.g., localhost:5000]

**Additional Context**
Any other relevant information
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this solve?

**Proposed Solution**
How would this work?

**Alternatives Considered**
Other solutions you've thought of

**Additional Context**
Mockups, examples, etc.
```

---

## 🧪 Testing Guidelines

### Backend Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_api.py

# Run with coverage
python -m pytest --cov=app --cov-report=html
```

### Writing Tests

```python
def test_feature_name():
    """Test description"""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### Frontend Tests

- Manual testing checklist
- Browser console checks
- Network tab validation
- Responsive design testing

---

## 📚 Documentation

### Where to Document

- **Code**: Docstrings and comments
- **README.md**: High-level overview
- **API**: Endpoint documentation
- **Guides**: DEPLOYMENT.md, TESTING.md, etc.

### Documentation Style

- Clear and concise
- Include examples
- Keep up to date
- Use proper formatting

---

## 🎯 Areas to Contribute

### Backend
- [ ] Add more ML models
- [ ] Improve preprocessing
- [ ] Add caching layer
- [ ] Rate limiting
- [ ] Authentication
- [ ] Database integration

### Frontend
- [ ] UI/UX improvements
- [ ] Dark/light mode toggle
- [ ] Accessibility features
- [ ] Multi-language support
- [ ] Data visualization
- [ ] Export results

### Documentation
- [ ] Video tutorials
- [ ] More examples
- [ ] Troubleshooting guide
- [ ] API documentation
- [ ] Architecture diagrams

### Testing
- [ ] More unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance tests
- [ ] Security tests

### DevOps
- [ ] CI/CD improvements
- [ ] Docker optimization
- [ ] Monitoring setup
- [ ] Logging improvements
- [ ] Deployment guides

---

## 🚫 What NOT to Contribute

- Breaking changes without discussion
- Code that doesn't follow style guide
- Features without tests
- Incomplete implementations
- Copyrighted code
- Malicious code

---

## 📞 Getting Help

- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: your.email@example.com

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive Behavior:**
- Being respectful
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy

**Unacceptable Behavior:**
- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

---

## 🎓 Learning Resources

### Python/Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Style Guide](https://pep8.org/)

### Machine Learning
- [Scikit-learn Docs](https://scikit-learn.org/)
- [NLTK Documentation](https://www.nltk.org/)

### Frontend
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript Guide](https://javascript.info/)

### Git
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)

---

## ⭐ Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in commits

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CyberSense! 🛡️
