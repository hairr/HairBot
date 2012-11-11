import mwhair
import mwparserfromhell as mw
import time
import datetime
import re
def getpages():
	year, currentyear, monthname, returnlist = 2012, datetime.datetime.now().year, lambda month_num:datetime.date(1900,month_num,1).strftime('%B'), []
	while 1:
		for monthnumber in range(1,12):
			pages = mwhair.category('Category:Dead-end pages from %s %s' % (monthname(monthnumber),year),limit='max')
			if pages != []:
				for page in pages: returnlist.append(page)
		year += 1
		if currentyear < year: return returnlist
def allow_bots(text, user): # [[Template:Bots#Python]]
    return not re.search(r'\{\{(nobots|bots\|(allow=none|deny=.*?' + user + r'.*?|optout=all|deny=all))\}\}', text, flags=re.IGNORECASE)
def remove(title):
		text = mw.parse(mwhair.edit(title))
		oldtext = text
		try: links = len(pagelinks(title))
		except: links = 0
		if links > 1:
			if allow_bots(mwhair.edit(title),'HairBot'):
				for template in text.filter_templates():
					if template.name is 'Multiple issues' or 'multiple issues' or 'Article issues' or 'Articleissues' or 'Issues' or 'MI' or 'mi' or 'Mi' or 'Multiple' or 'Multiple Issues' or 'Multipleissues':
						if template.has_param('dead end'):
								template.remove('dead end')
								if links <= 4:
									text = '{{subst:dated|Underlinked}}\n' + text
						else:
							try:
								for itemplate in template.get(1).value.filter_templates():
									if itemplate.name == 'Dead end' or 'dead end' or 'DEP' or 'dep' or 'DEp' or 'DeP' or 'Dead end page' or 'dead end page' or 'dead-end' or 'Dead-end' or 'Dead-End' or 'Deadend':
										text.remove(itemplate,'')
										if links <= 4:
											text = '{{subst:dated|Underlinked}}\n' + text
							except:
								pass
					elif template.name is 'Dead end' or 'dead end' or 'DEP' or 'dep' or 'DEp' or 'DeP' or 'Dead end page' or 'dead end page' or 'dead-end' or 'deadend' or 'Dead-end' or 'Deadend':
						text.replace(template,'')
				raw_input('Press enter')
				save(title,text)
def save(title,text):
	mwhair.save(title,text=text,summary='Removing dead end tag as not a valid dead end page',minor=True)
def pagelinks(title):
	return mwhair.links(title,namespace='0')
def main():
	pages = getpages()
	for page in pages:
		remove(page)
		time.sleep(1)
if __name__ == '__main__':
	mwhair.site('http://en.wikipedia.org/w/api.php')
	mwhair.login('HairBot','password')
	main()