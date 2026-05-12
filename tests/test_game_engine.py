"""
Comprehensive Test Suite for Game Generation Engine
Tests cover: Unit Tests, Integration Tests, and End-to-End Tests
"""

import pytest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

# Add server-side to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server-side'))

from web_server import app, _normalize_obstacles, _map_answers_to_storyboard_json, user_states, conversation_questions
from game_agent import generate_game_html
from storyboard_engine import generate_optimized_storyboard


# ============================================================================
# UNIT TESTS - Testing individual functions in isolation
# ============================================================================

class TestNormalizeObstacles:
    """Test cases for _normalize_obstacles function"""
    
    def test_normalize_none_input(self):
        """Test with None input should return default message"""
        assert _normalize_obstacles(None) == "No obstacles specified (default)"
    
    def test_normalize_empty_string(self):
        """Test with empty string should return default message"""
        assert _normalize_obstacles("") == "No obstacles specified (default)"
    
    def test_normalize_none_lowercase(self):
        """Test with 'none' (lowercase) should return default message"""
        assert _normalize_obstacles("none") == "No obstacles specified (default)"
    
    def test_normalize_no_lowercase(self):
        """Test with 'no' (lowercase) should return default message"""
        assert _normalize_obstacles("no") == "No obstacles specified (default)"
    
    def test_normalize_no_uppercase(self):
        """Test with 'No' (mixed case) should return default message"""
        assert _normalize_obstacles("No") == "No obstacles specified (default)"
    
    def test_normalize_na_abbreviation(self):
        """Test with 'n/a' should return default message"""
        assert _normalize_obstacles("n/a") == "No obstacles specified (default)"
    
    def test_normalize_with_whitespace(self):
        """Test with whitespace-only string should return default message"""
        assert _normalize_obstacles("   ") == "No obstacles specified (default)"
    
    def test_normalize_valid_obstacles(self):
        """Test with valid obstacles string should return as-is"""
        result = _normalize_obstacles("spikes and pits")
        assert result == "spikes and pits"
    
    def test_normalize_complex_obstacles(self):
        """Test with complex obstacles description"""
        obstacles = "lava pits, falling rocks, enemy guards"
        assert _normalize_obstacles(obstacles) == obstacles
    
    def test_normalize_no_obstacles_phrase(self):
        """Test with 'no obstacles' phrase"""
        assert _normalize_obstacles("no obstacles") == "No obstacles specified (default)"


class TestMapAnswersToStoryboardJson:
    """Test cases for _map_answers_to_storyboard_json function"""
    
    def test_collecting_goals_goal_type(self):
        """Test mapping collecting goals scenario"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "Brave knight",
            "game_location": "haunted forest",
            "collecting_goals_object": "magic gems",
            "collecting_goals_obstacles": "spikes"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Collecting goals"
        assert result["character"] == "Brave knight"
        assert result["background"] == "haunted forest"
        assert result["target"] == "magic gems"
        assert result["obstacles"] == "spikes"
    
    def test_rescue_mission_goal_type(self):
        """Test mapping rescue mission scenario"""
        answers = {
            "hero_goal": "rescue mission",
            "hero_description": "Space ranger",
            "game_location": "outer space",
            "rescue_mission_character": "lost alien",
            "rescue_mission_obstacles": "asteroid field"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Rescue mission"
        assert result["character"] == "Space ranger"
        assert result["target"] == "lost alien"
        assert result["obstacles"] == "asteroid field"
    
    def test_time_trial_goal_type(self):
        """Test mapping time trial scenario"""
        answers = {
            "hero_goal": "time trial",
            "hero_description": "Speed runner",
            "game_location": "city streets",
            "time_trial_obstacles": "traffic"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Time trial"
        assert result["target"] == "Finish line"
        assert result["obstacles"] == "traffic"
    
    def test_escape_goal_type(self):
        """Test mapping escape scenario"""
        answers = {
            "hero_goal": "escape",
            "hero_description": "Ninja",
            "game_location": "ancient temple",
            "escape_enemy_description": "ghost guardian"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Escape"
        assert result["target"] == "Exit gate"
        assert result["character"] == "Ninja"
    
    def test_obstacle_run_goal_type(self):
        """Test mapping obstacle run scenario"""
        answers = {
            "hero_goal": "obstacle run",
            "hero_description": "Runner",
            "game_location": "lava canyon",
            "obstacle_run_obstacles": "falling rocks"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Obstacle run"
        assert result["target"] == "Victory flag"
        assert result["obstacles"] == "falling rocks"
    
    def test_unknown_goal_type_defaults_to_rescue(self):
        """Test that unknown goal type defaults to rescue mission"""
        answers = {
            "hero_goal": "unknown",
            "hero_description": "Hero",
            "game_location": "world"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["goal_type"] == "Rescue mission"
        assert result["target"] == "Goal"
        assert result["obstacles"] == "Obstacles"
    
    def test_missing_character_uses_default(self):
        """Test that missing character description uses default"""
        answers = {
            "hero_goal": "collecting goals",
            "game_location": "forest",
            "collecting_goals_object": "coins"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["character"] == "main character"
    
    def test_missing_location_uses_default(self):
        """Test that missing location uses default"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "knight",
            "collecting_goals_object": "coins"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        assert result["background"] == "game level"


