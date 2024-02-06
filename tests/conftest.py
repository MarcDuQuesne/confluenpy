"""
Common fixtures and utils
"""

import os
import pytest

from dotenv import load_dotenv

load_dotenv()

e2e = pytest.mark.skipif("CONFLUENCE_API_TOKEN" not in os.environ, reason="No Confluence API token set")
