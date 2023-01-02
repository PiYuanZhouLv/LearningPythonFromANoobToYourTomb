import io
import math

# import
from PIL import Image
import numpy

# open sources
cover_base = Image.open('cover_base.png').convert("L")
fill_code = ("eval('''"
             + repr(open('fill_code.py', encoding='utf-8').read()).replace('\\\'', '\'').replace('\\n', '\\ń').replace(' ', '\\S')[1:-1]
             + "'''.replace('\\n', '').replace(' ', '').replace('\\ń', '\\n').replace('\\S', ' '))")

# parse base
new_base = []
count = 0
base = numpy.array(cover_base).tolist()
w, h = len(base[0]), len(base)
with open('temp.txt', 'w') as f:
    f.write(repr(base))
for line in base:
    current_line = []
    for cell in line:
        if cell <= 240:
            current_line.append(True)
            count += 2
        else:
            current_line.append(False)
    new_base.append(current_line)

with open('cover.txt', 'w') as f:
    f.write('\n'.join([''.join(['TT' if cell else '  ' for cell in line]) for line in new_base]))

output = io.StringIO()
if count > len(fill_code):
    fill_code = repr(open('fill_code.py', encoding='utf-8').read()).replace(' ', '\\S').replace('\\\'', '\'').replace('\\n', '\\ń')[1:-1]
    times = (count - 89 - len(str(len(fill_code)))) // len(fill_code) + 1
    fill_code = f"eval('''{fill_code * times}'''.replace(' ', '').replace('\\n', '')[:{len(fill_code)}].replace('\\ń', '\\n').replace('\\S', ' '))"
x = int(
    (
        -2 * (w + h)
        + math.sqrt(
            4 * (w + h) ** 2
            - 16 * (count - len(fill_code))
        )
    ) / 8
) + 1
seek = 0
for i in range(x):
    output.write(fill_code[seek:seek + (w + 2 * x)*2].ljust((w + 2 * x)*2, '#'))
    seek += (w + 2 * x)*2
    output.write('\n')
for line in new_base:
    for i in range(x):
        output.write(fill_code[seek:seek + 2].ljust(2, '#'))
        seek += 2
    for cell in line:
        if cell:
            output.write(fill_code[seek:seek + 2].ljust(2, '#'))
            seek += 2
        else:
            output.write('  ')
    for i in range(x):
        output.write(fill_code[seek:seek + 2].ljust(2, '#'))
        seek += 2
    output.write('\n')
for i in range(x):
    output.write(fill_code[seek:seek + (w + 2 * x)*2].ljust((w + 2 * x)*2, '#'))
    seek += (w + 2 * x)*2
    output.write('\n')
# eval(''''''.replace(' ', '').replace('\n', '').replace('\\S', ' ')[::n])
with open('cover_final.txt', 'w', encoding='utf-8') as f:
    f.write(output.getvalue())
