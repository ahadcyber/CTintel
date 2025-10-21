# Contributing to CTI Dashboard

Thank you for your interest in contributing to the **CTI Dashboard**! This project was developed by **Abdul Ahad Rasool** as a comprehensive threat intelligence platform, and community contributions are welcome to enhance its capabilities.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, MongoDB version)

### Suggesting Features

We welcome feature suggestions! Please create an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   - Ensure all ingestors work
   - Test the web dashboard
   - Verify API endpoints
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Adding New Threat Feeds

To add a new threat intelligence feed:

1. Create a new file in `ingestors/` (e.g., `newfeed.py`)
2. Follow the existing pattern:
   - Import required modules
   - Create a fetch function
   - Format IOCs consistently
   - Handle errors gracefully
3. Add the feed to `run_all.sh` and `run_all.bat`
4. Update README.md with feed details

## Testing

Before submitting a PR:
- Test locally with MongoDB running
- Verify all ingestors fetch data
- Check the dashboard displays correctly
- Test search functionality

## Contact

For questions, collaboration, or security research inquiries:
- 📧 Email: [ahadcyber7@gmail.com](mailto:ahadcyber7@gmail.com)
- 💼 GitHub: [@AbdulAhadRasool](https://github.com/AbdulAhadRasool)
- 🌐 Live Platform: [https://ctintel.onrender.com/](https://ctintel.onrender.com/)

## Questions?

Feel free to open an issue for any questions or discussions!

---

**Thank you for contributing!** 🙏
