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
    def __init__(self, select=True, verbose=False, color='Neutral'):
        if color not in ('Linux', 'LightBG', 'Neutral'):
            color = 'NoColor'

        self.select = select
        self.verbose = verbose
        self.color = color

        if color in ('Linux', 'Neutral'):
            self.color_index = '\033[33m'
            self.color_prompt = '\033[33m'
            self.color_reset = '\033[0m'
        else:
            self.color_index = ''
            self.color_prompt = ''
            self.color_reset = ''

    def __create_tb_class(self):
        from IPython.core.ultratb import AutoFormattedTB
        
        class TB(AutoFormattedTB):
            def format_records(self_, *args):
                frames = super().format_records(*args)
                num_frames = len(frames)
                for i in range(num_frames):
                    r = num_frames - i - 1
                    index = '{}({}){}'.format(self.color_prompt, i, self.color_reset)
                    frames[r] = '{} {}'.format(index, frames[r])
                return frames

        return TB
    
    def __call__(self, exc_type, exc, tb):
        from IPython import embed

        TB = self.__create_tb_class()
        tb_mode = ['Context', 'Verbose'][self.verbose]
        tb_handler = TB(mode=tb_mode, color_scheme=self.color)
        tb_handler(exc_type, exc, tb)
        
        frames = [t[0] for t in traceback.walk_tb(tb)][::-1]

        def prompt(*args, **kwargs):
            print(end=self.color_prompt)
            print(*args, **kwargs)
            print(end=self.color_reset, flush=kwargs.get('flush', False))

        while True:
            print()
            
            if self.select:
                prompt('Select a stack frame (default: 0, ? for info): ', end='')
                
                try:
                    s = input().strip()
                    if s in ('exit', 'quit', 'end', 'leave'):
                        break
                    if s == '?':
                        tb_handler(exc_type, exc, tb)
                        continue
                    n = int(s) if s else 0
                except (KeyboardInterrupt, EOFError):
                    break
                except:
                    continue
            else:
                n = 0

            frame = frames[n]
            prompt('Selected ({}) {}'.format(n, frame))
            
            user_module = inspect.getmodule(frame)
            user_ns = frame.f_locals

            if sys.version_info < (3, 7):
                # fix error in warning for python<3.7
                user_ns.setdefault('__name__', user_module.__name__)

            default_ns = {
                'exc': exc,
                'tb': tb
            }
            
            for key, value in default_ns.items():
                if key not in user_ns or value is user_ns[key]:
                    prompt('{:>8s}: {!r}'.format(key, value))
                    user_ns[key] = value

            embed(banner1='', user_module=user_module, user_ns=user_ns, colors=self.color)
            
            if not self.select:
                break
