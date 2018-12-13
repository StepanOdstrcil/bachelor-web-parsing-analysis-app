# Basic libraries

# App libraries
from WebParsing.web_parser import WebParser
from NLP.nlp_service import NLPService
# Third-party libraries


# MAIN CODE
def main():
    # PARSING

    # wb = WebParser()
    # wb.load_page(r"https://cs.wikipedia.org/wiki/Wiki")
    # print(wb.get_items_by_tag("p"))
    # print(wb.get_items_by_class("tocnumber"))
    # print(wb.get_all_links())
    # print(wb.get_all_emails())
    # print(wb.get_all_following_links(2))

    # NLP

    wb = WebParser()
    wb.load_page(r"https://en.wikipedia.org/wiki/Wiki")
    text = wb.get_items_by_tag("p")[14]

    print(text)
    print("----")

    nlp_service = NLPService(text)

    named_entities = nlp_service.get_named_entity_recognition()
    print("\nNamed entities:")
    print(named_entities)

    gensim = nlp_service.get_topic_modeling_and_summarization()
    print("\nTopic modeling:")
    print(gensim.get_topics())
    print("\nText summarization:")
    print(gensim.get_summarization())


# MAIN STARTUP SCRIPT
if __name__ == "__main__":
    main()
