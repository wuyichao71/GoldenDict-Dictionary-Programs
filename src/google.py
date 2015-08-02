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

import os
import sys

import urllib
import urllib2

def usage():
    print "argv required."

def main(argv):
    if len(argv) <= 0:
        usage()
        sys.exit(1)

    header ={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2467.2 Safari/537.36"}
    page = urllib2.urlopen(urllib2.Request("http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=en&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk=522919|25625&q=" + urllib.quote_plus(argv[0]), None, header)).read()

    true = True
    false = False

    i = 0
    while i < len(page) - 2:
        if (page[i] == "," and page[i + 1] == ",") or \
            (page[i] == "[" and page[i + 1] == ",") or \
            (page[i] == "," and page[i + 1] == "]"):
            page = page[:i + 1] + "None" + page[i + 1:]
            i += 4

        i += 1

    exec("result = " + page)

    print "\033[31mResult:\033[32m"
    for obj in result[0]:
        if obj[0] != None:
            sys.stdout.write(obj[0])
    print "\033[0m"

    if result[1] != None:
        print "\033[31mTranslations for \033[1;34m%s\033[0;31m:" % argv[0]
        for obj in result[1]:
            print "\033[33m%s\033[32m" % obj[0]
            for detail in obj[1]:
                print "\t" + detail
    print "\033[0m"
    
if __name__ == "__main__":
    main(sys.argv[1:])
