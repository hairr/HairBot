import mwhair, datetime, re
def getpages():
	year, currentyear, monthname, returnlist = 2012, datetime.datetime.now().year, lambda month_num:datetime.date(1900,month_num,1).strftime('%B'), []
	while 1:
		for monthnumber in range(1,12):
			pages = mwhair.category('Category:Dead-end pages from %s %s' % (monthname(monthnumber),year),limit='max')
			if pages != []:
				for page in pages: returnlist.append(page)
		year += 1
		if currentyear < year: return returnlist
def remove(title):
		try: links = len(pagelinks(title))
		except: links = 0
		if links > 0:
			text = mwhair.edit(title)
			print title
			newtext = re.sub(r'({{(D|d)ead end(\|(.*))?}}(\n)?|dead end ?=(\n)?|\| ?(d|D)ead end ?= ?([a-zA-Z0-9]+) ([a-zA-Z0-9]+))','',text)
			newtext = re.sub(r'{{Multiple issues\|\s*{{(?P<template>[^\|]+)\|date=(?P<date>[^}]+)}}\s*}}',r'{{\g<template>\|date=\g<date>}}',newtext)
			newtext = re.sub(r'{{Multiple issues\|\s*(?P<template>[^=]+) ?= ?(?P<date>[^\|}]+)}}',r'{{\g<template>|date=\g<date>}}',newtext)
			save(title,newtext)
def save(title,text):
	mwhair.save(title,text=text,summary='Removing dead end tag as not a valid dead end page',minor=True)
def pagelinks(title):
	return mwhair.links(title,limit='max',namespace='0')
def main():
	pages = getpages()
	for page in pages:
		remove(page)
if __name__ == '__main__':
	mwhair.site('http://en.wikipedia.org/w/api.php')
	mwhair.login('HairBot','password')
	main()