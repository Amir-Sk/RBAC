import json
from django.test import Client, TestCase


class ViewsTestCase(TestCase):

    client = Client()
    username = "Joe"
    password = "SGFrdW5hTWF0YXRhIQ=="
    wrong_password = "SGFrYXVuYVNhYmFiYSE="
    credentials = {
        'name': username,
        'password': password
    }

    wrong_password_credentials = {
        'name': username,
        'password': wrong_password
    }

    expected_endpoints = [
        'localhost:8000/index.html', 'localhost:8000/VF/create',
        'localhost:8000/VF/delete'
    ]

    def test_given_invalid_creds_fail_on_authentication(self):
        response = self.authenticate_to_server(self.wrong_password_credentials)
        self.assertEqual(401, response.status_code)
        print("----- END of test - test_given_invalid_creds_fail_on_authentication is Successful -----\n")

    def test_given_valid_creds_success_on_authentication(self):
        response = self.authenticate_to_server(self.credentials)
        self.assertEqual(200, response.status_code)
        print("----- End of test - test_given_valid_creds_success_on_authentication is Successful -----\n")

    def test_given_successful_auth_verify_endpoints(self):
        response = self.authenticate_to_server(self.credentials)
        data = json.loads(response.content)
        self.assertEqual(data["endpoints"], ViewsTestCase.expected_endpoints)
        print("----- End of test - test_given_successful_auth_verify_endpoints is Successful -----\n")

    @classmethod
    def authenticate_to_server(cls, credentials):
        return ViewsTestCase.client.post('/authenticate/', credentials)
