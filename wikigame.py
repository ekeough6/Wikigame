import re  # regular expressions

import requests
from bs4 import BeautifulSoup


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node] = []

    def add_edge(self, parent, child):
        if parent not in self.graph:
            self.add_node(parent)
        if child not in self.graph[parent]:
            self.graph[parent].append(child)

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.graph:
            return None
        shortest = None
        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


connections = Graph()
base_url = "https://en.wikipedia.org"
start_url = "/wiki/Long_Island"
url_regex = re.compile('^/wiki/\w*')
url_regex_bad = re.compile("^/wiki/\w*:\w*")

limit = 10
urls = [start_url]
for count in range(3):
    print(count)
    new_urls = []
    for url in urls:
        count_limit = 0
        current_key = re.sub("/wiki/", "", url)
        r = requests.get(base_url + url)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.content, "lxml")
            for link in soup.select("#bodyContent a"):
                link_url = str(link.get("href"))
                if url_regex.match(link_url) and not url_regex_bad.match(link_url):
                    count_limit += 1
                    link_key = re.sub("/wiki/", "", link_url)
                    new_urls.append(link_url)
                    connections.add_edge(current_key, link_key)
                if count_limit >= limit:
                    break
            urls = new_urls
print(connections.graph)
print()
print(connections.find_shortest_path("Long_Island", "Germany"))
