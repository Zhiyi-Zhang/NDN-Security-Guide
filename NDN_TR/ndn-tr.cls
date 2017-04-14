\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{NDN-TR}[2017/03/16]

\LoadClass{IEEEtran}

\newcounter{subparagraph}[paragraph]

\renewcommand \thesection {\@arabic\c@section.}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}

\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}{3.25ex \@plus1ex \@minus .2ex}{-1em}{\normalfont\normalsize\bfseries}}
