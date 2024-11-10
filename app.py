#!./venv/bin/python
import argparse
from os import mkdir, path, system 
from parse_webpage import DumpHtmlPage
parse = argparse.ArgumentParser(
    prog="dumper",
    description="Program dumper website for url",
    # help="url: http or https link\n-d or --dir: path to dir default=./webpage/"
)

parse.add_argument("-d", "--dir", default="webpage/")
parse.add_argument("url")

if __name__ == "__main__":
    args = parse.parse_args()
    if path.exists(args.dir):
        print(f"Wipe is directory: {args.dir}   y/n: ")
        select = input()
        if select.lower() == "y":
            if args.dir in ".":
                print("You dont wipe main directory")
            else:
                system(f"rm -r {args.dir}")
    mkdir(args.dir)
    page = DumpHtmlPage(args.url)
    page.preparing_web_page_layout()
    
    page.dump(args.dir)
# test
# page = DumpHtmlPage("https://pythonz.net/references/named/raise/")
# page.preparing_web_page_layout()
# mkdir("./raise/")
# page.dump("raise")