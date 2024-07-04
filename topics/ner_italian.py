import stanza

stanza.download('it')
nlp = stanza.Pipeline(lang="it")

# with open('test.txt', 'r') as file:
#     text = file.read()
text = "Il presidente della Repubblica italiana, Sergio Mattarella, ha nominato Mario Draghi come nuovo presidente del Consiglio dei ministri."
doc = nlp(text)
dic = {}
for ner in doc.ents:
    dic[ner.type].append(ner.text) if ner.type in dic else dic.update({ner.type: [ner.text]})
print(dic)