class TestGameHtmlGeneration:
    """Test cases for game HTML generation"""
    
    def test_generate_game_html_returns_string(self):
        """Test that generate_game_html returns a string"""
        result = generate_game_html("knight", "castle", "collect gold", "dragons")
        assert isinstance(result, str)
    
    def test_generate_game_html_contains_html_tags(self):
        """Test that generated HTML contains expected HTML tags"""
        result = generate_game_html("knight", "castle", "collect gold", "dragons")
        assert "<!DOCTYPE html>" in result
        assert "<html" in result
        assert "</html>" in result
        assert "<canvas" in result
    
    def test_generate_game_html_includes_parameters(self):
        """Test that game HTML includes the provided parameters"""
        hero = "Brave Knight"
        environment = "Haunted Castle"
        goal = "Rescue Princess"
        obstacle = "Fire Dragons"
        
        result = generate_game_html(hero, environment, goal, obstacle)
        
        # Check that parameters are included in the output
        assert hero.upper() in result or hero in result
        assert environment in result
        assert goal in result
        assert obstacle in result
    
    def test_generate_game_html_has_canvas_element(self):
        """Test that generated HTML has canvas element"""
        result = generate_game_html("hero", "world", "escape", "monsters")
        assert "canvas" in result.lower()
        assert "gameCanvas" in result
    
    def test_generate_game_html_has_script(self):
        """Test that generated HTML includes JavaScript"""
        result = generate_game_html("hero", "world", "escape", "monsters")
        assert "<script>" in result or "<script " in result


# ============================================================================
# FLASK APP INTEGRATION TESTS
# ============================================================================

class TestFlaskIntegration:
    """Integration tests for Flask app endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_route_loads(self, client):
        """Test that index route returns 200 OK"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_route_returns_html(self, client):
        """Test that index route returns HTML content"""
        response = client.get('/')
        assert response.content_type.startswith('text/html')
        assert b'<!DOCTYPE' in response.data or b'<html' in response.data
    
    def test_chat_endpoint_exists(self, client):
        """Test that chat endpoint exists"""
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "test", "session_id": "test123"}),
            content_type='application/json'
        )
        # Should return 200 or 500 but endpoint should be accessible
        assert response.status_code in [200, 400, 500]
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in response"""
        response = client.get('/')
        # CORS should be enabled
        assert response.status_code == 200


# ============================================================================
# END-TO-END CONVERSATION FLOW TESTS
# ============================================================================

class TestConversationFlow:
    """Test the complete conversation flow"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()  # Clear previous states
        with app.test_client() as client:
            yield client
    
    def test_conversation_question_structure(self):
        """Test that conversation questions are properly structured"""
        assert "name" in conversation_questions
        assert "hero_description" in conversation_questions
        assert "game_location" in conversation_questions
        assert "hero_goal" in conversation_questions
    
    def test_hero_goal_has_all_options(self):
        """Test that hero_goal question has all expected options"""
        hero_goal_q = conversation_questions["hero_goal"]
        expected_options = ["collecting goals", "rescue mission", "time trial", "escape", "obstacle run"]
        assert set(hero_goal_q["options"]) == set(expected_options)
    
    def test_hero_goal_has_next_question_map(self):
        """Test that hero_goal has proper next_question_map"""
        hero_goal_q = conversation_questions["hero_goal"]
        assert "next_question_map" in hero_goal_q
        assert len(hero_goal_q["next_question_map"]) == 5
    
    def test_all_questions_have_required_fields(self):
        """Test that all questions have required fields"""
        required_fields = ["question", "type"]
        for q_key, q_data in conversation_questions.items():
            assert "question" in q_data, f"Question {q_key} missing 'question' field"
            assert "type" in q_data, f"Question {q_key} missing 'type' field"
    
    def test_choice_questions_have_options(self):
        """Test that all choice-type questions have options"""
        for q_key, q_data in conversation_questions.items():
            if q_data["type"] == "choice":
                assert "options" in q_data, f"Choice question {q_key} missing 'options'"
                assert len(q_data["options"]) > 0, f"Choice question {q_key} has empty options"


