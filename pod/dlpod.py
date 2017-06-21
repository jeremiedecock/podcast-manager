#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
TODO...
"""

import argparse
import feedparser
import json
import os.path
import shutil
import urllib.request

DB_PATH = "podcasts.json"
OUTPUT_DIR_PATH = "./mp3"

def download_file(file_url, file_output_path, http_headers_dict={}):
    """
    TODO...
    """
    request = urllib.request.Request(file_url, data=None, headers= http_headers_dict)
    with urllib.request.urlopen(request) as response, open(file_output_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def download_podcast(url):
    """
    TODO...
    """
    feed = feedparser.parse(url)

    #print("Channel URL:", feed["url"])
    #print("Channel Title:", feed["channel"]["title"])
    #print("Channel Desc:", feed["channel"]["description"])

    channel_title = feed["channel"]["title"]

    for item in feed["items"]:
        #print(item.keys())

        pub_time = item["published_parsed"]
        pub_time_str = "{}-{:02d}-{:02d}_{:02d}h{:02d}".format(pub_time.tm_year, pub_time.tm_mon, pub_time.tm_mday, pub_time.tm_hour, pub_time.tm_min)

        item_title = item['title']

        for link in item["links"]:
            if link['type'] == 'audio/mpeg':
                item_url = link['href']

                file_name = item_url.split('/')[-1]
                file_name = file_name.split('%')[-1]

                file_name, file_extension = os.path.splitext(file_name)

                #file_name = channel_title + "_" + file_name + "_" + item_title + file_extension
                file_name = channel_title + "_" + pub_time_str + "_" + item_title + file_extension

                file_name = '_'.join(file_name.split())                                    # replace spaces with '_'
                file_name = ''.join(c for c in file_name if (c.isalnum() or c in ".-_"))   # remove special char in file_name
                file_name = '_'.join([c for c in file_name.split('_') if c != ''])         # replace multiples '_' with simple '_'
                file_name = '.'.join(file_name.split('_.'))
                file_name = file_name.lower()

                file_path = os.path.join(OUTPUT_DIR_PATH, file_name)

                # Download the files that haven't been downloaded yet
                if not os.path.exists(file_path):
                    print("Download", item_url, " -> ", file_path)
                    download_file(item_url, file_path)

    return feed

def main():
    """
    TODO...
    """
    parser = argparse.ArgumentParser(description='An argparse snippet.')

    parser.add_argument("url", nargs=1, metavar="URL",
                        help="URL of the RSS document to parse")

    args = parser.parse_args()
    rss_url = args.url[0]

    # Load the podcast db
    try:
        with open(DB_PATH, "r") as fd:
            feed_dict = json.load(fd)
    except FileNotFoundError:
        feed_dict = {}

    # Get last feeds
    last_feeds_dict = download_podcast(rss_url)

    # Update the podcast db
    feed_dict.update(last_feeds_dict)

    # Save the podcast db
    with open(DB_PATH, "w") as fd:
        json.dump(feed_dict, fd, sort_keys=True, indent=4)  # pretty print format

if __name__ == '__main__':
    main()

