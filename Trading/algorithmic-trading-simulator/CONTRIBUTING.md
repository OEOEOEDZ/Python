# Contributing to Algorithmic Trading Simulator

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- Clear description of the feature
- Use cases and benefits
- Any implementation ideas

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -am 'Add new feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Keep functions focused and small
- Write meaningful variable names

### Testing

- Write unit tests for new features
- Ensure all existing tests pass
- Aim for high test coverage

### Documentation

- Update README.md if needed
- Add docstrings to new code
- Include examples for new features

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithmic-trading-simulator.git
cd algorithmic-trading-simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Questions?

Feel free to open an issue for any questions or discussions.

---

**Author:** Yacine Abdi
