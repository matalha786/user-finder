# user-finder
Here is the `README.md` file for your GitHub repository:

```markdown
# User Finder Zeta

User Finder Zeta is an OSINT (Open Source Intelligence) tool that allows you to search for accounts by username or email across various social media platforms. The tool can generate reports in CSV, TXT, and PDF formats.

## Features

- Search for usernames across multiple platforms.
- Search for emails across multiple platforms.
- Permutation of usernames to find all possible variations.
- Generate reports in CSV, TXT, and PDF formats.
- API integration for GitHub, Mastodon, and Discord.
- Proxy support for HTTP requests.
- Timeout and rate limit handling.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/user-finder-zeta.git
    cd user-finder-zeta
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface (CLI)

You can run the tool using the command line interface with various options.

#### Basic Usage

```sh
python user_finder_zeta.py -u username1 username2 
python user_finder_zeta.py -e email1@example.com email2@example.com

```

#### Advanced Options

- `-u, --username`: One or more usernames to search.
- `-uf, --username-file`: The list of usernames to be searched from a file.
- `--permute`: Permute usernames, ignoring single elements.
- `--permuteall`: Permute usernames, all elements.
- `-e, --email`: One or more emails to search.
- `-ef, --email-file`: The list of emails to be searched from a file.
- `--csv`: Generate a CSV with the results.
- `--pdf`: Generate a PDF with the results.
- `--filter`: Filter sites to be searched by list property value. E.g., --filter "cat=social".
- `--no-nsfw`: Removes NSFW sites from the search.
- `--dump`: Dump HTML content for found accounts.
- `--proxy`: Proxy to send HTTP requests through.
- `--timeout`: Timeout in seconds for each HTTP request (Default is 30).
- `--max-concurrent-requests`: Specify the maximum number of concurrent requests allowed (Default is 30).
- `--no-update`: Don't update sites lists.
- `--about`: Show about information and exit.
- `-p, --profile`: Search related profiles (API key may be required).

### Graphical User Interface (GUI)

The tool also includes a graphical user interface for ease of use.

#### Running the GUI

1. Run the `user_finder_gui.py` script:
    ```sh
    python user_finder_gui.py
    ```

2. Enter the usernames and emails you want to search for.
3. Select the permutation options if needed.
4. Click "Start Search" to begin the search.
![Capture](https://github.com/matalha786/user-finder/assets/85659813/c7778618-5345-4484-99fc-c2aa3c4cdf0d)

## Examples

### Searching for Usernames

```sh
python user_finder_zeta.py -u john_doe jane_doe
```

### Searching for Emails

```sh
python user_finder_zeta.py -e john@example.com jane@example.com
```

### Permute Usernames (Strict)

```sh
python user_finder_zeta.py -u john_doe jane_doe --permute
```

### Permute Usernames (All)

```sh
python user_finder_zeta.py -u john_doe jane_doe --permuteall
```

### Generate CSV and PDF Reports

```sh
python user_finder_zeta.py -u john_doe -e john@example.com --csv --pdf
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## About

User Finder Zeta is developed by Team Zeta ITSOLERA. For more information, visit our [GitHub page](https://github.com/matalha786).

## Acknowledgements

Thanks to all the contributors and the OSINT community for their support and contributions.

```

Make sure to replace `yourusername` with your actual GitHub username and update any specific project details as needed.
