

def morph(text):
    from natasha import (
        Segmenter,

        NewsEmbedding,
        NewsMorphTagger,
        NewsSyntaxParser,
        NewsNERTagger,
        NamesExtractor,
        DatesExtractor,
        MoneyExtractor,
        MorphVocab,
        Doc
    )

    segmenter = Segmenter()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)

    # text = 'Президент России Владимир Путин 4 мая поприветствовал гостей и участников Кубка президента Российской Федерации по самбо, отметив, что данный вид спорта воспитывает в человеке высокие морально-волевые качества, соответствующая телеграмма опубликована на сайте Кремля. '

    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)

    sent = doc.sents[0]
    # sent.morph.print()
    ner_tagger = NewsNERTagger(emb)
    doc.tag_ner(ner_tagger)
    # doc.ner.print()
    extr = DatesExtractor(MorphVocab())
    matches = extr(text)
    # print(set(matches))

    dict_ner = dict()
    for span in list(doc.ner)[1]:
        dict_ner[text[span.start:span.stop]] = span.type
    # print(dict_ner)

    list_data = list()
    for m in matches:
        list_data.append(m.fact)




    return dict_ner, list_data





# print(morph("Новости Израиля за 26 мая"))