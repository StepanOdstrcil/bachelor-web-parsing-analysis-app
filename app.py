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


# MAIN STARTUP SCRIPT
if __name__ == "__main__":
    main()
