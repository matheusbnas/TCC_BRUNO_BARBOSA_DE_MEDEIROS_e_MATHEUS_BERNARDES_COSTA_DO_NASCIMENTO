# TCC - BRUNO MEDEIROS & MATHEUS BERNARDES

import requests


class Scrapping:
    def __init__(self, endpoint_type, font):
        self.endpoint_type = endpoint_type
        self.font = font

    @staticmethod
    def get_endpoint(ep):

        # Dicionário com os Endpoints do WordPress
        endpoints = {
            'Posts': '/wp-json/wp/v2/posts',
            'Post Revisions': '/wp-json/wp/v2/posts/<id>/revisions',
            'Categories': '/wp-json/wp/v2/categories',
            'Tags': '/wp-json/wp/v2/tags',
            'Pages': '/wp-json/wp/v2/pages',
            'Page Revisions': '/wp-json/wp/v2/pages/<id>/revisions',
            'Comments': '/wp-json/wp/v2/comments',
            'Taxonomies': '/wp-json/wp/v2/taxonomies',
            'Media': '/wp-json/wp/v2/media',
            'Users': '/wp-json/wp/v2/users',
            'Post Types': '/wp-json/wp/v2/types',
            'Post Statuses': '/wp-json/wp/v2/statuses',
            'Settings': '/wp-json/wp/v2/settings',
            'Themes': '/wp-json/wp/v2/themes',
            'Search': '/wp-json/wp/v2/search',
            'Block Types': '/wp-json/wp/v2/block-types',
            'Blocks': '/wp-json/wp/v2/blocks',
            'Block Revisions': '/wp-json/wp/v2/blocks/<id>/autosaves/',
            'Block Renderer': '/wp-json/wp/v2/block-renderer',
            'Block Directory Items': '/wp-json/wp/v2/block-directory/search',
            'Plugins': '/wp-json/wp/v2/plugins'
        }

        return endpoints[ep]

    @staticmethod
    def write_file(opt):

        with open(opt[0], "a", encoding="utf-8") as file:
            file.write('\n')
            file.write(str(f"**********{opt[2]} - Page:{opt[3]}**********"))
            file.write('\n\n')
            file.write(str(opt[1]))
            file.write('\n')

        return None

    @staticmethod
    def file_name(endpoint, site_name):
        return f"_{endpoint}-{site_name}.txt"

    def do_requests(self, site, complement, page):
        endpoint = self.get_endpoint(self.endpoint_type)
        endereco = site.wp_url + endpoint + complement + page
        response = requests.get(endereco).content
        self.write_file([self.file_name(self.endpoint_type, site.name), response, site.name, page])

        return None


class Site:
    def __init__(self, name, wp_url, pages, per_page):
        self.name = name
        self.wp_url = wp_url
        self.pages = pages
        self.per_page = per_page


if __name__ == '__main__':

    import time
    start = time.time()

    sites = [Site('Hospício Nerd', 'https://www.hospicionerd.com.br', 231, '14'),
             Site('World Education Blog', 'https://world-education-blog.org', 93, '12'),
             Site('Cristine Lowry', 'https://christinelowry.wordpress.com', 6, '10')
             ]

    for i in range(len(sites)):
        posts = Scrapping('Posts', sites[i])
        for j in range(1, sites[i].pages+1):
            posts.do_requests(sites[i], f'?per_page={sites[i].per_page}&page=', str(j))

    for i in range(len(sites)):
        comments = Scrapping('Comments', sites[i])
        for j in range(1, sites[i].pages+1):
            comments.do_requests(sites[i], f'?per_page={sites[i].per_page}&page=', str(j))

    end = time.time()
    print("Runtime: {:.2f} seconds.".format(end - start))
