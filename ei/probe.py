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


def probe():
    # Import IPython only when this function gets call
    from IPython import embed
    import IPython.core.ultratb
    
    print('IPython debug hook is available!')
    
    for name, value in IPython.core.ultratb.__dict__.items():
        # filter out other classes
        if not isinstance(value, type):
            continue
        if value is IPython.core.ultratb.TBTools:
            continue
        if not issubclass(value, IPython.core.ultratb.TBTools):
            continue
        
        # traceback class instance
        tb = value()
        
        # get valid modes
        modes = getattr(tb, 'valid_modes', None)
        
        # get valid color schemes
        colors = None
        if hasattr(tb, 'color_scheme_table'):
            colors = list(getattr(tb, 'color_scheme_table').keys())

        print('  class {}'.format(name))
        print('    modes: {}'.format(modes))
        print('    colors: {}'.format(colors))
