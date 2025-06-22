#!/bin/bash

# EasyFinance CI/CD Pipeline - Git Commit Script
# This script helps you commit all the CI/CD changes with proper commit messages

set -e  # Exit on any error

echo "🚀 EasyFinance CI/CD Pipeline - Git Commit Helper"
echo "=================================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Check for uncommitted changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "✅ No changes to commit. All files are already committed."
    exit 0
fi

echo "📋 Available commit strategies:"
echo "1. Granular commits (9 separate commits - recommended for teams)"
echo "2. Single comprehensive commit (1 commit - good for personal projects)"
echo "3. Cancel"
echo ""

read -p "Choose option (1, 2, or 3): " choice

case $choice in
    1)
        echo ""
        echo "🔄 Creating granular commits..."
        echo ""
        
        # Commit 1: Project Configuration
        echo "📝 Commit 1/9: Project configuration..."
        git add pyproject.toml pytest.ini
        git commit -m "feat: add project configuration with pyproject.toml and pytest.ini

- Add comprehensive pyproject.toml with build system, project metadata, and tool configurations
- Configure Black (88 char line length), isort (black profile), pytest, coverage, mypy, pylint, bandit
- Set up pytest.ini with test discovery, markers, and asyncio support
- Define project dependencies and optional dev/test dependency groups
- Configure coverage reporting with 80% minimum threshold"
        
        # Commit 2: Makefile
        echo "📝 Commit 2/9: Development workflow automation..."
        git add Makefile
        git commit -m "feat: add comprehensive Makefile for development workflow

- Add 50+ make targets for development, testing, building, and CI/CD
- Include installation targets for prod, dev, and test dependencies
- Add code quality targets: lint, format, format-check, security
- Add testing targets: test, test-cov, test-unit, test-integration
- Add building targets: build, docker-build, clean
- Add CI/CD targets: ci-lint, ci-test, ci-build, ci-full
- Add utility targets: check, fix, upgrade, info, help"
        
        # Commit 3: Pre-commit
        echo "📝 Commit 3/9: Pre-commit configuration..."
        git add .pre-commit-config.yaml
        git commit -m "feat: enhance pre-commit configuration with comprehensive hooks

- Add trailing-whitespace, end-of-file-fixer, and file format checks
- Configure Black with 88 character line length and Python 3+ support
- Add isort with black profile for import sorting
- Configure flake8 with max-line-length=88 and Black-compatible ignore rules
- Add mypy for type checking with ignore-missing-imports
- Add bandit for security analysis with pyproject.toml config
- Add pylint for advanced code analysis"
        
        # Commit 4: Main CI/CD Pipeline
        echo "📝 Commit 4/9: Main CI/CD pipeline..."
        git add .github/workflows/ci-cd.yml
        git commit -m "feat: implement comprehensive GitHub Actions CI/CD pipeline

- Add main workflow triggered on push/PR to main/develop branches
- Implement lint job with flake8, pylint, and mypy
- Add format job with Black and isort validation
- Configure test job with matrix for Python 3.9, 3.10, 3.11
- Add security job with Bandit and Safety vulnerability scanning
- Implement build job for Python packages with artifact upload
- Add Docker job for container building and testing
- Configure staging deployment for develop branch
- Configure production deployment for main branch
- Add notification job for pipeline status reporting
- Include comprehensive caching strategy for pip dependencies"
        
        # Commit 5: Additional Workflows
        echo "📝 Commit 5/9: Additional GitHub workflows..."
        git add .github/workflows/pre-commit.yml .github/workflows/codeql.yml .github/workflows/release.yml
        git commit -m "feat: add specialized GitHub Actions workflows

- Add pre-commit workflow for automated hook validation
- Implement CodeQL workflow for advanced security analysis with weekly schedule
- Add release workflow for automated releases on version tags
- Configure PyPI publishing with PYPI_API_TOKEN secret
- Add Docker Hub publishing with automated image tagging
- Include changelog generation and GitHub release creation"
        
        # Commit 6: Templates
        echo "📝 Commit 6/9: GitHub templates..."
        git add .github/ISSUE_TEMPLATE/ .github/pull_request_template.md 2>/dev/null || true
        git commit -m "feat: add comprehensive GitHub issue and PR templates

