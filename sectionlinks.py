"""
Copyright (C) 2012 Hair

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
import mwhair
import mwparserfromhell as mw
import re
import sqlite3 as lite

def get_pages():
	return mwhair.allpages(limit='max',namespace=0)

def find_links(text):
	new_text = mw.parse(text)
	links = new_text.filter_links()
	return links

def page_name(link):
	pattern = re.compile(r'\[\[(.*?)(#.*?)?(\|.*?)?\]\]')
	page_link = pattern.findall(link)
	return page_link[0][0]

def section_link(link):
	pattern = re.compile(r'\[\[.*#(.*?)(\|.*?)?\]\]')
	string = pattern.findall(link.encode('ascii','ignore'))
	if string != []:
		return string[0][0]

def matched(section,headers):
	count, total = 0, len(headers)
	for header in headers:
		if re.search(section, header):
			return True
		else:
			count += 1
			if count == total:
				return False

def replace_link(section, link, headers):
	for header in headers:
		if re.search(section, header, flags=re.IGNORECASE):
			return re.sub(section, header, link.encode('ascii','ignore'))
		else:
			return re.sub('#' + section,'',link.encode('ascii','ignore'))

def filter_headers(title):
	pattern = re.compile(r'\[\[(.*?)(#.*?)?(\|.*?)?\]\]')
	title2 = pattern.findall('%s' % title)[0][0]
	text, sections = get_contents(title2), []
	pattern = re.compile(r'<.*?[^>]+?id="([^"]+)".*?<\/.*?>')
	header_ids = pattern.findall(text)
	for header_id in header_ids:
		sections.append(header_id)
	for line in text.split('\n'):
		if line.startswith('==') and not line.startswith('===='):
			sections.append(re.sub(r'==(=)? ?(?P<header>.*?) ?==(=)?',r'\g<header>',line))
	return sections

def get_contents(title):
	con, revid = lite.connect('pages.db'), mwhair.revnumber(title)
	with con:
		cur = con.cursor()
		cur.execute("SELECT Contents FROM Pages WHERE Id = (?)",(revid,))
		try:
			return cur.fetchall()[0][0]
		except:
			text = mwhair.edit(title)
			cur.execute('INSERT INTO Pages VALUES(?,?)',(revid,text,))
			return text

def allow_bots(text, user):
    return not re.search(r'\{\{(nobots|bots\|(allow=none|deny=.*?' + user + r'.*?|optout=all|deny=all))\}\}', text, flags=re.IGNORECASE)

def save(title, text):
	mwhair.save(title,text=text,summary='Removing incorrect section link(s)',minor=True)

def main():
	pages = get_pages()
	for page in pages:
		text = get_contents(page)
		links = find_links(text)
		amount, count = len(links), 0
		for link in links:
			count += 1
			if '#' in link:
				section, headers = section_link(link), filter_headers(link)
				if not matched(section, headers):
					try:
						new_text = new_text.replace(link.encode('ascii','ignore'), replace_link(section,link,headers))
					except:
						new_text = text.replace(link.encode('ascii','ignore'), replace_link(section,link,headers))
			if count == amount and allow_bots(text, 'HairBot'):
				try:
					save(page,new_text)
					del new_text
				except:
					pass
if __name__ == '__main__':
	mwhair.site('http://en.wikipedia.org/w/api.php')
	mwhair.login('HairBot','password')
	main()