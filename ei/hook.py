'''
Copyright (c) 2025 Yuankui Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import inspect
import traceback


tb_context_lines = 5
tb_verbose_lines = 7


def _print_frames(tb_handler, records):
    for i, record in zip(reversed(range(len(records))), records):
        # Prepend a number for stack frame selection
        print('({}) {}'.format(i, tb_handler.format_record(record)))


def _embed(frame, exc, tb):
    user_module = inspect.getmodule(frame)
    user_ns = frame.f_locals.copy()
    default_ns = {'exc': exc, 'tb': tb}

    if sys.version_info < (3, 7):
        # Fix error for python<3.7
        user_ns.setdefault('__name__', user_module.__name__)

    for key, value in default_ns.items():
        user_ns.setdefault(key, value)

    from IPython import embed
    embed(
        display_banner=False,
        user_module=user_module,
        user_ns=user_ns,
        colors=('NoColor', 'Linux')[sys.stdout.isatty()],
    )


def hook(_exc_type, exc, tb):
    from IPython.core.ultratb import AutoFormattedTB
    context_tb = AutoFormattedTB(mode='Context')
    verbose_tb = AutoFormattedTB(mode='Verbose')

    frames = [t[0] for t in traceback.walk_tb(tb)]
    context_records = context_tb.get_records(tb, tb_context_lines, None)
    verbose_records = verbose_tb.get_records(tb, tb_verbose_lines, None)
    assert len(frames) == len(context_records) == len(verbose_records)

    _print_frames(context_tb, context_records)

    while True:
        print('Select a stack frame (q: quit, ?: info, ??: details) [0]: ', end='', flush=True)

        try:
            line = input().strip()
            if line == 'q':
                return
            elif line == '?':
                _print_frames(context_tb, context_records)
                continue
            elif line == '??':
                _print_frames(verbose_tb, verbose_records)
                continue
            elif line == '':
                selection = 0
            elif not line.isdigit():
                print('Error: please input a nonnegative integer')
                continue
            else:
                selection = int(line)
                if selection not in range(len(frames)):
                    print('Error: valid range is 0-{}'.format(len(frames) - 1))
                    continue
        except (KeyboardInterrupt, EOFError):
            break

        frame = frames[len(frames)-selection-1]
        print('Selected ({}) {}'.format(selection, frame))
        _embed(frame, exc, tb)
