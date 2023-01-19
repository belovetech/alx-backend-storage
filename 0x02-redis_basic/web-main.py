#!/usr/bin/env python3
"""Web main"""
get_page = __import__('web').get_page

def main():
    url = "http://slowwly.robertomurray.co.uk"
    # url = "https://github.com/belovetech"

    res = get_page(url)
    print(res)
    
if __name__ == '__main__':
    main()