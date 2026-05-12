# Game Generation Engine - Testing Guide

This document provides comprehensive information about the test suite for the Game Generation Engine project.

## Overview

The test suite consists of two main test files:

1. **test_game_engine.py** - Unit tests and integration tests for core functions
2. **test_api_endpoints.py** - API endpoint and HTTP request/response tests

## Test Coverage

### Unit Tests (test_game_engine.py)

#### 1. `TestNormalizeObstacles` - 10 test cases
Tests the `_normalize_obstacles` function which normalizes user input for obstacles.

**Test Cases:**
- `test_normalize_none_input` - None input returns default message
- `test_normalize_empty_string` - Empty string returns default message
- `test_normalize_none_lowercase` - "none" returns default message
- `test_normalize_no_lowercase` - "no" returns default message
- `test_normalize_no_uppercase` - "No" returns default message
- `test_normalize_na_abbreviation` - "n/a" returns default message
- `test_normalize_with_whitespace` - Whitespace-only returns default
- `test_normalize_valid_obstacles` - Valid input returns as-is
- `test_normalize_complex_obstacles` - Complex descriptions handled correctly
- `test_normalize_no_obstacles_phrase` - "no obstacles" phrase recognized

#### 2. `TestMapAnswersToStoryboardJson` - 9 test cases
Tests the `_map_answers_to_storyboard_json` function which converts user answers to game JSON.

**Test Cases:**
- `test_collecting_goals_goal_type` - Collecting goals path
- `test_rescue_mission_goal_type` - Rescue mission path
- `test_time_trial_goal_type` - Time trial path
- `test_escape_goal_type` - Escape scenario
- `test_obstacle_run_goal_type` - Obstacle run scenario
- `test_unknown_goal_type_defaults_to_rescue` - Unknown goal type handling
- `test_missing_character_uses_default` - Default character name
- `test_missing_location_uses_default` - Default location
- All test proper mapping of goal types, characters, targets, and obstacles

#### 3. `TestGameHtmlGeneration` - 5 test cases
Tests the game HTML generation function.

**Test Cases:**
- `test_generate_game_html_returns_string` - Returns string type
- `test_generate_game_html_contains_html_tags` - Valid HTML structure
- `test_generate_game_html_includes_parameters` - Parameters included in output
- `test_generate_game_html_has_canvas_element` - Canvas element present
- `test_generate_game_html_has_script` - JavaScript included

#### 4. `TestConversationFlow` - 5 test cases
Tests the conversation flow and question structure.

**Test Cases:**
- `test_conversation_question_structure` - All required questions exist
- `test_hero_goal_has_all_options` - All 5 goal options present
- `test_hero_goal_has_next_question_map` - Proper branching logic
- `test_all_questions_have_required_fields` - Valid question structure
- `test_choice_questions_have_options` - Choice questions have options

#### 5. `TestDataValidation` - 6 test cases
Tests data validation and edge cases.

**Test Cases:**
- `test_normalize_obstacles_with_special_characters` - Special characters handled
- `test_normalize_obstacles_with_unicode` - Hebrew/unicode text supported
- `test_storyboard_json_with_empty_obstacles` - Empty obstacles normalized
- `test_storyboard_json_with_none_values` - None values handled gracefully
- `test_storyboard_json_case_insensitive_goal` - Case-insensitive goal matching
- `test_storyboard_json_with_extra_fields` - Extra fields ignored

#### 6. `TestErrorHandling` - 3 test cases
Tests error handling.

**Test Cases:**
- `test_generate_game_html_with_empty_strings` - Empty parameters handled
- `test_generate_game_html_with_very_long_strings` - Long strings handled
- `test_normalize_obstacles_with_mixed_case` - Mixed case normalization

#### 7. `TestFlaskIntegration` - 4 test cases
Tests Flask app integration.

**Test Cases:**
- `test_index_route_loads` - Index route loads successfully
- `test_index_route_returns_html` - Returns HTML content
- `test_chat_endpoint_exists` - Chat endpoint is accessible
- `test_cors_headers_present` - CORS headers present

#### 8. `TestEdgeCases` - 8 test cases
Additional edge case testing.

**Test Cases:**
- `test_normalize_obstacles_with_numbers` - Numeric input handling
- `test_normalize_obstacles_case_variations` - Various case variations
- `test_storyboard_json_empty_answers_dict` - Empty answers dict
- `test_storyboard_json_partial_answers` - Partial answers handling
- `test_generate_game_html_with_special_chars` - Special characters in HTML
- `test_generate_game_html_with_newlines` - Newlines in parameters
- `test_conversation_question_types` - Question type validation
- `test_next_question_mapping_consistency` - Mapping consistency

