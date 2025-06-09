import os
import json
import unittest
from unittest.mock import patch, MagicMock
from base64 import b64encode

import trigger_pipeline

class TestTriggerPipeline(unittest.TestCase):
    @patch('requests.post')
    @patch.dict(os.environ, {
        'INPUT_ADO_ORG': 'test-org',
        'INPUT_ADO_PROJECT': 'test-project',
        'INPUT_PIPELINE_ID': '123',
        'INPUT_ADO_PAT': 'test-pat',
        'INPUT_REF_NAME': 'refs/heads/test-branch',
        'INPUT_API_VERSION': '7.1',
        'INPUT_TEMPLATE_PARAMETERS': json.dumps({
            'GROUP_ID': 'uk.gov.hmcts.test',
            'ARTIFACT_ID': 'test-artifact',
            'ARTIFACT_VERSION': '0.0.1'
        })
    }, clear=True)
    def test_trigger_pipeline_execution(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'Pipeline triggered'
        mock_response.json.return_value = {"status": "queued", "id": 1234567890}
        mock_post.return_value = mock_response

        with patch('builtins.print'):
            trigger_pipeline.main()

        expected_url = "https://dev.azure.com/test-org/test-project/_apis/pipelines/123/runs?api-version=7.1"
        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + b64encode(b":test-pat").decode()
        }
        expected_payload = {
            "resources": {
                "repositories": {
                    "self": {
                        "refName": "refs/heads/test-branch"
                    }
                }
            },
            "templateParameters": {
                'GROUP_ID': 'uk.gov.hmcts.test',
                'ARTIFACT_ID': 'test-artifact',
                'ARTIFACT_VERSION': '0.0.1'
            }
        }

        mock_post.assert_called_once_with(expected_url, headers=expected_headers, json=expected_payload)

    @patch.dict(os.environ, {
        'INPUT_ADO_ORG': 'test-org',
        'INPUT_ADO_PROJECT': 'test-project',
        'INPUT_PIPELINE_ID': '123',
        'INPUT_ADO_PAT': 'test-pat',
        'INPUT_REF_NAME': 'refs/heads/test-branch',
        'INPUT_API_VERSION': '7.1',
        'INPUT_TEMPLATE_PARAMETERS': '{}'
    }, clear=True)
    def test_fails_with_empty_template_parameters(self):
        with self.assertRaises(SystemExit) as cm, patch('builtins.print') as mock_print:
            trigger_pipeline.main()
        mock_print.assert_any_call("No template parameters provided. 'template-parameters' input must not be empty.")
        self.assertEqual(cm.exception.code, 1)

    @patch.dict(os.environ, {
        'INPUT_ADO_ORG': 'test-org',
        'INPUT_ADO_PROJECT': 'test-project',
        'INPUT_PIPELINE_ID': '123',
        'INPUT_ADO_PAT': 'test-pat',
        'INPUT_REF_NAME': 'refs/heads/test-branch',
        'INPUT_API_VERSION': '7.1',
        'INPUT_TEMPLATE_PARAMETERS': '{"invalid_json": }'
    }, clear=True)
    def test_fails_with_invalid_json(self):
        with self.assertRaises(SystemExit) as cm, patch('builtins.print') as mock_print:
            trigger_pipeline.main()
        mock_print.assert_any_call("Invalid JSON for template parameters")
        self.assertEqual(cm.exception.code, 1)

    @patch.dict(os.environ, {}, clear=True)
    def test_fails_with_missing_required_env_vars(self):
        with self.assertRaises(SystemExit) as cm, patch('builtins.print') as mock_print:
            trigger_pipeline.main()
        mock_print.assert_any_call("Missing required inputs: ADO_ORG, ADO_PROJECT, PIPELINE_ID, ADO_PAT, REF_NAME, API_VERSION, TEMPLATE_PARAMETERS")
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()