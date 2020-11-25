def main():
    from scrapy import cmdline
    cmdline.execute("scrapy crawl vnexpress -a limit=20".split())


if __name__ == '__main__':
    main()
