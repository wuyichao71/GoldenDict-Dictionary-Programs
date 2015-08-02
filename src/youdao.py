#! /usr/bin/python
# -*-  coding=utf8  -*-

import re;
import urllib;
import urllib2;
import sys;
def debug():
    xml = open("word.xml").read();
    print get_text(xml);
    print get_elements_by_path(xml, "custom-translation/content");
    #print_translations(xml, False, False);
def get_elements_by_path(xml, elem):
    if type(xml) == type(''):
        xml = [xml];
    if type(elem) == type(''):
        elem = elem.split('/');
    if (len(xml) == 0):
        return [];
    elif (len(elem) == 0):
        return xml;
    elif (len(elem) == 1):
        result = [];
        for item in xml:
            result += get_elements(item, elem[0]);
        return result;
    else:
        subitems = [];
        for item in xml:
            subitems += get_elements(item, elem[0]);
        return get_elements_by_path(subitems, elem[1:]);
textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL);
def get_text(xml):
    match = re.search(textre, xml);
    if not match:
        return xml;
    return match.group(1);
def get_elements(xml, elem):
    p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL);
    it = p.finditer(xml);
    result = [];
    for m in it:
        result.append(m.group(1));
    return result;
GREEN = "\033[32m";
DEFAULT = "\033[0;49m";
BOLD = "\033[1m";
UNDERLINE = "\033[4m";
NORMAL = "\033[m";
RED = "\033[31m"
def crawl_xml(queryword):
    return urllib2.urlopen("http://dict.yodao.com/search?keyfrom=dict.python&q="
        + urllib.quote_plus(queryword) + "&xmlDetail=true&doctype=xml").read();
def print_translations(xml, with_color, detailed):
        #print xml;
    original_query = get_elements(xml, "original-query");
    queryword = get_text(original_query[0]);
    custom_translations = get_elements(xml, "custom-translation");
    print BOLD + UNDERLINE + queryword + NORMAL;
    phonetic_symbol = get_elements(xml, "phonetic-symbol");
    if len(phonetic_symbol) > 0:
        print GREEN + "[" + phonetic_symbol[0] + "]" + DEFAULT;
    translated = False;
    
    for cus in custom_translations:
        source = get_elements_by_path(cus, "source/name");
        
        print RED + "Translations from " + source[0] + DEFAULT;
        contents = get_elements_by_path(cus, "translation/content");
        if with_color:
            for content in contents:
                print GREEN + get_text(content) + DEFAULT;
        else:
            for content in contents:
                print get_text(content);
        translated = True;

    yodao_web_dict = get_elements(xml, "yodao-web-dict");
    printed = False;
    for web_dict in yodao_web_dict:
        webtrans = get_elements(web_dict, "web-translation");
        for webtran in webtrans:
            if not printed:
                print RED + "Translations from yodao-web:" + DEFAULT;
                printed = True;
                keys = get_elements(webtran, "key");
            key = keys[0].strip();
            if with_color:
                print BOLD +  get_text(key) + ":\t" + DEFAULT;
            else:
                print get_text(key + ":\t");
            trans = get_elements(webtran, "trans")
            for tran in trans:
                values = get_elements(tran, "value");
                value = values[0].strip();
                if with_color:
                    print GREEN + get_text(value) + "; " + NORMAL;
                else:
                    print get_text(value) + "; ";
    
def usage():
    print "usage: dict.py word_to_translate";
def main(argv):
    if len(argv) <= 0:
        usage();
        #debug();
        sys.exit(1);
    xml = crawl_xml(" ".join(argv));
    print_translations(xml, True, False);

if __name__ == "__main__":
    main(sys.argv[1:]);
