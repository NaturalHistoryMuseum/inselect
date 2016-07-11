#!/usr/bin/env python3
from __future__ import unicode_literals

AUTHOR = 'Trustees of the Natural History Museum, London'
SITENAME = 'Inselect'

SITEURL = 'https://naturalhistorymuseum.github.io/inselect'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

CC_LICENSE = 'CC-BY'

# Blogroll
LINKS = (
    ('SYNTHESYS', 'http://www.synthesys.info/'),
)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/NaturalHistoryMuseum/inselect/'),
)

MENUITEMS = (
    ('Gallery', '{siteurl}/pages/gallery.html'.format(siteurl=SITEURL)),
    ('Install', '{siteurl}/pages/install.html'.format(siteurl=SITEURL)),
    ('Documentation', '{siteurl}/pages/documentation.html'.format(siteurl=SITEURL)),
    ('News', '{siteurl}/category/news.html'.format(siteurl=SITEURL)),
    ('Newsletter', '{siteurl}/pages/newsletter.html'.format(siteurl=SITEURL)),
    ('FAQs', '{siteurl}/pages/faqs.html'.format(siteurl=SITEURL)),
)

DEFAULT_PAGINATION = False

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

GITHUB_URL = "https://github.com/NaturalHistoryMuseum/inselect"

THEME = "../../pelican-themes/pelican-bootstrap3"
BOOTSTRAP_THEME = 'readable'

FAVICON = 'images/favicon.png'
SITELOGO = 'images/inselect128.png'
SITELOGO_SIZE = 32

PYGMENTS_STYLE = 'friendly'

SHOW_COPYRIGHT = False
CC_ATTR_MARKUP = True
