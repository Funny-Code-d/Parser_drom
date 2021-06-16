import parser_class

parser = parser_class.Parser()

d = parser.get_info_fields("https://auto.drom.ru/all/", 'novosibirsk')
f = parser.get_info_page_field('https://moscow.drom.ru/tesla/model_3/42586753.html')
for item in d.keys():
	print(d[item])

print("Объявление")
for item in f.keys():
	print(f[item])