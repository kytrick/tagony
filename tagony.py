
from collections import Counter
from HTMLParser import HTMLParser
import requests


# from markupsafe import escape
from cgi import escape  # https://wiki.python.org/moin/EscapingHtml


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self):
        """Initialize and reset this instance."""
        self.reset()
        self.TagCounter = Counter()
        self.augmented_html = ""

    def get_output(self):
        # this function wraps the augmented html
        return '<div class="highlight"><pre>' + self.augmented_html + '</pre></div>'

    def handle_starttag(self, tag, attrs):
        self.TagCounter[tag] += 1

        # (re)build the string of attrs that would appear inside a start tag.
        attr_string = ''
        for attr in attrs:
            # conditional protects against trying to cast None as unicode
            if attr[1] is None:
                attr = (attr[0], '')
            attr_string += escape(' ' + attr[0] + '="' + attr[1] + '"')

        # generate start tag string that includes attrs.
        tempstring = '<span class="my_' + tag + '">&lt;' + tag + attr_string + '&gt;</span>'

        self.augmented_html += tempstring

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        # this is commented out so that I don't count twice!
        # self.TagCounter[tag] += 1
        tempstring = '<span class="my_' + tag + '">&lt;/' + tag + '&gt;</span>'
        self.augmented_html += tempstring

    def handle_startendtag(self, tag, attrs):
        self.TagCounter[tag] += 1

        # (re)build the string of attrs that would appear inside a start tag.
        attr_string = ''
        for attr in attrs:
            if attr[1] is None:
                attr = (attr[0], '')
            attr_string += escape(' ' + attr[0] + '="' + attr[1] + '"')

        # generate start tag string that includes attrs.
        tempstring = '<span class="my_' + tag + '">&lt;' + tag + attr_string + ' /&gt;</span>'

        self.augmented_html += tempstring

    def handle_entityref(self, name):

        tempstring = '&amp;' + name + ';'
        self.augmented_html += tempstring

    def handle_charref(self, name):

        tempstring = '&amp;#' + name + ';'
        self.augmented_html += tempstring

    def handle_comment(self, data):
        # parser doesn't work perfectly with <!------>stuff-->
        tempstring = '<span class="my_comment">&lt;!--' + escape(data) + '--&gt;</span>'
        self.augmented_html += tempstring

    def handle_decl(self, data):
        tag = "decl"
        self.TagCounter[tag] += 1
        tempstring = '<span class="my_decl">' + '&lt;!' + escape(data) + '&gt;</span>'
        self.augmented_html += tempstring

    def handle_data(self, data):
        # need to escape
        tempstring = escape(data)
        self.augmented_html += tempstring

    def handle_pi(self, data):
        self.augmented_html += escape(data)

    def unknown_decl(self, decl):
        tag = "decl"
        self.TagCounter[tag] += 1
        # need to escape
        self.augmented_html += escape(decl)


def get_parsed_data(input_url):
    parser = MyHTMLParser()
    data = fetch_data(input_url)
    parser.feed(data)
    return parser


class FetchDataException(Exception):
    def __init__(self, e):
        # send the error object up the stack
        self.e = e

    def __str__(self):
        return repr(self.e)


def fetch_data(input_url):
    clean_url = clean_my_url(input_url)
    try:
        data = requests.get(clean_url).text
    except Exception as e:
        raise FetchDataException(e)
    return data


def clean_my_url(input_url):
    ''' this function does some sanity checking on the input url before giving
        it to get_parsed_data
    '''

    # did the user forget the http:// ?
    if input_url.find('://') < 0:
        input_url = 'http://' + input_url

    return input_url
