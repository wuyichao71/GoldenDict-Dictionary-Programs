#! /usr/bin/python
# -*-  coding=utf8  -*-

#    Copyright (C) 2015 Guangmu Zhu <guangmuzhu@gmail.com>
#
#    This file is part of GoldenDict-Dictionary-Programs.
#
#    GoldenDict-Dictionary-Programs is free software: you can redistribute it
#    and/or modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation, either version 3 of the License,
#    or (at your option) any later version.
#
#    GoldenDict-Dictionary-Programs is distributed in the hope that
#    it will be useful, but WITHOUT ANY WARRANTY; without even
#    the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyChat.  If not, see <http://www.gnu.org/licenses/>.

import re
import urllib
import urllib2
import sys

def get_elements_by_path(xml, elem):
    if type(xml) == type(''):
        xml = [xml]
    if type(elem) == type(''):
        elem = elem.split('/')
    if (len(xml) == 0):
        return []
    elif (len(elem) == 0):
        return xml
    elif (len(elem) == 1):
        result = []
        for item in xml:
            result += get_elements(item, elem[0])
        return result
    else:
        subitems = []
        for item in xml:
            subitems += get_elements(item, elem[0])
        return get_elements_by_path(subitems, elem[1:])

def get_text(xml):
    textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL)
    match = re.search(textre, xml)
    if not match:
        return xml
    return match.group(1)

def get_elements(xml, elem):
    p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL)
    it = p.finditer(xml)
    result = []
    for m in it:
        result.append(m.group(1))
    return result

def crawl_xml(queryword):
    return urllib2.urlopen("http://dict.yodao.com/search?keyfrom=dict.python&q="
    + urllib.quote_plus(queryword) + "&xmlDetail=true&doctype=xml").read()

def print_translations(xml):
    #print xml
    original_query = get_elements(xml, "original-query")
    queryword = get_text(original_query[0])
    phonetic_symbol = get_elements(xml, "phonetic-symbol")
    if len(phonetic_symbol) > 0:
        print "[" + phonetic_symbol[0] + "]"
    custom_translations = get_elements(xml, "custom-translation")
    translated = False

    pattern = re.compile(r'([A-Za-z]+\.)')

    print "<html>\n<body>\n<head><meta http-equiv=\"content-type\" content=\"text/htmlcharset=utf-8\"></head>"
    
    for cus in custom_translations:
        source = get_elements_by_path(cus, "source/name")
        print "<p style=\"color:green\">"
        print "Translations from " + source[0]
        print "</p>"
        contents = get_elements_by_path(cus, "translation/content")
        for content in contents:
            print "● "
            print pattern.sub("<font style=\"color:blue\">\\1</font>", get_text(content)) + "；"
            print "<br>"
        translated = True

    yodao_web_dict = get_elements(xml, "yodao-web-dict")
    printed = False
    for web_dict in yodao_web_dict:
        webtrans = get_elements(web_dict, "web-translation")
        for webtran in webtrans:
            if not printed:
                print "<p style=\"color:green\">"
                print "Translations from yodao-web:"
                print "</p>"
                printed = True
            keys = get_elements(webtran, "key")
            key = keys[0].strip()
            print "<font style=\"color:blue\">" +get_text(key) + ":" + "</font>"
            trans = get_elements(webtran, "trans")
            for tran in trans:
                values = get_elements(tran, "value")
                value = values[0].strip()
                sys.stdout.write(get_text(value) + "；")
            print "<br>"
    print "</body>\n</html>"
    
def usage():
    print "usage: dict.py word_to_translate"

def main(argv):
    if len(argv) <= 0:
        usage()
        sys.exit(1)
    xml = crawl_xml(" ".join(argv))
    print_translations(xml)

if __name__ == "__main__":
    main(sys.argv[1:])
