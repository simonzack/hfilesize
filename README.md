# Human Readable File Sizes

Parses & Formats integer file sizes to human readable file sizes.

## Example Usage

### Parsing

    >>> from hfilesize import Format, FileSize
    >>> FileSize('1k')
    ... 1000
    >>> FileSize('1K')
    ... 1024
    >>> FileSize('1kib')
    ... 1024
    >>> FileSize('1K', default_binary=False, case_sensitive=False)
    ... 1000
    >>> FileSize('1 kibibyte')
    ... 1024

### Formatting

    >>> '{:d}'.format(FileSize(1024))
    ... '1024'
    >>> '{:.02fH}'.format(FileSize(1024))
    ... '1 KB'
    >>> '{:.02fHcv}'.format(FileSize(1024))
    ... '1 kilobyte'
    >>> '{:.02fhs}'.format(FileSize(1000))
    ... '1 KB'
    >>> '{:.02fhs^0}'.format(FileSize(1000))
    ... '1000 B'
    >>> '{: >10.02fH}'.format(FileSize(1024))
    ... '      1 KB'

## Documentation

### Parsing Options

- `case_sensitive`:
Use 1024 for upper case and 1000 for lower case if casing exists, as is common in unix utilities, e.g. dd

- `default_binary`:
Default base if it is not clear what the unit is (i.e. if it is not 'mib' or 'mebibytes')

### Formatting Options

- format type:      `[hH][size_format][^exponent]`
    - `h`:              Base 1000
    - `H`:              Base 1024
- `size_format`:    `c | cs | cv | e | ev | s | sv`
    - `c`:              Commonly used case-sensitive suffixes 
    - `cs`:             Commonly used abbreviated case-sensitive suffixes
    - `cv`:             Commonly used verbose case-sensitive suffixes
    - `e`:              IEC suffixes
    - `ev`:             IEC verbose suffixes
    - `s`:              SI suffixes
    - `sv`:             SI verbose suffixes
- `exponent`:       `integer`

## References
Inspired by:

- [`hurry.filesize`](https://pypi.python.org/pypi/hurry.filesize)
- [Human readable file/memory sizes v2 (Python recipe) ](http://code.activestate.com/recipes/578323-human-readable-filememory-sizes-v2/)

## License
Licensed under GPLv3.
