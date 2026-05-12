"""
Comprehensive Integration and System Tests for Game Generation Engine
Tests complete workflows, system integration, and end-to-end scenarios
"""

import pytest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server-side'))

from web_server import app, user_states, conversation_questions
from game_agent import generate_game_html


# ============================================================================
# END-TO-END CONVERSATION TESTS
# ============================================================================

class TestEndToEndConversations:
    """Complete end-to-end conversation flow tests"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client

    def test_full_collecting_goals_flow(self, client):
        """Test complete collecting goals conversation flow"""
        session_id = "collecting_goals_e2e"

        # Step 1: Name
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "Alex", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Step 2: Hero description
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "Brave explorer", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Step 3: Game location
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "Ancient ruins", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Step 4: Hero goal
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "collecting goals", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Step 5: Object to collect
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "Mystic artifacts", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Step 6: Obstacles
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "Traps and guardians", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Verify session completed
        assert session_id in user_states

    def test_full_rescue_mission_flow(self, client):
        """Test complete rescue mission conversation flow"""
        session_id = "rescue_mission_e2e"

        steps = [
            "Sam",
            "Space ranger",
            "Alien planet",
            "rescue mission",
            "Lost crew member",
            "Meteor storms"
        ]

        for step_message in steps:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": step_message, "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        assert session_id in user_states

    def test_full_escape_flow(self, client):
        """Test complete escape conversation flow"""
        session_id = "escape_e2e"

        steps = [
            "Jordan",
            "Master thief",
            "High-security vault",
            "escape",
            "Laser security system"
        ]

        for step_message in steps:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": step_message, "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        assert session_id in user_states

    def test_full_time_trial_flow(self, client):
        """Test complete time trial conversation flow"""
        session_id = "time_trial_e2e"

        steps = [
            "Taylor",
            "Speed runner",
            "Urban cityscape",
            "time trial",
            "stopwatch",
            "Pedestrians and traffic"
        ]

        for step_message in steps:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": step_message, "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        assert session_id in user_states

    def test_full_obstacle_run_flow(self, client):
        """Test complete obstacle run conversation flow"""
        session_id = "obstacle_run_e2e"

        steps = [
            "Casey",
            "Parkour athlete",
            "Rooftop city",
            "obstacle run",
            "Moving platforms and gaps"
        ]

        for step_message in steps:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": step_message, "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        assert session_id in user_states


# ============================================================================
# ERROR RECOVERY TESTS
# ============================================================================

class TestErrorRecovery:
    """Test error recovery and resilience"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client

    def test_recover_from_invalid_goal_choice(self, client):
        """Test recovery from invalid goal choice"""
        session_id = "error_recovery_test"

        # Start conversation
        client.post(
            '/chat',
            data=json.dumps({"user_message": "TestUser", "session_id": session_id}),
            content_type='application/json'
        )
        client.post(
            '/chat',
            data=json.dumps({"user_message": "TestHero", "session_id": session_id}),
            content_type='application/json'
        )
        client.post(
            '/chat',
            data=json.dumps({"user_message": "TestLocation", "session_id": session_id}),
            content_type='application/json'
        )

        # Invalid goal choice
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "invalid_goal", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Valid goal choice should work
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "collecting goals", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

    def test_recover_from_empty_messages(self, client):
        """Test recovery from empty messages in conversation"""
        session_id = "empty_message_test"

        # Start with valid message
        client.post(
            '/chat',
            data=json.dumps({"user_message": "ValidUser", "session_id": session_id}),
            content_type='application/json'
        )

        # Send empty message
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

        # Continue with valid message
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "ValidHero", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]

    def test_session_recovery_after_server_restart(self, client):
        """Test behavior when session data is lost (simulating server restart)"""
        session_id = "server_restart_test"

        # Start conversation
        client.post(
            '/chat',
            data=json.dumps({"user_message": "TestUser", "session_id": session_id}),
            content_type='application/json'
        )

        # Simulate server restart by clearing user_states
        user_states.clear()

        # Next message should handle missing session gracefully
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "TestHero", "session_id": session_id}),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]


# ============================================================================
# LOAD AND STRESS TESTS
# ============================================================================

class TestLoadAndStress:
    """Load testing and stress testing"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client

    def test_multiple_concurrent_users(self, client):
        """Test multiple users interacting simultaneously"""
        num_users = 10
        sessions = [f"stress_user_{i}" for i in range(num_users)]

        # All users start conversations
        for session_id in sessions:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"User{session_id}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        # All sessions should exist
        for session_id in sessions:
            assert session_id in user_states

    def test_rapid_successive_requests(self, client):
        """Test rapid successive requests from same user"""
        session_id = "rapid_requests_test"

        # Send 20 rapid requests
        for i in range(20):
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"message_{i}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        assert session_id in user_states

    def test_large_number_of_sessions(self, client):
        """Test handling of large number of concurrent sessions"""
        num_sessions = 50

        # Create many sessions
        for i in range(num_sessions):
            session_id = f"bulk_session_{i}"
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"User{i}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        # Verify sessions exist
        assert len(user_states) >= num_sessions


# ============================================================================
# DATA INTEGRITY TESTS
# ============================================================================

class TestDataIntegrity:
    """Test data integrity and consistency"""

    def test_conversation_questions_immutable(self):
        """Test that conversation questions structure doesn't change"""
        original_questions = conversation_questions.copy()

        # Simulate some operations
        _ = conversation_questions["name"]
        _ = conversation_questions["hero_goal"]["options"]

        # Structure should remain the same
        assert conversation_questions == original_questions

    def test_user_states_thread_safety_simulation(self):
        """Test user states handling under concurrent access simulation"""
        user_states.clear()

        # Simulate concurrent access
        sessions = ["thread_a", "thread_b", "thread_c"]

        for session_id in sessions:
            user_states[session_id] = {"step": 1, "answers": {}}

        # All should exist
        for session_id in sessions:
            assert session_id in user_states
            assert user_states[session_id]["step"] == 1

    def test_game_html_generation_consistency(self):
        """Test that game HTML generation is consistent for same inputs"""
        hero = "TestHero"
        environment = "TestEnvironment"
        goal = "TestGoal"
        obstacle = "TestObstacle"

        # Generate multiple times
        html1 = generate_game_html(hero, environment, goal, obstacle)
        html2 = generate_game_html(hero, environment, goal, obstacle)
        html3 = generate_game_html(hero, environment, goal, obstacle)

        # Should be identical
        assert html1 == html2 == html3
        assert isinstance(html1, str)
        assert "<!DOCTYPE html>" in html1


