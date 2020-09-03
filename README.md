# web-crawler

An open source library for extracting the data you need from websites, xml sources.
- util.py has all functions that you need to nagivate through an html or an xml structure and retrieve data inside it.
- dbclass is an adapter class for MySQL Database which has methods to perform SQL commands.

Example:

from util import ds

from util import readurl

import dbclass.py

url = "..."

s = ds(readurl(url))

db = dbclass.DBAdapter()

db.connect(...)

db.execute(...)

