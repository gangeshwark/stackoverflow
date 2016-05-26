# test file
import HTMLParser


def remove_tags(text):
    passtext = HTMLParser.HTMLParser().unescape(text)
    shortenedText = [e.lower() and e.translate(passtext.maketrans("", ""), passtext.punctuation) for e in text.split()
                     if len(e) >= 3 and not e.startswith('http')]
    return shortenedText


def main():
    strg = """**Possible Duplicate:**[Where can I find stock or custom ROMs for my Android device?]"""
    print remove_tags(strg)
