import urllib.request
import re

class UrlParser:
    """
    Model class handling standard internet protocols to extract raw structured text content.
    """
    def __init__(self):
        pass

    def extract_title(self, url):
        """
        Attempts to load a web page and extract the text from its <title> HTML tag.
        Handles possible timeouts or parsing errors and returns a clean string.
        :param url: Complete hyperlink string starting with HTTP protocols
        :return: Trimmed header string content from the network stream
        :raises Exception: Occurs on connection timeouts or resolution errors
        """
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                html_source = response.read().decode('utf-8', errors='ignore')
                
            match = re.search(r'<title.*?>(.*?)</title>', html_source, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            return None
        except Exception as e:
            raise Exception(f"Failed to extract page from URL: {e}")
