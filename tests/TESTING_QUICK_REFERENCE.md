# Testing Quick Reference Guide

A quick lookup guide for testing the Game Generation Engine.

## Files Created

| File | Purpose |
|------|---------|
| `test_game_engine.py` | 45+ unit and integration tests |
| `test_api_endpoints.py` | 35+ API endpoint tests |
| `test_integration_system.py` | 20+ integration and system tests |
| `TEST_GUIDE.md` | Complete testing documentation |
| `MANUAL_TESTING.md` | Manual testing procedures |
| `TESTING_QUICK_REFERENCE.md` | This file |

## Quick Start

### 1. Install Test Dependencies
```bash
pip install pytest pytest-cov pytest-mock
```

### 2. Run All Tests
```bash
pytest -v
```

### 3. View Coverage
```bash
pytest --cov=server-side --cov-report=html
# Opens htmlcov/index.html
```

---

## Test Categories at a Glance

### Unit Tests (test_game_engine.py) - 45+ tests

**Functions Tested:**
- ✓ `_normalize_obstacles` (10 tests)
- ✓ `_map_answers_to_storyboard_json` (9 tests)
- ✓ `generate_game_html` (5 tests)
- ✓ Conversation flow validation (5 tests)
- ✓ Data validation and edge cases (6 tests)
- ✓ Error handling (3 tests)
- ✓ Flask integration (4 tests)
- ✓ Edge cases (8 tests)
- ✓ Session management (2 tests)
- ✓ Configuration (3 tests)
- ✓ Type/format validation (3 tests)

**What They Test:**
- Input validation and normalization
- Answer mapping for all 5 game types
- HTML generation and structure
- Conversation flow logic
- Error handling and recovery
- Session persistence
- Data integrity

**Run Command:**
```bash
pytest test_game_engine.py -v
```

---

### API Tests (test_api_endpoints.py) - 35+ tests

**Endpoints Tested:**
- ✓ GET `/` (index page - 3 tests)
- ✓ POST `/chat` (conversation - 14 tests)
- ✓ File upload endpoints (2 tests)
- ✓ Storyboard endpoints (1 test)
- ✓ Game generation endpoints (1 test)
- ✓ Advanced API features (6 tests)
- ✓ Session management (3 tests)
- ✓ Error handling (3 tests)
- ✓ Security tests (3 tests)
- ✓ Integration flows (2 tests)
- ✓ Performance tests (2 tests)

**What They Test:**
- HTTP status codes and response formats
- JSON request/response handling
- Session isolation and persistence
- CORS and cross-origin requests
- Error handling and recovery
- Security vulnerabilities
- Performance benchmarks
- Unicode and special character support

**Run Command:**
```bash
pytest test_api_endpoints.py -v
```

---

### Integration & System Tests (test_integration_system.py) - 20+ tests

**Complete Workflows Tested:**
- ✓ End-to-end conversations (5 tests) - All 5 game types
- ✓ Error recovery scenarios (3 tests)
- ✓ Load and stress testing (3 tests)
- ✓ Data integrity (3 tests)
- ✓ Cross-browser compatibility (2 tests)
- ✓ Accessibility compliance (2 tests)
- ✓ Internationalization (2 tests)
- ✓ Performance regression (2 tests)

**What They Test:**
- Complete user journeys from start to game generation
- System resilience under error conditions
- Performance under load
- Data consistency across operations
- Browser compatibility
- Accessibility standards
- Multi-language support
- Performance stability over time

**Run Command:**
```bash
pytest test_integration_system.py -v
```

---

## Total Test Count: 100+ test cases

### Test Distribution:
- **Unit Tests:** 45+ tests (45%)
- **API Tests:** 35+ tests (35%)
- **Integration Tests:** 20+ tests (20%)

---

## Common Test Commands

