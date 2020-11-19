'''
Copyright (c) 2020 Yuankui Lee

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

import inspect
import traceback


class Hook:
    def __init__(self, select=False, tb_class='AutoFormattedTB', tb_mode='Context', tb_color='Neutral'):
        self.select = select
        self.tb_class = tb_class
        self.tb_mode = tb_mode
        self.tb_color = tb_color
    
    def __call__(self, exc_type, exc, tb):
        from IPython import embed
        import IPython.core.ultratb
        
        TB = getattr(IPython.core.ultratb, self.tb_class)
        tb_handler = TB(mode=self.tb_mode, color_scheme=self.tb_color)
        tb_handler(exc_type, exc, tb)
        
        frames = [t[0] for t in traceback.walk_tb(tb)][::-1]
        
        while True:
            print()
            
            if self.select:
                print('Select a stack frame to embed IPython shell (default: 0):')
                for i, frame in enumerate(frames):
                    print('{}. {}'.format(i, frame))
                try:
                    s = input('> ').strip()
                    if s in ('exit', 'quit', 'end', 'leave'):
                        break
                    n = int(s) if s else 0
                    frame = frames[n]
                except (KeyboardInterrupt, EOFError):
                    break
                except:
                    continue
            else:
                frame = frames[0]

            print('Embedded into', frame)
            
            user_module = inspect.getmodule(frame)
            user_ns = frame.f_locals
            
            user_ns.setdefault('etype', exc_type)
            user_ns.setdefault('evalue', exc)
            user_ns.setdefault('etb', tb)
        
            embed(banner1='', user_module=user_module, user_ns=user_ns, colors='Neutral')
            
            if not self.select:
                break
