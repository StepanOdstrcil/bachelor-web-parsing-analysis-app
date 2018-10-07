# Basic libraries

# App libraries
from WebParsing.web_parser import WebParser
# Third-party libraries


# MAIN CODE
def main():
    wb = WebParser()
    wb.load_page(r"https://cs.wikipedia.org/wiki/Wiki")
    print(wb.get_items_by_tag("p"))
    print(wb.get_items_by_class("tocnumber"))
    print(wb.get_all_links())
    print(wb.get_all_emails())
    print(wb.get_all_following_links(2))


# MAIN STARTUP SCRIPT
if __name__ == "__main__":
    main()