### Run Everything
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest test_game_engine.py -v
pytest test_api_endpoints.py -v
```

### Run Specific Test Class
```bash
pytest test_game_engine.py::TestNormalizeObstacles -v
```

### Run Specific Test
```bash
pytest test_game_engine.py::TestNormalizeObstacles::test_normalize_none_input -v
```

### Run Tests Matching Pattern
```bash
pytest -k "normalize" -v
pytest -k "chat" -v
```

### Run with Coverage
```bash
pytest --cov=server-side
pytest --cov=server-side --cov-report=html
```

### Run and Show Print Statements
```bash
pytest -s -v
```

### Run with Detailed Failures
```bash
pytest -vv --tb=long
```

### Run Fastest Tests First
```bash
pytest --durations=10
```

### Debug a Failing Test
```bash
pytest --pdb test_game_engine.py::TestClass::test_method
```

---

## Test Organization

```
Project Root/
├── tests/
│   ├── test_game_engine.py          # Unit tests (45+ tests)
│   ├── test_api_endpoints.py        # API tests (35+ tests)
│   ├── test_integration_system.py   # Integration tests (20+ tests)
├── TEST_GUIDE.md                    # Full documentation
├── MANUAL_TESTING.md                # Manual procedures
├── TESTING_QUICK_REFERENCE.md       # This file
└── server-side/
    ├── game_agent.py
    ├── web_server.py
    ├── storyboard_engine.py
    └── ...
```

---

## What Each Test File Tests

### test_game_engine.py - 45+ tests

**Core Functions:**
1. `_normalize_obstacles` - Validates obstacle input
2. `_map_answers_to_storyboard_json` - Maps user answers to JSON
3. `generate_game_html` - Generates game HTML

**Test Structure:**
```python
class TestNormalizeObstacles:         # 10 tests
class TestMapAnswersToStoryboardJson: # 9 tests
class TestGameHtmlGeneration:         # 5 tests
class TestFlaskIntegration:           # 4 tests
class TestConversationFlow:           # 5 tests
class TestDataValidation:             # 6 tests
class TestErrorHandling:              # 3 tests
class TestEdgeCases:                  # 8 tests
class TestConversationFlowEdgeCases:  # 4 tests
class TestStoryboardEngineIntegration:# 1 test
class TestGeminiAssistantIntegration: # 1 test
class TestSessionPersistence:         # 2 tests
class TestInputValidation:            # 3 tests
class TestPerformanceBoundaries:      # 3 tests
class TestUserSessions:               # 2 tests
class TestConfiguration:              # 3 tests
class TestTypesAndFormats:            # 3 tests
```

### test_api_endpoints.py - 35+ tests

**API Endpoints:**
1. Index route (GET /)
2. Chat endpoint (POST /chat)
3. Upload endpoint (POST /upload)
4. Other endpoints (if implemented)

**Test Structure:**
```python
class TestAPIEndpoints:           # 14 tests
class TestResponseFormats:        # 2 tests
class TestFileUploadEndpoints:    # 2 tests
class TestStoryboardEndpoints:    # 1 test
class TestGameEndpoints:          # 1 test
class TestPerformance:            # 2 tests
class TestAdvancedAPIEndpoints:   # 6 tests
class TestSessionManagementAdvanced: # 3 tests
class TestErrorHandlingAdvanced:  # 3 tests
class TestSecurityTests:          # 3 tests
class TestIntegrationFlows:       # 2 tests
```

### test_integration_system.py - 20+ tests

**System Integration:**
1. End-to-end conversation flows
2. Error recovery scenarios
3. Load and stress testing
4. Data integrity validation
5. Cross-browser compatibility
6. Accessibility compliance
7. Internationalization support
8. Performance regression testing

**Test Structure:**
```python
class TestEndToEndConversations:  # 5 tests
class TestErrorRecovery:          # 3 tests
class TestLoadAndStress:          # 3 tests
class TestDataIntegrity:          # 3 tests
class TestCrossBrowserCompatibility: # 2 tests
class TestAccessibility:          # 2 tests
class TestInternationalization:   # 2 tests
class TestPerformanceRegression:  # 2 tests
```

---

## Test Data & Scenarios

### Valid Inputs to Test With
- Names: Alice, Bob, Charlie, Diana, José
- Heroes: Knight, Wizard, Ninja, Space Ranger, Dragon
- Locations: Castle, Forest, Space Station, Temple, City
- Goals: collecting goals, rescue mission, escape, time trial, obstacle run
- Obstacles: Dragons, Lava, Spikes, Ghosts, Rocks

### Edge Cases to Test
- Empty strings: ""
- Very long strings: "a" * 1000
- Special characters: @#$%^&*()
- Unicode: 中文, العربية, עברית
- None values: None
- Mixed case: "ESCAPE", "Collecting Goals"

---

## Expected Results

### All Tests Pass
```
===================== 100+ passed in X.XXs ======================
```

### With Coverage
```
Name                          Stmts   Miss  Cover
-------------------------------------------------------
server-side/game_agent.py        50      5    90%
server-side/web_server.py       100     10    90%
server-side/storyboard_engine    75      8    89%
-------------------------------------------------------
TOTAL                           225     23    90%
```

---

## Troubleshooting

### Tests Won't Run
```bash
# Check if pytest installed
pip list | findstr pytest

