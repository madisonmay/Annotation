import re

from colorama import Fore, Back, Style


class Document(object):

    def __init__(self, text, labels=None):
        """
        Document class designed for easy annotation + colored annotation display
        """
        self.text = text
        self.labels = labels
        if not self.labels:
            self.labels = {}
        self.annotations = []

    def add_label(self, label, color):
        """
        Add a new category of annotation
        """
        self.labels[label] = color

    def get_style_modifier(self, color):
        """
        Retrieve the color code necessary to highlight text background
        """
        style_modifier = getattr(Back, color.upper(), None)

        if style_modifier is None:
            accepted_colors = ", ".join(Back.__dict__.keys())
            raise ValueError(
                "The color `{color}` is not a supported highlight color."
                " Please choose from the following: {accepted_colors}".format(
                    color=color.upper(),
                    accepted_colors=accepted_colors
                )
            )

        return style_modifier

    def highlight(self, search_term, color='yellow'):
        """
        Highlight all occurrences of a given search term
        """
        style_modifier = self.get_style_modifier(color)
        for match in re.finditer(search_term, self.text):
            self.annotations.append({
                'start': match.start(),
                'end': match.end(),
                'style': style_modifier
            })

    def formatted_text(self):
        """
        Produce a nicely formatted representation of annotations
        """
        self.annotations.sort(key=lambda annotation: annotation.get('start'))

        cursor = 0
        formatted_text_chunks = []
        for annotation in self.annotations:
            start, end = annotation.get('start'), annotation.get('end')
            formatted_text_chunks.extend([
                self.text[cursor:start],
                annotation.get("style"),
                self.text[start:end],
                Style.RESET_ALL
            ])
            cursor = end
        formatted_text_chunks.append(self.text[cursor:])

        return "".join(formatted_text_chunks)


    def highlight_range(self, start, end, color='yellow'):
        """
        Highlight a character range
        """
        self.annotations.append({
            'start': start,
            'end': end,
            'style': self.get_style_modifier(color)
        })

    def annotate(self, search_term, category):
        """
        Annotate all occurrences of a search term
        """
        try:
            color = self.labels[category]
        except KeyError:
            raise ValueError(
                "Annotation type `{category}` does not exist.".format(
                    category=category
                )
            )
        
        self.highlight(search_term, color)

    def annotate_range(self, start, end, category):
        """
        Annotate a character range
        """
        try:
            color = self.labels[category]
        except KeyError:
            raise ValueError(
                "Annotation type `{category}` does not exist.".format(
                    category=category
                )
            )

        self.highlight_range(start, end, color)

    def __repr__(self):
        return self.formatted_text()

if __name__ == "__main__":
    sample_text = "Nothing but a tiny little library for making text annotation a little easier."
    doc = Document(sample_text)

    doc.add_label('adjective', 'yellow')
    doc.add_label('noun', 'blue')
    doc.add_label('verb', 'red')
    
    doc.annotate('little', category='adjective')
    doc.annotate('library', category='noun')
    print(doc)
