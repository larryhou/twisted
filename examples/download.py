#!/usr/bin/env python3

from pyquery import PyQuery
import requests, os
import os.path as p

def resolve_url(base_url:str, path:str):
    components = path.split('/')
    if base_url[-1] == '/': base_url = base_url[:-1]
    while components[0] == '..':
        base_url = os.path.dirname(base_url)
        del components[0]
    return base_url + '/' + '/'.join(components)

def download_examples(url:str, topic:str):
    jq = PyQuery(url)
    if not p.exists(topic):
        os.makedirs(topic)
    for item in jq.find('a.reference.download'):
        download_url = resolve_url(base_url=url, path=item.get('href'))
        file_name = p.basename(download_url)
        response = requests.get(download_url)
        with open('{}/{}'.format(topic, file_name), 'w+') as fp:
            fp.write(response.text)
            print('+ {} => {}'.format(download_url, fp.name))

if __name__ == '__main__':
    import argparse, sys
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--url', '-u', required=True, nargs='+')
    arguments.add_argument('--topic', '-t', required=True)
    options = arguments.parse_args(sys.argv[1:])
    os.chdir(p.dirname(p.abspath(__file__)))
    for u in options.url:
        download_examples(u, topic=options.topic)