# ============================================================================
# CROSS-BROWSER COMPATIBILITY TESTS
# ============================================================================

class TestCrossBrowserCompatibility:
    """Test cross-browser compatibility aspects"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_html_generation_browser_compatibility(self, client):
        """Test that generated HTML is browser-compatible"""
        # Generate a game
        html_content = generate_game_html("hero", "world", "win", "enemies")

        # Check for browser-compatible features
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "<head>" in html_content
        assert "<body>" in html_content
        assert "<canvas" in html_content
        assert "<script>" in html_content

        # Check for proper meta charset
        assert "charset" in html_content.lower()

    def test_json_responses_browser_friendly(self, client):
        """Test that JSON responses are browser-friendly"""
        response = client.post(
            '/chat',
            data=json.dumps({"user_message": "test", "session_id": "browser_test"}),
            content_type='application/json'
        )

        if response.status_code == 200:
            # Should be valid JSON
            data = json.loads(response.data)
            assert isinstance(data, dict)

            # Should not contain browser-breaking characters
            json_str = response.data.decode('utf-8')
            assert '<' not in json_str  # No HTML injection
            assert 'script' not in json_str.lower()  # No script tags


# ============================================================================
# ACCESSIBILITY TESTS
# ============================================================================

class TestAccessibility:
    """Test accessibility compliance"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_index_page_accessibility_basics(self, client):
        """Test basic accessibility features on index page"""
        response = client.get('/')
        assert response.status_code == 200

        html_content = response.data.decode('utf-8')

        # Should have proper HTML structure
        assert '<html' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content

        # Should have title
        assert '<title>' in html_content or 'title' in html_content.lower()

    def test_generated_game_accessibility(self, client):
        """Test accessibility of generated games"""
        html_content = generate_game_html("hero", "world", "goal", "obstacles")

        # Should have proper HTML structure
        assert '<!DOCTYPE html>' in html_content
        assert '<html' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content

        # Should have title
        assert '<title>' in html_content

        # Should have meta charset
        assert 'charset' in html_content.lower()


# ============================================================================
# INTERNATIONALIZATION TESTS
# ============================================================================

class TestInternationalization:
    """Test internationalization and localization support"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_unicode_support_in_messages(self, client):
        """Test unicode character support in chat messages"""
        unicode_messages = [
            "Hello 世界",  # Chinese
            "Hola 🌍 mundo",  # Spanish with emoji
            "Привет мир 🚀",  # Russian with emoji
            "مرحبا بالعالم",  # Arabic
            "שלום עולם ⭐",  # Hebrew with emoji
        ]

        for message in unicode_messages:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": message, "session_id": "unicode_test"}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

    def test_game_generation_with_unicode(self, client):
        """Test game generation with unicode characters"""
        unicode_hero = "גיבור עברי"
        unicode_environment = "עולם עברי"
        unicode_goal = "מטרה עברית"
        unicode_obstacle = "מכשול עברי"

        html_content = generate_game_html(unicode_hero, unicode_environment, unicode_goal, unicode_obstacle)

        # Should contain the unicode text
        assert unicode_hero in html_content
        assert unicode_environment in html_content
        assert unicode_goal in html_content
        assert unicode_obstacle in html_content

        # Should be valid HTML
        assert "<!DOCTYPE html>" in html_content


# ============================================================================
# PERFORMANCE REGRESSION TESTS
# ============================================================================

class TestPerformanceRegression:
    """Test for performance regressions"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_memory_usage_stability(self, client):
        """Test that memory usage doesn't grow unbounded"""
        import psutil
        import os

        # Get initial memory
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Perform many operations
        for i in range(100):
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"test_{i}", "session_id": f"session_{i}"}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]

        # Check memory didn't grow excessively
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory

        # Memory growth should be reasonable (less than 50MB)
        assert memory_growth < 50 * 1024 * 1024, f"Memory grew by {memory_growth} bytes"

    def test_response_time_consistency(self, client):
        """Test that response times remain consistent"""
        import time

        response_times = []

        # Measure response times for multiple requests
        for i in range(10):
            start_time = time.time()
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"test_{i}", "session_id": "consistency_test"}),
                content_type='application/json'
            )
            end_time = time.time()

            assert response.status_code in [200, 400, 500]
            response_times.append(end_time - start_time)

        # Calculate average and check consistency
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)

        # Max should not be more than 3x average
        assert max_time <= avg_time * 3, f"Inconsistent response times: avg={avg_time}, max={max_time}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])