#### 9. `TestConversationFlowEdgeCases` - 4 test cases
Conversation flow edge cases.

**Test Cases:**
- `test_conversation_question_types` - Question types validation
- `test_next_question_mapping_consistency` - Mapping consistency
- `test_all_next_questions_exist` - Next questions exist
- `test_choice_options_are_strings` - Options are strings

#### 10. `TestStoryboardEngineIntegration` - 1 test case
Storyboard engine integration.

#### 11. `TestGeminiAssistantIntegration` - 1 test case
Gemini assistant integration.

#### 12. `TestSessionPersistence` - 2 test cases
Session persistence testing.

#### 13. `TestInputValidation` - 3 test cases
Input validation and security.

#### 14. `TestPerformanceBoundaries` - 3 test cases
Performance boundary testing.

#### 15. `TestUserSessions` - 2 test cases
User session management.

#### 16. `TestConfiguration` - 3 test cases
Application configuration.

#### 17. `TestTypesAndFormats` - 3 test cases
Type and format validation.

### API Endpoint Tests (test_api_endpoints.py)

#### 1. `TestAPIEndpoints` - 14 test cases
Tests HTTP endpoints.

**Test Cases:**
- Index page loading and content
- Chat endpoint with valid/invalid JSON
- Session ID requirements
- Message requirements
- Empty and very long messages
- Unicode character support
- Session isolation and persistence
- Invalid JSON handling
- CORS handling

#### 2. `TestResponseFormats` - 2 test cases
Tests response formats.

**Test Cases:**
- `test_chat_response_json_structure` - Valid JSON responses
- `test_index_response_has_html_structure` - Valid HTML responses

#### 3. `TestFileUploadEndpoints` - 2 test cases
Tests file upload functionality.

**Test Cases:**
- `test_upload_endpoint_exists` - Upload endpoint accessibility
- `test_upload_with_missing_file` - Missing file handling

#### 4. `TestStoryboardEndpoints` - 1 test case
Tests storyboard endpoints if implemented.

#### 5. `TestGameEndpoints` - 1 test case
Tests game generation endpoints.

#### 6. `TestPerformance` - 2 test cases
Tests application performance.

**Test Cases:**
- `test_index_response_time` - Index loads under 1 second
- `test_chat_response_time` - Chat responds under 5 seconds

#### 7. `TestAdvancedAPIEndpoints` - 6 test cases
Advanced API testing.

**Test Cases:**
- `test_chat_endpoint_with_extremely_long_message` - 10k character messages
- `test_chat_endpoint_with_special_unicode` - Special unicode characters
- `test_chat_endpoint_with_json_injection_attempt` - JSON injection attempts
- `test_chat_endpoint_with_malformed_json` - Malformed JSON handling
- `test_chat_endpoint_content_types` - Different content types
- `test_chat_endpoint_http_methods` - HTTP method validation

#### 8. `TestSessionManagementAdvanced` - 3 test cases
Advanced session management.

#### 9. `TestErrorHandlingAdvanced` - 3 test cases
Advanced error handling.

#### 10. `TestSecurityTests` - 3 test cases
Security-focused tests.

#### 11. `TestIntegrationFlows` - 2 test cases
Integration flow testing.

### Integration & System Tests (test_integration_system.py)

#### 1. `TestEndToEndConversations` - 5 test cases
Complete end-to-end conversation flows.

**Test Cases:**
- `test_full_collecting_goals_flow` - Complete collecting goals flow
- `test_full_rescue_mission_flow` - Complete rescue mission flow
- `test_full_escape_flow` - Complete escape flow
- `test_full_time_trial_flow` - Complete time trial flow
- `test_full_obstacle_run_flow` - Complete obstacle run flow

#### 2. `TestErrorRecovery` - 3 test cases
Error recovery testing.

#### 3. `TestLoadAndStress` - 3 test cases
Load and stress testing.

#### 4. `TestDataIntegrity` - 3 test cases
Data integrity testing.

#### 5. `TestCrossBrowserCompatibility` - 2 test cases
Cross-browser compatibility.

#### 6. `TestAccessibility` - 2 test cases
Accessibility testing.

#### 7. `TestInternationalization` - 2 test cases
Internationalization support.

#### 8. `TestPerformanceRegression` - 2 test cases
Performance regression testing.

## Total Test Count: 100+ test cases

### Test Distribution:
- **Unit Tests:** 45+ tests (45%)
- **API Tests:** 35+ tests (35%)
- **Integration Tests:** 20+ tests (20%)

## Setup Instructions

### 1. Install Testing Dependencies

```bash
# Ensure you're in your virtual environment
venv\Scripts\activate

# Install pytest
pip install pytest pytest-cov pytest-mock

# Install any other dependencies from requirements.txt
pip install -r requirements.txt
```

