import io
import os
import re
import shutil
import urllib.parse

import markdown

tree = []
cap_list = sorted(
    map(
        lambda x: x[9:],
        filter(
            os.path.isdir,
            map(
                lambda x: "Markdown/" + x, os.listdir("Markdown")
            )
        )
    ),
    key=lambda x: int(
        x.split('、')[0].translate(
            str.maketrans("一二三四五六七八九", "123456789")
        )
    )
)
for cap in cap_list:
    cla_ref = []
    tree.append((cap, cla_ref))
    cla_list = sorted(
        map(
            lambda x: x.rsplit("/")[-1][:-3],
            filter(
                lambda x: os.path.isfile(x) and not x.endswith('章首.md'),
                map(
                    lambda x: f"Markdown/{cap}/" + x,
                    os.listdir("Markdown/" + cap)
                )
            )
        ),
        key=lambda x: int(x.split(".")[0])
    )
    [cla_ref.append(cla) for cla in cla_list]

print(tree)

for path, dirs, files in os.walk("Markdown/"):
    path = path.replace('\\', '/')
    print("walk into", path)
    for folder in dirs:
        print("query if", folder, "exists")
        if not os.path.exists(os.path.join(path.replace("Markdown", "HTML"), folder)):
            print("create folder", folder)
            os.mkdir(os.path.join(path.replace("Markdown", "HTML"), folder))
    for file in files:
        print("work on", file)
        if file.endswith('.md'):
            print("convert", file, "to HTML")
            path_to_root = "../" * re.subn(r"[\\/]", "", path if path.endswith('/') else path + "/")[1]
            if file not in ('首页.md', '章首.md'):
                for i, (cap, clas) in enumerate(tree):
                    if file[:-3] in clas:
                        j = clas.index(file[:-3])
                        break
                title = file[:-3]
                link_html = f'''
            <nav>
                <a href="{
                '#' if i == 0 else f'../{urllib.parse.quote(tree[i - 1][0])}/%E7%AB%A0%E9%A6%96.html'
                }" title="{'' if i == 0 else tree[i - 1][0]}" {'disabled' if i == 0 else ''}>上一章</a> 
                <a href="%E7%AB%A0%E9%A6%96.html" title="{tree[i][0]}">转至章首</a>
                <a href="{
                '#' if i == j == 0 else (
                    f"{urllib.parse.quote(tree[i][1][j - 1])}.html" if j != 0 else
                    (
                            f"../{urllib.parse.quote(tree[i - 1][0])}/"
                            + f"{urllib.parse.quote(tree[i - 1][1][-1])}.html"
                    )
                )
                }" title="{'' if i == j == 0 else (
                    tree[i][1][j - 1] if j != 0 else
                    tree[i - 1][1][-1]
                )}" {'disabled' if i == j == 0 else ''}>上一节</a>
                <a href="{
                '#' if i == len(tree) - 1 and j == len(tree[i][1]) - 1 else (
                    f"{urllib.parse.quote(tree[i][1][j + 1])}.html" if j != len(tree[i][1]) - 1 else
                    (
                            f"../{urllib.parse.quote(tree[i + 1][0])}/"
                            + f"%E7%AB%A0%E9%A6%96.html"
                    )
                )
                }" title="{'' if i == len(tree) - 1 and j == len(tree[i][1]) - 1 else (
                    tree[i][1][j + 1] if j != len(tree[i][1]) - 1 else
                    tree[i + 1][0]
                )}" {'disabled' if i == len(tree) - 1 and j == len(tree[i][1]) - 1 else ''}>下一节</a>
                <a href="{
                '#' if i == len(tree) - 1 else (f'../{urllib.parse.quote(tree[i + 1][0])}/'
                                                + f'%E7%AB%A0%E9%A6%96.html')
                }" title="{'' if i == len(tree) - 1 else tree[i + 1][0]}" {
                'disabled' if i == len(tree) - 1 else ''
                }>下一章</a>
            </nav>
'''
            elif file == '首页.md':
                title = "Python从入门到入坟"
                link_html = f'''
            <nav>
                <a href="{urllib.parse.quote(tree[0][0])}/%E7%AB%A0%E9%A6%96.html" title="{tree[0][0]}">开始阅读</a>
                <a href="#ContentTable" title="目录">转至目录</a>
            </nav>
'''
            elif file == '章首.md':
                cap = path.strip("/").rsplit("/")[-1]
                i = list(map(lambda x: x[0], tree)).index(cap)
                title = cap
                link_html = f'''
            <nav>
                <a href="{
                '#' if i == 0 else f'../{urllib.parse.quote(tree[i - 1][0])}/%E7%AB%A0%E9%A6%96.html'
                }" title="{
                '' if i == 0 else tree[i - 1][0]
                }" {"disabled" if i == 0 else ''}>上一章</a>
                <a href="{
                urllib.parse.quote(tree[i][1][0])}.html" title="{tree[i][1][0]}">开始本章之旅</a>
                <a href="{
                '#' if i == len(tree) - 1 else f'../{urllib.parse.quote(tree[i + 1][0])}/%E7%AB%A0%E9%A6%96.html'
                }" title="{
                '' if i == len(tree) - 1 else tree[i + 1][0]
                }" {"disabled" if i == len(tree) - 1 else ''}>下一章</a>
            </nav>
'''
            else:
                title = "<kbd>出</kbd><kbd>现</kbd><kbd>问</kbd><kbd>题</kbd><kbd>了</kbd>"
                link_html = '''<kbd>出</kbd><kbd>现</kbd><kbd>问</kbd><kbd>题</kbd><kbd>了</kbd>'''

            with open(os.path.join(path, file), encoding='utf-8') as f:
                html = markdown.markdown(f.read(), output_format="html",
                                         extensions=["fenced_code", "tables"])
            html = f"""
<!DOCTYPE html>
<html lang="zh">
    <head>
        <title>{title} - Python从入门到入坟</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href='{path_to_root}resources/lxgw-wenkai-webfont/lxgwwenkai-regular.css'>
        <link rel="stylesheet" href='{path_to_root}resources/lxgw-wenkai-webfont/lxgwwenkaimono-regular.css'>
        <link rel="stylesheet" href="{path_to_root}resources/simple.css">
        <link rel="stylesheet" href="{path_to_root}resources/CodeHighLight/styles/hybrid.min.css">
        <script src="{path_to_root}resources/CodeHighLight/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
        <style>
            code.hljs{{
                background-color: var(--accent-bg) !important;
            }}
        </style>
        <style>
            body{{
                font-family: "LXGW WenKai",serif;
            }}
            code{{
                font-family: "LXGW WenKai Mono",monospace;
            }}
            a[disabled]{{
                cursor: not-allowed;
                filter: alpha(opacity=50);
                -moz-opacity: 0.5;
                opacity: 0.5;
            }}
            a[disabled]:hover{{
                cursor: not-allowed;
                filter: alpha(opacity=50);
                -moz-opacity: 0.5;
                opacity: 0.5;
            }}
            @media (prefers-color-scheme: dark) {{
                footer > nav :nth-child(2n) > button {{
                    background-color: #66CCFF !important;
                }}
            }}
            @media (prefers-color-scheme: light) {{
                footer > nav :nth-child(2n) > button {{
                    background-color: #0F604E !important;
                }}
            }}
            button{{
                font-family: LXGW WenKai;
            }}
            .right{{
                color: #00ff00;
                font-size: 30px;
            }}
            .right::before{{
                content: "✔";
            }}
            .wrong{{
                color: #ff0000;
                font-size: 30px;
            }}
            .wrong::before{{
                content: "❌";
            }}
            .showMessage{{
                padding: 10px 20px;
                border-radius: 5px;
                position: fixed;
                top: 15%;
                left: 50%;
                color: #000000;
                background-color: #FFFFFF;
                border: 1px solid #F0F0F0;
                z-index: 999;
                transform: translate(-50%, 0);
            }}
            .showMessageSuccess{{
                background-color: #F0F9EB;
                border: 1px solid #E1F3D8;
                color: #67C23A;
            }}
            .showMessageError{{
                background-color: #FEF0F0;
                border: 1px solid #FDE2E2;
                color: #F76C6C;
            }}
            .showMessageInfo{{
                background-color: #70C3E3;
                border: 1px solid #13B8EB;
                color: #FFFFFF;
            }}
        </style>
        <script src="{path_to_root}resources/jquery-3.6.1.min.js" type="application/javascript"></script>
        <script type="application/javascript">
            $(document).ready(
                function(){{
                    $('a[disabled]').click(function(event){{
                            // console.log("clicked");
                            event.preventDefault();
                        }} 
                    );
                    nav = $("<nav></nav>")
                    $('footer>nav>a').each(function(index, elem){{
                        c_elem = $(elem).clone();
                        c_elem.empty();
                        inner = $("<button></button>");
                        inner.append(elem.innerText);
                        inner.appendTo(c_elem);
                        if (elem.hasAttribute('disabled')){{
                            inner.attr('disabled', true);
                        }}
                        c_elem.appendTo(nav)
                        elem.remove()
                    }})
                    nav.insertBefore($("footer>:first-child"))
                    align = $("[align]")
                    align.each((e)=>{{
                        e = align.get(e)
                        e.style.textAlign = e.attributes.align.value;
                    }})
                }}
            );
            function showMessage(message, type) {{
                let messageJQ = $("<div class='showMessage'>" + message + "</div>");
                if (type === 0) {{
                    messageJQ.addClass("showMessageError");
                }} else if (type === 1) {{
                    messageJQ.addClass("showMessageSuccess");
                }} else if (type === 2) {{
                    messageJQ.addClass("showMessageInfo");
                }}
                messageJQ.hide().appendTo("body").slideDown(400);
                window.setTimeout(function(){{
                    messageJQ.show().slideUp(400, function(){{
                        messageJQ.remove();
                    }})
                }}, 4000);
            }}
        </script>
    </head>
    <body>
        <header>
            <nav>
                <a href="{path_to_root[:-3]}%E9%A6%96%E9%A1%B5.html">首页</a>
                <a href="{path_to_root[:-3]}%E9%A6%96%E9%A1%B5.html#ContentTable">目录</a>
                <a href="https://github.com/PiYuanZhouLv/LearningPythonFromARunoobToYourTomb/">
                    <svg style="height: 1em;" class="icon" viewBox="0 0 32 32">
                        <path d="M16 0.395c-8.836 0-16 7.163-16 16 0 7.069 4.585 13.067 10.942 15.182 0.8 0.148 1.094-0.347 1.094-0.77 0-0.381-0.015-1.642-0.022-2.979-4.452 0.968-5.391-1.888-5.391-1.888-0.728-1.849-1.776-2.341-1.776-2.341-1.452-0.993 0.11-0.973 0.11-0.973 1.606 0.113 2.452 1.649 2.452 1.649 1.427 2.446 3.743 1.739 4.656 1.33 0.143-1.034 0.558-1.74 1.016-2.14-3.554-0.404-7.29-1.777-7.29-7.907 0-1.747 0.625-3.174 1.649-4.295-0.166-0.403-0.714-2.030 0.155-4.234 0 0 1.344-0.43 4.401 1.64 1.276-0.355 2.645-0.532 4.005-0.539 1.359 0.006 2.729 0.184 4.008 0.539 3.054-2.070 4.395-1.64 4.395-1.64 0.871 2.204 0.323 3.831 0.157 4.234 1.026 1.12 1.647 2.548 1.647 4.295 0 6.145-3.743 7.498-7.306 7.895 0.574 0.497 1.085 1.47 1.085 2.963 0 2.141-0.019 3.864-0.019 4.391 0 0.426 0.288 0.925 1.099 0.768 6.354-2.118 10.933-8.113 10.933-15.18 0-8.837-7.164-16-16-16z">
                        </path>
                    </svg>
                    Github
                </a>
                <span>附上常用网址:</span>
                <a href="https://www.baidu.com/">
                    <img style="height: 1em;" 
                    src="https://www.baidu.com/img/baidu_85beaf5496f291521eb75ba38eacbd87.svg" alt="">
                    百度
                </a>
                <a href="https://www.bilibili.com">
                    <img style="height: 1em;" src="https://www.bilibili.com/favicon.ico?v=1" alt="">
                    Bilibili
                </a>
                <a href="https://www.python.org">
                    <img style="height: 1em;" src="https://www.python.org/static/favicon.ico" alt="">
                    Python
                </a>
            </nav>
            <h1>{title}</h1>
            {link_html}
        </header>
        <main>{html}</main>
        <footer>
        {link_html}
        Author: PiYuanZhouLv
        </footer>
    </body>
</html>
"""
            with open(
                    os.path.join(
                        path.replace("Markdown", "HTML"),
                        file.replace(".md", ".html")
                    ),
                    'w', encoding='utf-8'
            ) as f:
                f.write(html)
        else:
            print("copy", file, "to new folder")
            shutil.copy(
                os.path.join(path, file),
                os.path.join(path.replace("Markdown", "HTML"), file.replace(".md", ".html"))
            )

