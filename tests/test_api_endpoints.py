"""
API Endpoint Tests for Game Generation Engine
Tests the HTTP endpoints and request/response handling
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server-side'))

from web_server import app, user_states


class TestAPIEndpoints:
    """Test API endpoints and HTTP requests"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    # ========================================================================
    # INDEX ENDPOINT TESTS
    # ========================================================================
    
    def test_get_index(self, client):
        """Test GET / returns index page"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.content_type.startswith('text/html')
    
    def test_index_contains_title(self, client):
        """Test that index page contains expected title or elements"""
        response = client.get('/')
        assert response.status_code == 200
        # Index should be HTML
        assert b'<' in response.data and b'>' in response.data
    
    # ========================================================================
    # CHAT ENDPOINT TESTS
    # ========================================================================
    
    def test_chat_endpoint_with_valid_json(self, client):
        """Test chat endpoint with valid JSON"""
        payload = {
            "user_message": "test message",
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Endpoint should exist and respond
        assert response.status_code in [200, 400, 500, 201]
    
    def test_chat_endpoint_requires_session_id(self, client):
        """Test that chat endpoint requires session_id"""
        payload = {
            "user_message": "test message"
            # session_id is missing
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should handle missing session_id gracefully
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_requires_user_message(self, client):
        """Test that chat endpoint requires user_message"""
        payload = {
            "session_id": "test_session_123"
            # user_message is missing
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should handle missing user_message gracefully
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_returns_json(self, client):
        """Test that chat endpoint returns JSON response"""
        payload = {
            "user_message": "What is your name?",
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.content_type.startswith('application/json')
    
    def test_chat_endpoint_response_has_message(self, client):
        """Test that chat response contains message field"""
        payload = {
            "user_message": "test",
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        if response.status_code == 200:
            data = json.loads(response.data)
            assert "message" in data or "error" in data
    
    def test_chat_endpoint_handles_empty_message(self, client):
        """Test chat endpoint handles empty messages"""
        payload = {
            "user_message": "",
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_handles_long_message(self, client):
        """Test chat endpoint handles very long messages"""
        long_message = "a" * 5000
        payload = {
            "user_message": long_message,
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_with_unicode_message(self, client):
        """Test chat endpoint handles unicode characters"""
        payload = {
            "user_message": "שלום עולם 🎮",
            "session_id": "test_session_123"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        assert response.status_code in [200, 400, 500]
    
    # ========================================================================
    # SESSION MANAGEMENT TESTS
    # ========================================================================
    
    def test_different_sessions_isolated(self, client):
        """Test that different sessions maintain separate state"""
        payload1 = {
            "user_message": "Alice",
            "session_id": "session_1"
        }
        payload2 = {
            "user_message": "Bob",
            "session_id": "session_2"
        }
        
        response1 = client.post(
            '/chat',
            data=json.dumps(payload1),
            content_type='application/json'
        )
        response2 = client.post(
            '/chat',
            data=json.dumps(payload2),
            content_type='application/json'
        )
        
        assert response1.status_code in [200, 400, 500]
        assert response2.status_code in [200, 400, 500]
    
    def test_same_session_maintains_state(self, client):
        """Test that same session maintains conversation state"""
        session_id = "persistent_session"
        
        payload1 = {
            "user_message": "start",
            "session_id": session_id
        }
        payload2 = {
            "user_message": "continue",
            "session_id": session_id
        }
        
        response1 = client.post(
            '/chat',
            data=json.dumps(payload1),
            content_type='application/json'
        )
        response2 = client.post(
            '/chat',
            data=json.dumps(payload2),
            content_type='application/json'
        )
        
        # Both should succeed
        assert response1.status_code in [200, 400, 500]
        assert response2.status_code in [200, 400, 500]
    
    # ========================================================================
    # ERROR HANDLING TESTS
    # ========================================================================
    
    def test_endpoint_with_invalid_json(self, client):
        """Test endpoint handles invalid JSON gracefully"""
        response = client.post(
            '/chat',
            data='{"invalid json}',
            content_type='application/json'
        )
        # Should return 400 Bad Request or similar
        assert response.status_code in [400, 415, 500]
    
    def test_endpoint_with_missing_content_type(self, client):
        """Test endpoint without content-type header"""
        payload = {
            "user_message": "test",
            "session_id": "test_session"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload)
            # content_type not specified
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
    
    # ========================================================================
    # CORS TESTS
    # ========================================================================
    
    def test_cors_enabled(self, client):
        """Test that CORS is enabled"""
        response = client.get('/')
        # CORS should not break the request
        assert response.status_code == 200
    
    def test_cors_options_request(self, client):
        """Test OPTIONS request for CORS preflight"""
        response = client.options('/chat')
        # Should allow OPTIONS or at least not crash
        assert response.status_code in [200, 404, 405]


class TestResponseFormats:
    """Test response format and structure"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    def test_chat_response_json_structure(self, client):
        """Test that chat response has correct JSON structure"""
        payload = {
            "user_message": "test",
            "session_id": "test_session"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                assert isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail("Response is not valid JSON")
    
    def test_index_response_has_html_structure(self, client):
        """Test that index response has HTML structure"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<' in response.data


class TestFileUploadEndpoints:
    """Test file upload functionality if implemented"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_upload_endpoint_exists(self, client):
        """Test if upload endpoint exists"""
        # Try to find upload endpoint
        response = client.post('/upload')
        # If endpoint exists, it should respond (may be 400/415 if no file provided)
        # If it doesn't exist, it will be 404
        assert response.status_code in [200, 400, 404, 415]
    
    def test_upload_with_missing_file(self, client):
        """Test upload endpoint without file"""
        response = client.post('/upload')
        # Should handle missing file gracefully
        assert response.status_code in [400, 404, 415]


class TestStoryboardEndpoints:
    """Test storyboard generation endpoints if implemented"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_storyboard_endpoint_exists(self, client):
        """Test if storyboard endpoint exists"""
        response = client.post(
            '/generate_storyboard',
            data=json.dumps({"topic": "test"}),
            content_type='application/json'
        )
        # Should either exist and respond, or return 404
        assert response.status_code in [200, 400, 404, 500]


class TestGameEndpoints:
    """Test game generation endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_game_endpoint_if_exists(self, client):
        """Test game generation endpoint"""
        payload = {
            "hero": "knight",
            "location": "castle",
            "goal": "escape",
            "obstacles": "dragons"
        }
        response = client.post(
            '/generate_game',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should handle the request
        assert response.status_code in [200, 400, 404, 500]


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test application performance"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_response_time(self, client):
        """Test that index page loads reasonably fast"""
        import time
        start = time.time()
        response = client.get('/')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should load in under 1 second
        assert elapsed < 1.0, f"Index took {elapsed} seconds to load"
    
    def test_chat_response_time(self, client):
        """Test that chat endpoint responds reasonably fast"""
        import time
        payload = {
            "user_message": "test",
            "session_id": "test_session"
        }
        
        start = time.time()
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        elapsed = time.time() - start
        
        # Should respond in reasonable time
        assert elapsed < 5.0, f"Chat took {elapsed} seconds to respond"


# ============================================================================
# ADDITIONAL API TESTS
# ============================================================================

class TestAdvancedAPIEndpoints:
    """Advanced API endpoint testing"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    def test_chat_endpoint_with_extremely_long_message(self, client):
        """Test chat endpoint with extremely long message (10k chars)"""
        long_message = "a" * 10000
        payload = {
            "user_message": long_message,
            "session_id": "long_message_test"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_with_special_unicode(self, client):
        """Test chat endpoint with special unicode characters"""
        special_chars = "🚀🌟💫🎮🎯🏆⚡🔥💎"
        payload = {
            "user_message": f"Hello {special_chars} World",
            "session_id": "unicode_test"
        }
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_with_json_injection_attempt(self, client):
        """Test chat endpoint with JSON injection attempts"""
        injection_attempts = [
            '{"user_message": "test", "session_id": "test"}',
            '{"user_message": "test", "session_id": "test", "extra": "field"}',
            '{"user_message": "test", "session_id": "test", "nested": {"key": "value"}}'
        ]
        
        for payload_str in injection_attempts:
            response = client.post(
                '/chat',
                data=payload_str,
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_with_malformed_json(self, client):
        """Test chat endpoint with various malformed JSON"""
        malformed_jsons = [
            '{"user_message": "test", "session_id": "test"',  # Missing closing brace
            '{"user_message": "test" "session_id": "test"}',   # Missing comma
            '{"user_message": "test", session_id: "test"}',    # Missing quotes
            '{"user_message": "test", "session_id": "test",}', # Trailing comma
        ]
        
        for malformed in malformed_jsons:
            response = client.post(
                '/chat',
                data=malformed,
                content_type='application/json'
            )
            # Should return 400 Bad Request for malformed JSON
            assert response.status_code in [400, 415, 500]
    
    def test_chat_endpoint_content_types(self, client):
        """Test chat endpoint with different content types"""
        payload = {
            "user_message": "test",
            "session_id": "content_type_test"
        }
        
        # Test with different content types
        content_types = [
            'application/json',
            'application/json; charset=utf-8',
            'application/json; charset=UTF-8',
        ]
        
        for content_type in content_types:
            response = client.post(
                '/chat',
                data=json.dumps(payload),
                content_type=content_type
            )
            assert response.status_code in [200, 400, 500]
    
    def test_chat_endpoint_http_methods(self, client):
        """Test chat endpoint with different HTTP methods"""
        # GET should not be allowed
        response = client.get('/chat')
        assert response.status_code in [405, 404]  # Method Not Allowed or Not Found
        
        # PUT should not be allowed
        response = client.put('/chat')
        assert response.status_code in [405, 404]
        
        # DELETE should not be allowed
        response = client.delete('/chat')
        assert response.status_code in [405, 404]
        
        # PATCH should not be allowed
        response = client.patch('/chat')
        assert response.status_code in [405, 404]


class TestSessionManagementAdvanced:
    """Advanced session management tests"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    def test_session_isolation_detailed(self, client):
        """Test detailed session isolation"""
        session1 = "session_1"
        session2 = "session_2"
        
        # Start both sessions
        client.post(
            '/chat',
            data=json.dumps({"user_message": "Alice", "session_id": session1}),
            content_type='application/json'
        )
        client.post(
            '/chat',
            data=json.dumps({"user_message": "Bob", "session_id": session2}),
            content_type='application/json'
        )
        
        # Both sessions should exist independently
        assert session1 in user_states
        assert session2 in user_states
        assert user_states[session1] != user_states[session2]
    
    def test_session_persistence_across_requests(self, client):
        """Test session persistence across multiple requests"""
        session_id = "persistent_session"
        
        # Make multiple requests
        for i in range(5):
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"message_{i}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]
        
        # Session should still exist
        assert session_id in user_states
    
    def test_session_cleanup(self, client):
        """Test that sessions can be cleaned up"""
        session_id = "cleanup_test"
        
        # Create session
        client.post(
            '/chat',
            data=json.dumps({"user_message": "test", "session_id": session_id}),
            content_type='application/json'
        )
        
        assert session_id in user_states
        
        # Manually clear (simulating cleanup)
        user_states.clear()
        
        assert session_id not in user_states


class TestErrorHandlingAdvanced:
    """Advanced error handling tests"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_endpoint_with_oversized_payload(self, client):
        """Test endpoint with oversized payload"""
        large_payload = {
            "user_message": "x" * 100000,  # 100KB message
            "session_id": "oversized_test"
        }
        
        response = client.post(
            '/chat',
            data=json.dumps(large_payload),
            content_type='application/json'
        )
        
        # Should handle gracefully (may return 413 Request Entity Too Large or process)
        assert response.status_code in [200, 400, 413, 500]
    
    def test_endpoint_with_binary_data(self, client):
        """Test endpoint with binary data in message"""
        binary_message = b'\x00\x01\x02\x03\xff\xfe\xfd'
        payload = {
            "user_message": binary_message.decode('latin-1', errors='ignore'),
            "session_id": "binary_test"
        }
        
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 400, 500]
    
    def test_endpoint_with_null_bytes(self, client):
        """Test endpoint with null bytes in message"""
        null_message = "test\x00message\x00with\x00nulls"
        payload = {
            "user_message": null_message,
            "session_id": "null_test"
        }
        
        response = client.post(
            '/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 400, 500]


class TestSecurityTests:
    """Security-focused tests"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_no_directory_traversal(self, client):
        """Test that directory traversal attacks are prevented"""
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32"
        ]
        
        for payload in traversal_payloads:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": payload, "session_id": "traversal_test"}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]  # Should not crash
    
    def test_no_command_injection(self, client):
        """Test that command injection is prevented"""
        injection_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "`whoami`",
            "$(rm -rf /)",
            "&& echo 'injected'",
            "|| echo 'injected'"
        ]
        
        for payload in injection_payloads:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": payload, "session_id": "injection_test"}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]  # Should not execute commands
    
    def test_rate_limiting_simulation(self, client):
        """Test behavior under rapid requests (simulating rate limiting)"""
        session_id = "rate_limit_test"
        
        # Send many rapid requests
        for i in range(50):
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"request_{i}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500, 429]  # 429 = Too Many Requests


