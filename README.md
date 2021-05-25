# ei

Automatically embed IPython into arbitrary stack frames in traceback.

## Install

```bash
pip install ei

# Or from GitHub
pip install git+https://github.com.djosix/ei.git
```

## Usage

Basic usage:

```python
def main():
    a = 123
    b = 0
    return a / b

if __name__ == '__main__':
    import ei; ei.patch()

    main()
```

You can also unpatch:

```python
ei.unpatch() # this will recover the exception hook
```

Context manager:

```python
with ei.capture():
    main()

# The exception hook is recovered
```
