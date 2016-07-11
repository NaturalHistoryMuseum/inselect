#!/usr/bin/env python3
"""Creates a news article per release
"""
import re

from pathlib import Path

import requests

# Github
OWNER = 'NaturalHistoryMuseum'
REPO = 'inselect'
API = 'https://api.github.com/repos/{owner}/{repo}/releases'

# Write articles here
OUTPUT = Path('content/news')
SANITIZE_FNAME = re.compile('[^a-zA-Z0-9_\.\- \(\)]')

# Link to github issues
GITHUB_ISSUE = re.compile(' #([0-9]+)')

# Markdown for github issue
ISSUE_MD = ' [{number}](https://github.com/NaturalHistoryMuseum/inselect/issues/{number})'

# Markdown template
DOCUMENT = """Title: Inselect {title} released

You can [download {title}]({link}).

{body}
"""

res = requests.get(API.format(owner=OWNER, repo=REPO))

for release in res.json():
    # Link to github issues
    body = GITHUB_ISSUE.sub(
        lambda match: ISSUE_MD.format(number=match.group(1)), release['body']
    )
    # Remove Windows line endings
    body = body.replace('\r', '')
    doc = DOCUMENT.format(
        title=release['name'], link=release['html_url'], body=body
    )
    # In the form YYYY-MM-DD-vx.y.z.md
    fname = '{date}-{title}.md'.format(
        date=release['published_at'][:10], title=release['name']
    )
    # TODO How best to sanitize filenames?
    fname = SANITIZE_FNAME.sub('_', fname)
    with OUTPUT.joinpath(fname).open('w') as outfile:
        outfile.write(doc)