# Check if in project root
pwd  # or cd to correct directory

# Check if server-side path correct
python -c "import sys; print(sys.path)"
```

### Import Errors
```bash
# Reinstall requirements
pip install -r requirements.txt

# Verify imports work
python -c "from server-side.web_server import app"
```

### Test Failures
```bash
# Run with verbose output
pytest -vv --tb=short

# Run with print statements
pytest -s -v

# Run single test
pytest test_file.py::TestClass::test_method -v
```

### Unicode Errors
```bash
# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Re-run tests
pytest -v
```

### Port Already in Use
```bash
# If testing with real server, find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

---

## Manual Testing Quick Checklist

### Basic Flow Test
- [ ] Load app at localhost:5000
- [ ] Enter name
- [ ] Enter hero description
- [ ] Enter location
- [ ] Choose goal type
- [ ] Answer goal-specific questions
- [ ] Game generates successfully
- [ ] Generated game is playable

### Error Handling Test
- [ ] Invalid choice rejects with error
- [ ] Can retry after error
- [ ] No crash on special characters
- [ ] No crash on very long input

### Session Test
- [ ] Two browsers show different states
- [ ] Session maintains conversation state
- [ ] No data mixing between sessions

### Performance Test
- [ ] Page loads in < 2 seconds
- [ ] Chat responds in < 2 seconds
- [ ] Game generates in reasonable time

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov
```

### Pre-commit Hook
```bash
#!/bin/bash
pytest --quiet || exit 1
```

---

## Test Coverage Goals

- **Aim:** 85%+ overall coverage
- **Unit Tests:** 90%+ coverage
- **Integration Tests:** 80%+ coverage
- **Critical Functions:** 100% coverage

### Check Coverage
```bash
pytest --cov=server-side --cov-report=term-missing
```

---

## When to Run Tests

- **Before committing:** `pytest -v`
- **Before pushing:** `pytest --cov`
- **In CI/CD:** `pytest --cov --cov-report=xml`
- **During development:** Use watch mode: `ptw`
- **Before release:** Full suite + manual testing

---

## Key Testing Principles

1. **Test Isolation:** Each test is independent
2. **Clear Names:** Test name explains what it tests
3. **Arrange-Act-Assert:** Setup → Action → Verify
4. **DRY:** Use fixtures to avoid repetition
5. **Real Data:** Use realistic test data
6. **Edge Cases:** Test boundaries and errors

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [Testing Best Practices](https://realpython.com/python-testing/)

---

## Quick Links

- **Full Testing Guide:** [TEST_GUIDE.md](TEST_GUIDE.md)
- **Manual Testing:** [MANUAL_TESTING.md](MANUAL_TESTING.md)
- **Updated Testing Plan:** [TESTING_UPDATED.md](TESTING_UPDATED.md)

---

**Version:** 1.0  
**Last Updated:** 2024  
**Total Tests:** 50+  
**Coverage Goal:** 85%+
