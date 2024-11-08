import argparse
import os
import parse_webpage
parse = argparse.ArgumentParser(
    prog="dumper",
    description="Program dumper website for url",
    # help="url: http or https link\n-d or --dir: path to dir default=./webpage/"
)
parse.add_argument("-d", "--dir", default="webpage/")
parse.add_argument("url")
if __name__ == "__main__":
    args = parse.parse_args()
    os.mkdir(args.dir)
    page = parse_webpage.WebPage(args.url)
    page.preparing_web_page_layout()
    page.dump(args.dir)
    