
### `config.py`
```python
import os
from rich.console import Console

LOG_PATH = "logs/user_finder_zeta.log"
console = Console()

username = None
username_file = None
email = None
email_file = None
permute = False
permuteall = False
csv = False
pdf = False
filter = None
no_nsfw = False
dump = False
proxy = None
verbose = False
timeout = 30
max_concurrent_requests = 30
no_update = False
about = False

dateRaw = None
datePretty = None
userAgent = None

usernameFoundAccounts = None
emailFoundAccounts = None

currentUser = None
currentEmail = None