### 2. Verify Test Files Location

Test files should be in the root directory of your project:
- `test_game_engine.py`
- `test_api_endpoints.py`

## Running the Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
# Run only unit tests
pytest test_game_engine.py -v

# Run only API endpoint tests
pytest test_api_endpoints.py -v
```

### Run Specific Test Class

```bash
pytest test_game_engine.py::TestNormalizeObstacles -v
pytest test_api_endpoints.py::TestAPIEndpoints -v
```

### Run Specific Test Case

```bash
pytest test_game_engine.py::TestNormalizeObstacles::test_normalize_none_input -v
```

### Run with Coverage Report

```bash
pytest --cov=server-side --cov-report=html
```

This generates an HTML coverage report in the `htmlcov` directory.

### Run Tests in Watch Mode (requires pytest-watch)

```bash
pip install pytest-watch
ptw
```

### Run Tests with Markers

```bash
# Run tests matching a pattern
pytest -k "normalize" -v

# Skip specific tests
pytest --ignore=test_api_endpoints.py
```

## Test Execution Flow

### Before Running Tests
1. Ensure virtual environment is activated
2. Ensure all dependencies are installed
3. Ensure test files are in the project root

### During Test Execution
- Each test is independent
- User session states are cleared before each test class
- Flask app is in testing mode
- No actual API calls are made (uses mock data)

### After Test Execution
- Review failed tests
- Check coverage report if generated
- Fix any failing tests before committing code

## Expected Test Results

When running all tests successfully:

```
===================== 50+ passed in X.XXs ======================
```

## Common Test Failures and Solutions

### Issue: Tests can't find module imports
**Solution:**
```bash
# Ensure you're in the project root directory
# Verify sys.path includes server-side folder
```

### Issue: Flask app not initializing
**Solution:**
```bash
# Install all requirements
pip install -r requirements.txt
```

### Issue: Tests pass locally but fail in CI/CD
**Solution:**
- Ensure .env file exists or is not required for testing
- Mock external API calls (like Gemini API)
- Use test fixtures for Flask app

### Issue: Unicode character tests fail
**Solution:**
```bash
# Ensure Python is using UTF-8 encoding
# In PowerShell:
$env:PYTHONIOENCODING = "utf-8"
```

## Test Categories Explained

### Unit Tests
Test individual functions in isolation:
- `_normalize_obstacles` - Validates obstacle input normalization
- `_map_answers_to_storyboard_json` - Validates answer mapping
- `generate_game_html` - Validates HTML generation

### Integration Tests
Test how components work together:
- Flask app initialization
- Conversation flow
- Session management

### API Tests
Test HTTP endpoints:
- GET / (index)
- POST /chat (conversation)
- CORS headers

### Functional Tests
Test complete workflows:
- Conversation flow from start to game generation
- Session persistence

### Performance Tests
Test application speed:
- Index page response time
- Chat endpoint response time

## Continuous Integration

To integrate these tests with CI/CD:

### GitHub Actions Example
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=server-side
```

## Test Maintenance

### Adding New Tests
1. Identify the function/endpoint to test
2. Create a new test class in the appropriate test file
3. Follow naming convention: `test_<what_is_being_tested>`
4. Add docstring explaining the test
5. Run the new test to verify it works

### Updating Tests
When modifying code:
1. Update related tests
2. Run full test suite to ensure nothing breaks
3. Add tests for new functionality
4. Maintain test coverage above 80%

## Mocking and Fixtures

The tests use pytest fixtures for:
- Flask test client: `@pytest.fixture def client(self)`
- User state cleanup: `user_states.clear()`
- Test isolation

## Coverage Goals

Aim for:
- **Unit Tests:** 90%+ coverage
- **Integration Tests:** 80%+ coverage
- **Overall:** 85%+ coverage

Generate coverage report:
```bash
pytest --cov=server-side --cov-report=term-missing
```

## Advanced Testing

### Debugging Tests
```bash
# Run with print statements visible
pytest -s -v

# Use pdb for debugging
pytest --pdb test_game_engine.py
```

### Profiling Tests
```bash
# See which tests are slowest
pytest --durations=10
```

### Test Documentation
Run with `--collect-only` to see all tests:
```bash
pytest --collect-only
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)

## Support

If you encounter issues:
1. Check that all requirements are installed: `pip list`
2. Verify test files are in the correct location
3. Review test output for specific error messages
4. Check that the application runs without errors
5. Ensure UTF-8 encoding is used for non-ASCII characters

---

**Last Updated:** 2024
**Test Suite Version:** 1.0
**Total Tests:** 50+
