# Contributing to HomeBridge

Thank you for your interest in contributing to HomeBridge! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a welcoming, inclusive, and harassment-free environment. We expect all contributors to:
- Be respectful and considerate
- Use inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community

## How to Contribute

1. **Fork the Repository**
   - Fork the repository to your GitHub account
   - Clone your fork locally

2. **Set Up Development Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

5. **Test Your Changes**
   - Ensure all tests pass
   - Test the application locally
   - Verify changes work with different configurations

6. **Submit a Pull Request**
   - Push changes to your fork
   - Create a pull request from your branch to our main branch
   - Describe your changes in detail
   - Reference any related issues

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise

### Testing
- Write unit tests for new features
- Ensure existing tests pass
- Test edge cases and error conditions

### Documentation
- Update README.md if needed
- Document new features or changes
- Include docstrings for new functions
- Update API documentation if applicable

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issue numbers when applicable

## Getting Help

If you need help:
1. Check existing issues and documentation
2. Ask questions in pull requests
3. Contact the maintainers

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Additional Resources

- [Project README](README.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License](LICENSE)

Thank you for contributing to HomeBridge! 