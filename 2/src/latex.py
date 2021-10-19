from pylatex import Document, Section, Subsection, Alignat, Figure, NoEscape, LongTable
from more_itertools import ichunked

def print_table(doc, data, caption, row_size=10):
    with doc.create(Section(caption)):
        with doc.create(LongTable("l " * row_size)) as table:
            for i in ichunked(data, row_size):
                table.add_row(list(i))

def latex_solution(data):
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    
    print_table(doc, data, 'input data')
    print_table(doc, sorted(data), 'variational series')

    doc.generate_pdf('full', clean_tex=False)