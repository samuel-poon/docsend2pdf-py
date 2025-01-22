# DocSend2PDF (Unofficial)

Use DocSend2PDF with Python. I am not affiliated with DocSend2PDF or DocSend in any way.

## Installation
```bash
pip3 install docsend2pdf
```

## Quick Start
```python
from docsend2pdf import DocSendClient

docsend_client = DocSendClient()

docsend_client.download(
    file_name=FILE_NAME # Required, (e.g. 'output.pdf')
    url=URL,            # Required (e.g. 'https://docsend.com/view/abc123')
    email=EMAIL,        # Optional
    passcode=PASSCODE,  # Optional
    searchable=True,    # Optional, defaults to True
)
```