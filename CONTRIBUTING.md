# Contributing to Pocketbook Highlights Sync

Thank you for considering contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to see if the bug has already been reported
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your system info (macOS version, Python version, Pocketbook model)
   - Error messages or logs if applicable

### Suggesting Features

1. **Open a discussion** first to gauge interest
2. **Create an issue** describing:
   - The problem the feature would solve
   - Proposed solution
   - Alternative approaches considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**:
   - Manually test with a Pocketbook device
   - Ensure no regressions
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots if UI changes

## Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/heissjl/pocketbook-sync.git
   cd pocketbook-sync
   ```

2. **Run the setup wizard**:
   ```bash
   python3 setup.py
   ```

3. **Test your changes**:
   ```bash
   python3 sync_highlights.py
   ```

## Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where helpful

## Project Structure

```
pocketbook-sync/
├── sync_highlights.py      # Main sync script
├── setup.py                # Setup wizard
├── inspect_db.py           # Database inspection tool
├── README.md               # Main documentation
├── SETUP_PROMPT.md         # Claude Code setup guide
├── CONTRIBUTING.md         # This file
├── LICENSE                 # MIT license
├── .gitignore              # Git ignore patterns
└── Pocketbook Sync.app/    # macOS application bundle
    └── Contents/
        ├── Info.plist
        └── MacOS/
            └── launch
```

## Testing

Since this tool interacts with hardware (Pocketbook e-reader) and various software (Calibre, note-taking apps), testing can be challenging:

### Manual Testing Checklist

- [ ] Fresh setup wizard completes successfully
- [ ] Auto-detection finds Pocketbook, Calibre, and vault
- [ ] Sync extracts highlights correctly
- [ ] Markdown files are properly formatted
- [ ] Calibre links work (show-book and view-book)
- [ ] Page numbers are extracted correctly
- [ ] Multiple books sync without errors
- [ ] Configuration persists across runs

### Test Cases

1. **First-time setup** - no config exists
2. **Reconfiguration** - config already exists
3. **Missing Pocketbook** - device not connected
4. **No Calibre** - skipping integration works
5. **Different note apps** - Obsidian, Logseq, etc.
6. **Books without highlights** - handled gracefully
7. **Special characters in titles** - filename sanitization

## Adding Support for New E-Readers

To add support for other e-readers:

1. Research the database schema (usually SQLite)
2. Identify where highlights are stored
3. Create a new extraction function
4. Add device detection logic
5. Update documentation

## Documentation

When making changes:

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Update SETUP_PROMPT.md if setup process changes

## Questions?

- Open a discussion for general questions
- Tag maintainers in issues for clarification
- Check existing issues and PRs for similar topics

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing! 🎉
