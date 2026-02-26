from pathlib import Path

def fileread(filename, authority):
    text = ''
    filepath = Path(__file__).parent.parent / "texts" / filename

    try:
       with open(filepath, authority, encoding='utf-8') as f:
          text = f.read()
    except FileNotFoundError:
        print('FileNotFoundError')

    return text
