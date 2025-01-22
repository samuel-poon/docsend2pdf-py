import requests
from bs4 import BeautifulSoup

from .exceptions import InvalidPDFError

class DocSendClient:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_tokens = {}
    
    def generate_csrf_tokens(self):
        try:
            r = self.session.get('https://docsend2pdf.com/')
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException('Failed to generate CSRF tokens.') from e

        cookies = self.session.cookies.get_dict()
        soup = BeautifulSoup(r.content, 'html.parser')

        csrftoken = cookies['csrftoken']
        csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

        return {
            'csrftoken': csrftoken,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
    
    def refresh_csrf_tokens(self):
        self.csrf_tokens = self.generate_csrf_tokens()
    
    def get_pdf(
            self,
            url:str,
            email:str               = '',
            passcode:str            = '',
            searchable: bool        = True,
        ) -> bytes:

        if not all(key in self.csrf_tokens for key in ['csrftoken', 'csrfmiddlewaretoken']):
            self.refresh_csrf_tokens()

        payload = {
            'csrfmiddlewaretoken': self.csrf_tokens.get('csrfmiddlewaretoken'),
            'url': url,
            'email': email,
            'passcode': passcode,
            'searchable': 'on' if searchable else 'off'
        }
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'csrftoken={self.csrf_tokens.get("csrftoken")}',
            'Origin': 'https://docsend2pdf.com',
            'Referer': 'https://docsend2pdf.com/',
        }

        response = requests.post('https://docsend2pdf.com/', headers=headers, data=payload)
        
        if response.content.startswith(b'%PDF-'): # All valid PDFs should start with %PDF-
            return response.content
        
        else:
            raise InvalidPDFError(f'Failed to download PDF. Is {url} a valid DocSend link? Check if an email or password is required.')
        
    def download(
            self,
            file_name:str,
            url:str,
            email:str       = '',
            passcode:str    = '',
            searchable:bool = True
    ) -> None:
        pdf = self.get_pdf(url=url, email=email, passcode=passcode, searchable=searchable)
        
        with open(file_name, 'wb') as f:
            f.write(pdf)