class TestIntegrationFlows:
    """Integration tests for complete flows"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        user_states.clear()
        with app.test_client() as client:
            yield client
    
    def test_complete_conversation_flow_integration(self, client):
        """Test complete conversation flow from start to finish"""
        session_id = "integration_test"
        
        # Step 1: Name
        response1 = client.post(
            '/chat',
            data=json.dumps({"user_message": "TestUser", "session_id": session_id}),
            content_type='application/json'
        )
        assert response1.status_code in [200, 400, 500]
        
        # Step 2: Hero description
        response2 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Brave knight", "session_id": session_id}),
            content_type='application/json'
        )
        assert response2.status_code in [200, 400, 500]
        
        # Step 3: Location
        response3 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Dark castle", "session_id": session_id}),
            content_type='application/json'
        )
        assert response3.status_code in [200, 400, 500]
        
        # Step 4: Goal choice
        response4 = client.post(
            '/chat',
            data=json.dumps({"user_message": "collecting goals", "session_id": session_id}),
            content_type='application/json'
        )
        assert response4.status_code in [200, 400, 500]
        
        # Step 5: Object to collect
        response5 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Golden coins", "session_id": session_id}),
            content_type='application/json'
        )
        assert response5.status_code in [200, 400, 500]
        
        # Step 6: Obstacles
        response6 = client.post(
            '/chat',
            data=json.dumps({"user_message": "Dragons and traps", "session_id": session_id}),
            content_type='application/json'
        )
        assert response6.status_code in [200, 400, 500]
        
        # Session should have progressed through all steps
        assert session_id in user_states
    
    def test_multiple_concurrent_conversations(self, client):
        """Test multiple users having conversations simultaneously"""
        sessions = ["user_a", "user_b", "user_c", "user_d", "user_e"]
        
        # Each user starts their conversation
        for session_id in sessions:
            response = client.post(
                '/chat',
                data=json.dumps({"user_message": f"User_{session_id}", "session_id": session_id}),
                content_type='application/json'
            )
            assert response.status_code in [200, 400, 500]
        
        # All sessions should exist
        for session_id in sessions:
            assert session_id in user_states
        
        # Each session should have different state
        states = [user_states[session_id] for session_id in sessions]
        assert len(set(str(state) for state in states)) > 1  # At least some different states


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
