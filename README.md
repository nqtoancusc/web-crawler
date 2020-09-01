# web-crawler

An open source library for extracting the data you need from websites, xml source.

- To use util library:

from util import ds
from util import readurl

url = "..."
s = ds(readurl(url))

- To use dbclass:

import dbclass

db = dbclass.DBAdapter()
db.connect(...)
db.execute(...)

