import os
import re
import sys
import getpass
from string import Template

import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def show_help():
    print "usage: python build.py <file.html>"

def replace_code(content):
    def highlight_code(match):
        lexer_name = match.group(1)
        code = match.group(2)
        lexer = get_lexer_by_name(lexer_name, stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="source")
        return "<div class='code-block'>%s</div>" % highlight(code, lexer, formatter)
    return re.sub(r"```(\w+)\s*\n+(.*?)```", highlight_code, content, flags=re.DOTALL|re.UNICODE)

def build_slide(content):
    content = replace_code(content)
    content = markdown.markdown(content)
    # content = re.sub("^\s+", "", content, flags=re.MULTILINE);
    return "<section>\n%s\n</section>" % content

def handle_slide_sub(match):
    return build_slide(match.groups()[0])

def build_slides(source_html):
    content = re.sub(r"<slide>(.*?)</slide>", handle_slide_sub, source_html, flags=re.DOTALL|re.UNICODE)
    return content

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        show_help()
        exit()

    script_path = os.path.realpath(__file__)
    script_home = os.path.dirname(script_path)

    f = open(file)
    slides_content = build_slides(f.read())

    template = Template(open(os.path.join(script_home, 'template.html')).read())
    print template.substitute({"content": slides_content})
