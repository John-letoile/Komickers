# Komickers

Download your comics automatically, using your terminal alone.

Komickers reads your comic pull list from [League of Comic Geeks](https://leagueofcomicgeeks.com/) email notifications, extracts download links from [GetComics.org](https://getcomics.org), and batch-downloads your comics using an external download manager.

## Features

- **Email Integration** -- Reads pull list emails via Gmail API (OAuth2) or IMAP
- **Automatic Extraction** -- Parses HTML emails to extract comic names and download links
- **Batch Downloading** -- Resolves and downloads all comics via Surge, uGet, or wget2
- **Pull List Caching** -- Avoids re-downloading previously fetched pull lists
- **Inventory Tracking** -- Tracks pulled vs. missed comics
- **Manual Mode** -- Download comics from a text file of comic names

## Requirements

- Python >= 3.11
- `curl` available on your system PATH
- One of the supported download managers:
  - [Surge](https://github.com/yt-dlp/surge) (default)
  - [uGet](http://ugetdm.com/)
  - [wget2](https://gitlab.com/gnuwget/wget2)

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/ArshiaShaygan/Komickers.git
cd Komickers
uv sync                     # install base dependencies
uv sync --extra google      # with Gmail API support
uv sync --all-extras        # include dev tools (pytest, ruff, mypy)
```

### Using pip

```bash
git clone https://github.com/ArshiaShaygan/Komickers.git
cd Komickers
pip install .
pip install ".[google]"     # with Gmail API support
```

## Usage

```bash
komickers
# or
python -m komickers
```

### Main Menu

| Key | Action |
|-----|--------|
| `c` | Change configuration |
| `p` | Pull latest pull list (email -> extract -> download) |
| `d` | Download comics from a text file |
| `q` | Quit |

### Configuration

On first run, or by pressing `c` in the main menu, you can configure:

- **Email address** -- Your Gmail address
- **Email provider** -- Default: `noreply@leagueofcomicgeeks.com`
- **Authentication** -- IMAP App Password or Google OAuth2 credentials
- **Downloads directory** -- Default: `./inbox`
- **Download manager** -- `surge` (default), `uget`, or `wget2`
- **Temp directory** -- Default: `./.tmp`

Settings are saved to `.config/komickers.toml`.

## Project Structure

```
Komickers/
├── .config/komickers.toml        # User configuration
├── credentials/                  # Google OAuth credentials (gitignored)
├── inbox/                        # Downloaded comics
├── token/                        # Google OAuth tokens (gitignored)
├── src/komickers/
│   ├── main.py                   # Entry point and main menu loop
│   ├── config.py                 # TOML configuration loading
│   ├── mail_reader/              # Email reading (Gmail API / IMAP)
│   ├── core/
│   │   ├── extractor.py          # HTML parsing and link extraction
│   │   └── downloader.py         # Download orchestration
│   └── menu/                     # Interactive terminal menus
└── pyproject.toml                # Project metadata and dependencies
```

## License

MIT License. See [LICENSE](LICENSE) for details.
