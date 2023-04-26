

import sqlite3
import unittest
from unittest.mock import patch, Mock, MagicMock
import streamlit as st

from streamlit.utils import create_users_table,register_user,get_credentials,list_files_in_drive,login_user,log_queries,get_search_history,display_files_in_drive


class TestFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up SQLite database connection and cursor
        cls.conn = sqlite3.connect("test_users.db")
        cls.c = cls.conn.cursor()
        
        # Create users table and history table in the test database
        
        create_users_table(cls.conn, cls.c)
        
    @classmethod
    def tearDownClass(cls):
        # Drop the users table and history table from the test database
        cls.c.execute("DROP TABLE IF EXISTS users")
        cls.conn.commit()
        
        cls.c.execute("DROP TABLE IF EXISTS history")
        cls.conn.commit()
        
        cls.conn.close()
        
    def test_create_users_table(self):
        # Test creating the users table in the test database
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = self.c.fetchone()
        self.assertIsNotNone(result)
        
    def test_register_user(self):
        # Mock the Streamlit text_input and button widgets for testing
        with patch("streamlit.sidebar.text_input") as mock_text_input, \
             patch("streamlit.sidebar.button") as mock_button:
            
            # Set the mock return values for the user registration form
            mock_text_input.side_effect = ["test_user", "test_password"]
            mock_button.return_value = True
            
            # Call the register_user function and check the database for the new user
            register_user(self.c)
            self.c.execute("SELECT * FROM users WHERE username=?", ("test_user",))
            result = self.c.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], "d9e4e9c8e0236c4b7384464c4d369be0fb5e489f1e2f0c56e9b7de25d3c3cbdd")
            
    def test_login_user(self):
        # Mock the Streamlit text_input and button widgets for testing
        with patch("streamlit.sidebar.text_input") as mock_text_input, \
             patch("streamlit.sidebar.button") as mock_button:
            
            # Set the mock return values for the user login form
            mock_text_input.side_effect = ["test_user", "test_password"]
            mock_button.return_value = True
            
            # Call the login_user function and check that the session state username is set
            with patch.object(st.session_state, "username", None):
                login_user(self.c)
                self.assertEqual(st.session_state.username, "test_user")
                
    def test_log_queries(self):
        # Insert a test user into the database
        self.c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("test_user", "test_password_hash"))
        self.conn.commit()
        
        # Call the log_queries function and check the history table for the new query
        log_queries(self.c, "test_user", "test_query")
        self.c.execute("SELECT queries FROM history WHERE username=?", ("test_user",))
        result = self.c.fetchall()
        self.assertEqual(result, [("test_query",)])
        
    def test_get_search_history(self):
            # Insert a test user and query into the database
            self.c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("test_user", "test_password_hash"))
            self.c.execute("INSERT INTO history (username, queries) VALUES (?, ?)", ("test_user", "test_query"))
            self.conn.commit()
            
            # Call the get_search_history function and check that it returns the expected result
            result = get_search_history(self.conn, "test_user")
            expected_result = [("test_query",)]
            self.assertEqual(result, expected_result)


    def test_get_credentials(self):
        # set up the test Streamlit session state
        st.set_option('client.caching', 'test')
        st.session_state.creds = None

        # call the function and check that it returns a valid Google Drive API service object
        service = get_credentials()
        self.assertIsNotNone(service)
        self.assertTrue(service._http.request.credentials.valid)



    def test_list_files_in_drive():
        # Create a mock service object
        mock_service = MagicMock()

        # Mock the results of the files().list() method
        mock_results = {
            "files": [
                {"name": "Folder1", "mimeType": "application/vnd.google-apps.folder"},
                {"name": "File1", "mimeType": "application/pdf"},
                {"name": "Folder2", "mimeType": "application/vnd.google-apps.folder"},
                {"name": "File2", "mimeType": "application/vnd.google-apps.document"},
            ]
        }
        mock_service.files().list().execute.return_value = mock_results

        # Replace the get_credentials() function with a mock that returns a mock credentials object
        with patch("module.get_credentials", return_value=MagicMock()):
            # Call the list_files_in_drive() function and capture the output
            with patch("streamlit.write") as mock_write:
                list_files_in_drive()

        # Check that the expected output was generated
        assert mock_write.call_count == 4
        assert mock_write.call_args_list[0][0][0] == "Files in Google Drive"
        assert mock_write.call_args_list[1][0][0] == "Folder: Folder1"
        assert mock_write.call_args_list[2][0][0] == "File: File1"
        assert mock_write.call_args_list[3][0][0] == "Folder: Folder2"

if __name__ == '__main__':
    unittest.main()