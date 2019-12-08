from models import Target, Method, Tag, Category


def save_targets():
	targets = Target.query.all()
	with open('prebuilt/targets.py', 'w') as file:
		file.write('TARGETS = {\n')
		for target in targets:
			file.write("\t'{}': {},\n".format(sanitise(target.name), [sub.string for sub in target.substrings]))
		file.write('}\n')


def save_methods():
	methods = Method.query.all()
	with open('prebuilt/methods.py', 'w') as file:
		file.write('METHODS = {\n')
		for method in methods:
			file.write("\t'{}': {},\n".format(sanitise(method.name),
												[sanitise(sub.string) for sub in method.substrings]))
		file.write('}\n')


def save_tags():
	tags = Tag.query.all()
	with open('prebuilt/tags.py', 'w') as file:
		file.write('TAGS = {\n')
		for tag in tags:
			file.write("\t'{}': ({}, '{}'),\n".format(
				sanitise(tag.name), [sanitise(target.name) for target in tag.targets],
				sanitise(tag.category.name) if tag.category is not None else None))
		file.write('}\n')


def save_categories():
	categories = Category.query.all()
	with open('prebuilt/categories.py', 'w') as file:
		file.write('CATEGORIES = [\n')
		for category in categories:
			file.write("\t'{}',\n".format(sanitise(category.name)))
		file.write(']\n')


def sanitise(string):
	return string.replace("'", r"\'")


def save_all():
	save_targets()
	save_methods()
	save_tags()
	save_categories()
