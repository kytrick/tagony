from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
from collections import Counter
from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser
import json
import requests


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
        # print "Encountered a start tag:", tag
        self.TagCounter[tag] += 1

        # (re)build the string of attrs that would appear inside a start tag.
        attr_string = ''
        for attr in attrs:
            attr_string += ' ' + attr[0] + '="' + attr[1] + '"'

           # attr_string += ' %s="%s"' % (attr[0], attr[1])

        # generate start tag string that includes attrs.
        tempstring = '<span class="my_' + tag + '">&lt;' + tag + attr_string + '&gt;</span>'

        # print tempstring
        self.augmented_html += tempstring

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        # this is commented out so that I don't count twice!
        # self.TagCounter[tag] += 1
        tempstring = '<span class="my_' + tag + '">&lt;/' + tag + '&gt;</span>'
        # print tempstring
        self.augmented_html += tempstring

    def handle_startendtag(self, tag, attrs):
        # print "Encountered a startend tag :", tag
        self.TagCounter[tag] += 1

        # (re)build the string of attrs that would appear inside a start tag.
        attr_string = ''
        for attr in attrs:
            attr_string = attr_string + ' ' + attr[0] + '=' + '"' + attr[1] + '"'

        # generate start tag string that includes attrs.
        tempstring = '<span class="my_' + tag + '">&lt;' + tag + attr_string + ' /&gt;</span>'
        # print tempstring
        self.augmented_html += tempstring

    def handle_entityref(self, name):

        tempstring = '&amp;' + name + ';'
        self.augmented_html += tempstring

    def handle_charref(self, name):

        tempstring = '&amp;#' + name + ';'
        self.augmented_html += tempstring

    def handle_comment(self, data):
        # parser doesn't work perfectly with <!------>stuff-->
        # print "Comment  :", data
        tempstring = '<span class="my_comment">&lt;!--' + data + '--&gt;</span>'
        # print tempstring
        self.augmented_html += tempstring

    def handle_decl(self, data):
        # print "Decl     :", data
        tempstring = '<span class="my_decl">' + '&lt;!' + data + '&gt;</span>'
        # print tempstring
        self.augmented_html += tempstring

    def handle_data(self, data):
        # print "Encountered some data  :", data
        tempstring = data
        self.augmented_html += tempstring

    def handle_pi(self, data):
        self.augmented_html += data

    def unknown_decl(self, decl):
        self.augmented_html += decl

p = '<html><head><title>Test</title></head><body><h1><poop><img src="blah.jpg" />Parse me!</poop><p>Kayla Paragraph</p></h1></body></html>'
p1 = '<!DOCTYPE html>&gt;&gt;&gt;&#38;<html><!-- I am a comment --><head><title>Test</title></head><body><h1><img src="blah.jpg" />Parse me!</h1></body></html>'
p2 = requests.get('http://pygments.org/docs/quickstart/').text
p3 = '<html><p>beep</p></html>'
p4 = requests.get('http://dev.w3.org/html5/html-author/charref').text

# instantiate the parser and feed it some HTML
parser = MyHTMLParser()
parser.feed(p)
print parser.get_output()

print "======================="

def colorized_html_generator(urltext):
    """
    This is pygments. Using for comparison with my augmented html generator
    """
    return highlight(urltext, HtmlLexer(), HtmlFormatter())

print colorized_html_generator(p)