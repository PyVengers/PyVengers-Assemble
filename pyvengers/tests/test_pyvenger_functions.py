import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
from main import search_pyvenger, add_pyvenger, list_pyvengers, interactive_menu, DATA_FILE

class TestPyVengers(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "IronMan", "superpower": "Super Strength", "mission": "Save the world"}, {"name": "SpiderMan", "superpower": "Web-Slinging", "mission": "Protect the neighborhood"}]')
    @patch('os.path.exists', return_value=True)
    def test_search_pyvenger_found(self, mock_exists, mock_file):
    # Test searching for a PyVenger with a partial name match
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            search_pyvenger("Man")  # Partial match
            output = mock_stdout.getvalue()
            self.assertIn("IronMan", output)
            self.assertIn("SpiderMan", output)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "IronMan", "superpower": "Super Strength", "mission": "Save the world"}]')
    @patch('os.path.exists', return_value=True)
    def test_search_pyvenger_not_found(self, mock_exists, mock_file):
        # Test searching for a PyVenger with no match
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            search_pyvenger("Thor")  # No match
            output = mock_stdout.getvalue()
            self.assertIn("No PyVenger found containing the name 'Thor'.", output)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('os.path.exists', return_value=True)
    def test_add_pyvenger(self, mock_exists, mock_file):
        # Test adding a new PyVenger to the file
        add_pyvenger("IronMan", "Super Strength", "Save the world")
        
        # Verify that the file is opened correctly for writing
        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_any_call(DATA_FILE, "w")
        
        # Check that the JSON is written correctly
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        pyvengers = json.loads(written_data)
        self.assertEqual(pyvengers[0]['name'], "IronMan")
        self.assertEqual(pyvengers[0]['superpower'], "Super Strength")
        self.assertEqual(pyvengers[0]['mission'], "Save the world")

    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "IronMan", "superpower": "Super Strength", "mission": "Save the world"}]')
    @patch('os.path.exists', return_value=True)
    def test_list_pyvengers(self, mock_exists, mock_file):
        # Capture the output of the print function
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_pyvengers()
            
            output = mock_stdout.getvalue()
            self.assertIn("IronMan", output)
            self.assertIn("Super Strength", output)
            self.assertIn("Save the world", output)
            
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('os.path.exists', return_value=False)
    def test_no_pyvengers_file(self, mock_exists, mock_file):
        # Test if there are no PyVengers yet when the file does not exist
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_pyvengers()
            output = mock_stdout.getvalue()
            self.assertIn("No PyVengers yet! Add one now.", output)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('os.path.exists', return_value=True)
    def test_list_empty_pyvengers(self, mock_exists, mock_file):
        # Test if there are no PyVengers yet when the list is empty
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_pyvengers()
            output = mock_stdout.getvalue()
            self.assertIn("No PyVengers yet! Add one now.", output)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "IronMan", "superpower": "Super Strength", "mission": "Save the world"}]')
    @patch('os.path.exists', return_value=True)
    def test_interactive_menu_list_option(self, mock_exists, mock_file):
        # Test the list option in the interactive menu
        with patch('builtins.input', side_effect=['2', '4']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            interactive_menu()
            output = mock_stdout.getvalue()
            self.assertIn("PyVengers List:", output)
            self.assertIn("IronMan", output)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "IronMan", "superpower": "Super Strength", "mission": "Save the world"}]')
    @patch('os.path.exists', return_value=True)
    def test_interactive_menu_add_option(self, mock_exists, mock_file):
        # Test the add PyVenger option in the interactive menu
        with patch('builtins.input', side_effect=['1', 'Hulk', 'Strength', 'Smash', '4']):
            interactive_menu()
        
        # Check if the file was written with the new PyVenger
        mock_file.assert_called_with(DATA_FILE, 'w')
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        added_pyvenger = json.loads(written_data)
        self.assertEqual(len(added_pyvenger), 2)
        self.assertEqual(added_pyvenger[1]['name'], 'Hulk')

if __name__ == '__main__':
    unittest.main()
