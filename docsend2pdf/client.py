import requests
from bs4 import BeautifulSoup

from .exceptions import InvalidPDFError, InvalidURLError, InvalidCredentialsError

class DocSendClient:    
    def generate_csrf_tokens(self) -> dict:
        try:
            r = requests.get('https://docsend2pdf.com/')
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException('Failed to generate CSRF tokens.') from e

        cookies = r.cookies.get_dict()
        soup = BeautifulSoup(r.content, 'html.parser')

        csrftoken = cookies['csrftoken']
        csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

        return {
            'csrftoken': csrftoken,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
    
    def get_pdf(
            self,
            url:str,
            email:str               = '',
            passcode:str            = '',
            searchable: bool        = True,
        ) -> bytes:

        csrf_tokens = self.generate_csrf_tokens()

        payload = {
            'csrfmiddlewaretoken': csrf_tokens.get('csrfmiddlewaretoken'),
            'url': url,
            'email': email,
            'passcode': passcode,
            'searchable': 'on' if searchable else 'off'
        }
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'csrftoken={csrf_tokens.get("csrftoken")}',
            'Origin': 'https://docsend2pdf.com',
            'Referer': 'https://docsend2pdf.com/',
        }

        response = requests.post('https://docsend2pdf.com/', headers=headers, data=payload)
        
        if response.content.startswith(b'%PDF-'): # All valid PDFs should start with %PDF-
            return response.content
        
        # To do: see if there is a more robust way of checking for errors
        elif response.headers.get('Content-Type') == 'text/html; charset=utf-8':
            soup = BeautifulSoup(response.content, 'html.parser')

            if soup.find('p', {'class':'text-danger'}):
                text_danger = soup.find('p', {'class':'text-danger'}).text
            
                if text_danger.startswith('Unable to authenticate with provided credentials'):
                    raise InvalidCredentialsError(f'Failed to authenticate with provided credentials. Check if {passcode} is the correct password.')
        
                if text_danger.startswith('Invalid url'):
                    raise InvalidURLError(f'{url} is not a valid DocSend link. Please check the URL and try again.')
    
        # Catch if error cannot be determined
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