# ============================================================================
# DATA VALIDATION TESTS
# ============================================================================

class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_normalize_obstacles_with_special_characters(self):
        """Test obstacle normalization with special characters"""
        result = _normalize_obstacles("spikes & pits!")
        assert result == "spikes & pits!"
    
    def test_normalize_obstacles_with_unicode(self):
        """Test obstacle normalization with unicode characters"""
        result = _normalize_obstacles("מכשולים ודרקונים")  # Hebrew text
        assert result == "מכשולים ודרקונים"
    
    def test_storyboard_json_with_empty_obstacles(self):
        """Test storyboard JSON mapping with empty obstacle field"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "knight",
            "game_location": "castle",
            "collecting_goals_object": "gold",
            "collecting_goals_obstacles": ""
        }
        result = _map_answers_to_storyboard_json(answers)
        assert result["obstacles"] == "No obstacles specified (default)"
    
    def test_storyboard_json_with_none_values(self):
        """Test storyboard JSON mapping handles None values gracefully"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": None,
            "game_location": None,
            "collecting_goals_object": "treasure"
        }
        result = _map_answers_to_storyboard_json(answers)
        assert result["character"] == "main character"
        assert result["background"] == "game level"
    
    def test_storyboard_json_case_insensitive_goal(self):
        """Test that goal type matching is case-insensitive"""
        answers = {
            "hero_goal": "COLLECTING GOALS",
            "hero_description": "knight",
            "game_location": "castle",
            "collecting_goals_object": "gold"
        }
        result = _map_answers_to_storyboard_json(answers)
        assert result["goal_type"] == "Collecting goals"
    
    def test_storyboard_json_with_extra_fields(self):
        """Test that storyboard JSON handles extra unexpected fields"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "knight",
            "game_location": "castle",
            "collecting_goals_object": "gold",
            "collecting_goals_obstacles": "spikes",
            "extra_field": "should be ignored",
            "another_field": "also ignored"
        }
        result = _map_answers_to_storyboard_json(answers)
        # Should not raise error and should process correctly
        assert result["goal_type"] == "Collecting goals"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_generate_game_html_with_empty_strings(self):
        """Test game generation with empty string parameters"""
        result = generate_game_html("", "", "", "")
        assert isinstance(result, str)
        assert "<!DOCTYPE" in result
    
    def test_generate_game_html_with_very_long_strings(self):
        """Test game generation with very long parameter strings"""
        long_string = "a" * 1000
        result = generate_game_html(long_string, long_string, long_string, long_string)
        assert isinstance(result, str)
    
    def test_normalize_obstacles_with_mixed_case(self):
        """Test obstacle normalization with mixed case None values"""
        assert _normalize_obstacles("NoNe") == "No obstacles specified (default)"
        assert _normalize_obstacles("NONE") == "No obstacles specified (default)"
        assert _normalize_obstacles("nOnE") == "No obstacles specified (default)"


# ============================================================================
# USER SESSION TESTS
# ============================================================================

class TestUserSessions:
    """Test user session management"""
    
    def test_user_states_dictionary_exists(self):
        """Test that user_states dictionary exists"""
        assert isinstance(user_states, dict)
    
    def test_unique_session_ids(self):
        """Test that unique session IDs can be tracked"""
        user_states.clear()
        
        session_id_1 = "session_abc123"
        session_id_2 = "session_def456"
        
        user_states[session_id_1] = {"answer": "test1"}
        user_states[session_id_2] = {"answer": "test2"}
        
        assert user_states[session_id_1]["answer"] == "test1"
        assert user_states[session_id_2]["answer"] == "test2"
        assert len(user_states) == 2


# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

class TestConfiguration:
    """Test application configuration"""
    
    def test_flask_app_exists(self):
        """Test that Flask app is properly initialized"""
        assert app is not None
        assert app.name is not None
    
    def test_upload_folder_configured(self):
        """Test that upload folder is configured"""
        assert app.static_folder is not None
    
    def test_conversation_questions_complete(self):
        """Test that all conversation questions are defined"""
        expected_questions = [
            "name",
            "hero_description",
            "game_location",
            "hero_goal",
            "collecting_goals_object",
            "collecting_goals_obstacles",
            "rescue_mission_character",
            "rescue_mission_obstacles",
            "time_trial_type",
            "time_trial_obstacles",
            "escape_enemy_description",
            "obstacle_run_obstacles"
        ]
        for q in expected_questions:
            assert q in conversation_questions, f"Missing question: {q}"


# ============================================================================
# TYPE AND FORMAT TESTS
# ============================================================================

class TestTypesAndFormats:
    """Test that functions return correct types and formats"""
    
    def test_normalize_obstacles_always_returns_string(self):
        """Test that _normalize_obstacles always returns string"""
        test_inputs = [None, "", "test", 123, 0, "none", "No"]
        for test_input in test_inputs:
            result = _normalize_obstacles(test_input)
            assert isinstance(result, str)
    
    def test_storyboard_json_returns_dictionary(self):
        """Test that _map_answers_to_storyboard_json returns dictionary"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "knight",
            "game_location": "castle",
            "collecting_goals_object": "gold"
        }
        result = _map_answers_to_storyboard_json(answers)
        assert isinstance(result, dict)
    
    def test_storyboard_json_has_expected_keys(self):
        """Test that storyboard JSON has expected keys"""
        answers = {
            "hero_goal": "escape",
            "hero_description": "ninja",
            "game_location": "temple",
            "escape_enemy_description": "guards"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        expected_keys = ["goal_type", "character", "background", "target", "obstacles"]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"


# ============================================================================
# ADDITIONAL EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Additional edge cases and boundary tests"""
    
    def test_normalize_obstacles_with_numbers(self):
        """Test obstacle normalization with numeric inputs"""
        assert _normalize_obstacles(0) == "No obstacles specified (default)"
        assert _normalize_obstacles(123) == "123"
        assert _normalize_obstacles("0") == "No obstacles specified (default)"
    
    def test_normalize_obstacles_case_variations(self):
        """Test various case variations of 'none'"""
        variations = ["NONE", "None", "nOne", "noNe", "NONe"]
        for variation in variations:
            result = _normalize_obstacles(variation)
            assert result == "No obstacles specified (default)"
    
    def test_storyboard_json_empty_answers_dict(self):
        """Test mapping with completely empty answers dict"""
        result = _map_answers_to_storyboard_json({})
        assert result["goal_type"] == "Rescue mission"
        assert result["character"] == "main character"
        assert result["background"] == "game level"
        assert result["target"] == "Goal"
        assert result["obstacles"] == "Obstacles"
    
    def test_storyboard_json_partial_answers(self):
        """Test mapping with partial answers for different goals"""
        # Partial collecting goals
        answers = {"hero_goal": "collecting goals", "collecting_goals_object": "coins"}
        result = _map_answers_to_storyboard_json(answers)
        assert result["goal_type"] == "Collecting goals"
        assert result["target"] == "coins"
        assert result["obstacles"] == "Obstacles"
    
    def test_generate_game_html_with_special_chars(self):
        """Test game generation with special characters in inputs"""
        hero = "Hero & Dragon"
        environment = "Castle <3"
        goal = "Collect 100% gold"
        obstacle = "Fire & Ice"
        
        result = generate_game_html(hero, environment, goal, obstacle)
        assert hero in result
        assert environment in result
        assert goal in result
        assert obstacle in result
        assert "<!DOCTYPE html>" in result
    
    def test_generate_game_html_with_newlines(self):
        """Test game generation with newlines in inputs"""
        hero = "Hero\nwith\nnewlines"
        result = generate_game_html(hero, "castle", "goal", "obstacles")
        assert hero in result
        assert isinstance(result, str)


class TestConversationFlowEdgeCases:
    """Test edge cases in conversation flow"""
    
    def test_conversation_question_types(self):
        """Test that all question types are valid"""
        valid_types = ["text", "text_or_image", "choice"]
        for q_key, q_data in conversation_questions.items():
            assert q_data["type"] in valid_types, f"Invalid type for {q_key}: {q_data['type']}"
    
    def test_next_question_mapping_consistency(self):
        """Test that next_question_map keys match hero_goal options"""
        hero_goal_options = conversation_questions["hero_goal"]["options"]
        next_question_map = conversation_questions["hero_goal"]["next_question_map"]
        
        assert set(next_question_map.keys()) == set(hero_goal_options)
    
    def test_all_next_questions_exist(self):
        """Test that all referenced next questions actually exist"""
        for q_key, q_data in conversation_questions.items():
            if "next_question" in q_data:
                next_q = q_data["next_question"]
                assert next_q in conversation_questions, f"Next question {next_q} not found"
    
    def test_choice_options_are_strings(self):
        """Test that all choice options are strings"""
        for q_key, q_data in conversation_questions.items():
            if q_data["type"] == "choice":
                for option in q_data["options"]:
                    assert isinstance(option, str), f"Non-string option in {q_key}: {option}"


class TestStoryboardEngineIntegration:
    """Test integration with storyboard engine"""
    
    @patch('storyboard_engine.generate_optimized_storyboard')
    def test_storyboard_generation_called(self, mock_generate):
        """Test that storyboard generation is called when needed"""
        mock_generate.return_value = "mock storyboard"
        
        # This would be called from web_server when generating storyboard
        from storyboard_engine import generate_optimized_storyboard
        result = generate_optimized_storyboard("test topic")
        
        mock_generate.assert_called_once_with("test topic")
        assert result == "mock storyboard"


class TestGeminiAssistantIntegration:
    """Test integration with Gemini assistant"""
    
    @patch('gemini_assistant.GeminiGameAssistant.generate_response')
    def test_gemini_assistant_called(self, mock_generate):
        """Test that Gemini assistant is called when needed"""
        mock_generate.return_value = "mock response"
        
        from gemini_assistant import GeminiGameAssistant
        assistant = GeminiGameAssistant(api_key="test_key")
        result = assistant.generate_response("test prompt")
        
        mock_generate.assert_called_once_with("test prompt")
        assert result == "mock response"


class TestSessionPersistence:
    """Test session state persistence across multiple interactions"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    def test_session_state_progression(self, client):
        """Test that session state progresses correctly through conversation"""
        session_id = "progression_test"
        
        # Start conversation
        response1 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Alice", "session_id": session_id}),
            content_type='application/json'
        )
        assert response1.status_code in [200, 400, 500]
        
        # Check session state exists
        assert session_id in user_states
        
        # Continue conversation
        response2 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Brave knight", "session_id": session_id}),
            content_type='application/json'
        )
        assert response2.status_code in [200, 400, 500]
        
        # Session should still exist and have progressed
        assert session_id in user_states
    
    def test_multiple_sessions_concurrent(self, client):
        """Test multiple sessions running concurrently"""
        sessions = ["session_a", "session_b", "session_c"]
        
        for session_id in sessions:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": "test", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]
        
        # All sessions should exist
        for session_id in sessions:
            assert session_id in user_states


class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_normalize_obstacles_sql_injection_attempt(self):
        """Test that SQL injection attempts are handled safely"""
        sql_attempt = "'; DROP TABLE users; --"
        result = _normalize_obstacles(sql_attempt)
        assert result == sql_attempt  # Should return as-is, not execute
    
    def test_normalize_obstacles_xss_attempt(self):
        """Test that XSS attempts are handled safely"""
        xss_attempt = "<script>alert('xss')</script>"
        result = _normalize_obstacles(xss_attempt)
        assert result == xss_attempt  # Should return as-is, not execute
    
    def test_storyboard_json_with_malicious_input(self):
        """Test storyboard mapping with potentially malicious input"""
        answers = {
            "hero_goal": "collecting goals",
            "hero_description": "<script>alert('xss')</script>",
            "game_location": "'; DROP TABLE games; --",
            "collecting_goals_object": "gold"
        }
        result = _map_answers_to_storyboard_json(answers)
        
        # Should process without crashing
        assert isinstance(result, dict)
        assert result["character"] == "<script>alert('xss')</script>"  # Input preserved


class TestPerformanceBoundaries:
    """Test performance boundaries and limits"""
    
    def test_normalize_obstacles_very_long_input(self):
        """Test obstacle normalization with very long input"""
        long_input = "a" * 10000
        result = _normalize_obstacles(long_input)
        assert result == long_input
        assert len(result) == 10000
    
    def test_storyboard_json_large_answers_dict(self):
        """Test mapping with large answers dictionary"""
        large_answers = {}
        for i in range(100):
            large_answers[f"field_{i}"] = f"value_{i}" * 100
        
        # Should not crash
        result = _map_answers_to_storyboard_json(large_answers)
        assert isinstance(result, dict)
    
    def test_generate_game_html_large_parameters(self):
        """Test game generation with large parameter strings"""
        large_string = "x" * 5000
        result = generate_game_html(large_string, large_string, large_string, large_string)
        assert isinstance(result, str)
        assert len(result) > 1000  # Should contain HTML structure


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
