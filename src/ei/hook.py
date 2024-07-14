'''
Copyright (c) 2021 Yuankui Lee

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


class Hook:
    COLOR_SCHEME_LIST = ('Linux', 'LightBG', 'Neutral')

    def __init__(self, select=True, verbose=False, color='Neutral', ostream=sys.stdout):
        try:
            mode = ostream.mode
            writable = ostream.writable()
            ostream.write
        except AttributeError:
            raise TypeError('invalid type of ostream')

        if 'b' in mode:
            raise TypeError('expect ostream in text mode')

        if not writable:
            raise ValueError('ostream is not writable')

        if color not in self.COLOR_SCHEME_LIST or not ostream.isatty():
            color = 'NoColor'

        self.select = select
        self.verbose = verbose
        self.color = color
        self.ostream = ostream

        self.ansi_color = ''
        self.ansi_reset = ''
        if color in ('Linux', 'Neutral'):
            self.ansi_color = '\033[33m'
            self.ansi_reset = '\033[0m'

    def __print(self, text):
        self.ostream.write(self.ansi_color)
        self.ostream.write(text)
        self.ostream.write(self.ansi_reset)
        self.ostream.flush()

    def __embed(self, frame, exc, tb):
        user_module = inspect.getmodule(frame)
        user_ns = frame.f_locals
        default_ns = {'exc': exc, 'tb': tb}

        if sys.version_info < (3, 7):
            # fix error in warning for python<3.7
            user_ns.setdefault('__name__', user_module.__name__)

        for key, value in default_ns.items():
            user_ns.setdefault(key, value)

        from IPython import embed
        embed(banner1='', user_module=user_module, user_ns=user_ns, colors=self.color)

    def __call__(self, exc_type, exc, tb):
        from IPython.core.ultratb import AutoFormattedTB
        tb_handler = AutoFormattedTB(mode=['Context', 'Verbose'][self.verbose],
                                     color_scheme=self.color,
                                     ostream=self.ostream)

        frames = [t[0] for t in traceback.walk_tb(tb)]
        records = tb_handler.get_records(tb, 5, None)
        assert len(frames) == len(records)

        def print_frames():
            for i, record in zip(reversed(range(len(records))), records):
                self.ostream.write(self.ansi_color)
                self.ostream.write('({}) '.format(i))
                self.ostream.write(self.ansi_reset)
                self.ostream.write(tb_handler.format_record(record))
                self.ostream.write('\n')

        print_frames()

        if not self.select:
            selection = 0
            frame = frames[len(frames)-1-selection]
            self.__print('Selected ({}) {}\n'.format(selection, frame))
            self.__embed(frame, exc, tb)
            return

        while True:
            self.ostream.write('\n')
            self.__print('Select a stack frame (q: quit, ?: info) [0]: ')

            try:
                line = input().strip()
                if line == 'q':
                    return
                elif line == '?':
                    print_frames()
                    continue
                elif line == '':
                    selection = 0
                elif not line.isdigit():
                    self.__print('[!] please input a nonnegative integer\n')
                    continue
                else:
                    selection = int(line)
                    if selection not in range(len(frames)):
                        self.__print('[!] valid range is 0-{}\n'.format(len(frames) - 1))
                        continue
            except (KeyboardInterrupt, EOFError):
                break

            frame = frames[len(frames)-selection-1]
            self.__print('Selected ({}) {}\n'.format(selection, frame))
            self.__embed(frame, exc, tb)
