# Basic libraries

# App libraries
from GUI.App import App
# Third-party libraries


# MAIN CODE
def main():
    app = App()
    app.build()


# MAIN STARTUP SCRIPT
if __name__ == "__main__":
    main()
    # TEST_TEXT_1 = 'An back office handling all agregated data should be available for the customers of vehicle certificate service. These data must be available through a secured access.'
    # TEST_TEXT_2 = 'If you are a resident of the european economic area (eea) you have certain rights and protections under the gdpr regarding the processing of your personal data. '

    # nlp_s = NLPService()
    # print(nlp_s.get_word_movers(TEST_TEXT_1, TEST_TEXT_2))
    # nlp_s.show_word_movers_plot(TEST_TEXT_1, TEST_TEXT_2)
