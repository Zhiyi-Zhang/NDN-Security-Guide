import sys
import os
import re
sys.path.insert(0, os.path.abspath('NDN_TR'))

extensions = ['customizations']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'security-guide'

# General information about the project.
project = u'NDN Security Guide'
copyright = u''
author = u'Zhiyi Zhang, Yingdi Yu, Alex Afanasyev, Lixia Zhang'

NDN = {
    'tr-number': 'NDN-0051',
    'revisions': [
        {
            'number': '1',
            'date': 'April 12, 2017',
            'link': '',
        },
    ]}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------
html_theme = 'alabaster'
# html_theme_options = {}
html_static_path = ['_static']

# -- Options for LaTeX output ---------------------------------------------

offset = -85
NDN_revision_text = ''
for revision in NDN['revisions']:
    NDN_revision_text += '''%
\put(\strip@pt\@tempdimb,\strip@pt\@tempdimc){%
    \makebox(0,''' + str(offset) + ''')[l]{\color{black}%
Revision ''' + revision['number'] + ''': ''' + revision['date'] + '''}
  }%'''
    offset -= 20

latex_elements = {
    'papersize': 'letterpaper,onecolumn',
    'pointsize': '10pt',
    'tableofcontents': '',
    'geometry': '\\usepackage[margin=0.8in]{geometry}',
    'preamble': '''
\usepackage{eso-pic,xcolor}
\makeatletter
\AddToShipoutPicture*{%
\setlength{\@tempdimb}{20pt}%
\setlength{\@tempdimc}{\paperheight}%
\setlength{\unitlength}{1pt}%
\put(\strip@pt\@tempdimb,\strip@pt\@tempdimc){%
    \makebox(0,-60)[l]{\color{blue}%
NDN, Technical Report NDN-0054. \url{http://named-data.net/techreports.html}}
  }%
''' + NDN_revision_text + '''
}
\makeatother

\\usepackage{etoolbox}
\\usepackage{xstring}
\\DeclareListParser{\\doslashlist}{/}
\\newcounter{ndnNameComponentCounter}%
\\newcommand{\\ndnName}[1]{{%
  \\setcounter{ndnNameComponentCounter}{0}%
  \\renewcommand{\\do}[1]{{%
    \\ifnumgreater{\\value{ndnNameComponentCounter}}{0}{\\allowbreak/}{}%
    \\ifnumodd{\\value{ndnNameComponentCounter}}{}{}%
    ##1}%
    \\stepcounter{ndnNameComponentCounter}}%
``{\\fontfamily{cmtt}\\small\\selectfont\\IfBeginWith{#1}{/}{/}{}\\doslashlist{#1}}''%
}}

\\sphinxsetup{TitleColor={rgb}{0,0,0}}
\\pagestyle{headings}
\\fvset{frame=none,fontfamily=cmtt}
\\renewcommand*{\\ttdefault}{cmtt}
''',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_toplevel_sectioning = 'section'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, '%s-%s.tex' % (NDN['tr-number'].lower(), master_doc), project, author, '../../NDN_TR/ndn-tr'),
]