- Add bug report template with environment info and reproduction steps
- Add feature request template with use cases and acceptance criteria
- Add security vulnerability template with severity assessment
- Add detailed PR template with type classification and review checklist
- Include testing, security, performance, and compatibility sections
- Add post-merge tasks and reviewer guidelines"
        
        # Commit 7: Dependencies
        echo "📝 Commit 7/9: Updated dependencies..."
        git add src/requirements.txt src/requirements-dev.txt tests/requirements-test.txt
        git commit -m "feat: update project dependencies for CI/CD pipeline

- Upgrade src/requirements.txt with FastAPI, Pydantic, JWT, BCrypt, uvicorn
- Enhance src/requirements-dev.txt with linting and formatting tools
- Add tests/requirements-test.txt with pytest, coverage, and testing utilities
- Pin minimum versions while allowing patch updates
- Include all dependencies needed for comprehensive CI/CD pipeline"
        
        # Commit 8: Test Infrastructure
        echo "📝 Commit 8/9: Test infrastructure..."
        git add tests/run_tests.py tests/test_utils.py
        git commit -m "feat: enhance test infrastructure with utilities and runner

- Add custom test runner using unittest for dependency-free testing
- Create comprehensive test utilities with TestDataFactory, DatabaseTestHelper
- Add TokenTestHelper for JWT testing scenarios
- Include ValidationHelper for common assertions
- Add TempDatabaseContext for isolated database testing
- Provide fallback testing solution for environments with dependency conflicts"
        
        # Commit 9: Documentation
        echo "📝 Commit 9/9: Documentation..."
        git add .github/CICD.md CICD_README.md SETUP_COMPLETE.md GIT_COMMIT_GUIDE.md commit_changes.sh
        git commit -m "docs: add comprehensive CI/CD documentation

- Add .github/CICD.md with technical pipeline documentation
- Create CICD_README.md with user-friendly setup guide and workflow explanations
- Add SETUP_COMPLETE.md with step-by-step completion instructions
- Include troubleshooting guides, environment setup, and best practices
- Document all make targets, workflow triggers, and quality gates
- Provide migration guides and future enhancement roadmap
- Add GIT_COMMIT_GUIDE.md with commit message templates
- Include automated commit script for easy setup"
        
        echo ""
        echo "✅ All 9 commits completed successfully!"
        ;;
        
    2)
        echo ""
        echo "🔄 Creating single comprehensive commit..."
        echo ""
        
        git add .
        git commit -m "feat: implement comprehensive CI/CD pipeline with GitHub Actions

BREAKING CHANGE: Major CI/CD infrastructure addition

- Add GitHub Actions workflows for CI/CD, pre-commit, CodeQL, and releases
- Implement comprehensive code quality gates with linting, formatting, and security scanning
- Add multi-version testing across Python 3.9, 3.10, 3.11 with 80% coverage requirement
- Configure automated deployments to staging (develop) and production (main)
- Add automated release process with PyPI and Docker Hub publishing
- Enhance pre-commit configuration with comprehensive hooks
- Add project configuration with pyproject.toml and tool settings
- Create comprehensive Makefile with 50+ development workflow commands
- Add GitHub issue templates (bug, feature, security) and PR template
- Update dependencies for production, development, and testing
- Add test utilities and alternative test runner for compatibility
- Include comprehensive documentation and setup guides

Features:
- Code quality: Black, isort, flake8, pylint, mypy, bandit
- Security: Vulnerability scanning, secret detection, CodeQL analysis
- Testing: pytest, coverage reporting, async support, multi-version matrix
- Automation: pre-commit hooks, automated releases, dependency updates
- Deployment: staging and production environments with approval gates
- Monitoring: build status, coverage tracking, security alerts"
        
        echo ""
        echo "✅ Comprehensive commit completed successfully!"
        ;;
        
    3)
        echo ""
        echo "❌ Cancelled. No commits were made."
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ Invalid option. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "🎉 Git commits completed!"
echo ""
echo "📋 Next steps:"
echo "1. Review your git log: git log --oneline"
echo "2. Push to your repository: git push origin main"
echo "3. Set up GitHub repository secrets for full CI/CD functionality"
echo "4. Create 'develop' branch: git checkout -b develop && git push -u origin develop"
echo ""
echo "📚 For detailed setup instructions, see SETUP_COMPLETE.md"
echo "📖 For CI/CD documentation, see CICD_README.md"