# print('=' * 10)

content_table = io.StringIO()


def f(content, path=''):
    if len(content) == 2 and type(content[1]) == list:
        print('<details>', file=content_table)
        print('<summary>', file=content_table)
        print(content[0],
              f'<a href="{urllib.parse.quote(path + content[0] + "/")}'
              + f'%E7%AB%A0%E9%A6%96.html">跳转</a>',
              file=content_table)
        print("</summary>", file=content_table)
        f(content[1], path + content[0] + '/')
        print('</details>', file=content_table)
    elif type(content) == list and type(content[0]) == tuple:
        [f(sub_content, path) for sub_content in content]
    else:
        print('<ul>', file=content_table)
        for c in content:
            print('<li>', f'<a href="{urllib.parse.quote(path + c)}.html">{c}</a>', '</li>', file=content_table)
        print('</ul>', file=content_table)


print('<details id="ContentTable">', file=content_table)
print('<summary>', '目录', '</summary>', file=content_table)
[f(sub_tree) for sub_tree in tree]
print('</details>', file=content_table)
with open('HTML/首页.html', encoding='utf-8') as f:
    content = f.read()
with open('cover_final.txt', encoding='utf-8') as f:
    cover = f.read()
content = content.replace('%ContentTable%', content_table.getvalue()).replace('%Cover%', f'''
<pre><div style="transform: scale(0.41);margin-top: -750;margin-bottom: -750;margin-left: -200;font-size: 12px;">{
    cover
}</div></pre>''').replace(
    '%CopyButton%',
    f'''
<button id="copy_to_see" title="将这段代码复制到 Python Shell 中会输出源代码">复制为源代码</button>
<button id="copy_to_run" title="将这段代码复制到 Python Shell 中会直接执行">复制为可执行代码</button>
<script src="../resources/clipboard/dist/clipboard.min.js" type="application/javascript"></script>
<script type="application/javascript">
    $('#copy_to_see').click(() => {{
        const textCopied = ClipboardJS.copy(`{cover.replace('eval(', 'print(', 1).replace(')###', '####').replace(chr(92), chr(92)*2)}`);
        $('#copy_to_see').text('Copied!');
        setTimeout(()=>{{$('#copy_to_see').text('复制为源代码')}}, 1000)
        console.log('copied!', textCopied);
    }})
    
    $('#copy_to_run').click(() => {{
        const textCopied = ClipboardJS.copy(`{cover.replace(chr(92), chr(92)*2)}`);
        $('#copy_to_run').text('Copied!');
        setTimeout(()=>{{$('#copy_to_run').text('复制为可执行代码')}}, 1000)
        console.log('copied!', textCopied);
    }})
</script>
'''
)
with open('HTML/首页.html', 'w', encoding='utf-8') as f:
    f.write(content)
