% -- ------------------------------------------------------------------------------------ -- %
% -- Proyecto:                                                                            -- %
% -- Codigo:                                                                              -- %
% -- Repositorio:                                                                         -- %
% -- Autor:                                                                               -- %
% -- ------------------------------------------------------------------------------------ -- %

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class options                        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Orientation:                         %
% portrait (default), landscape        %
%                                      %
% Paper size:                          %
% a0paper (default), a1paper, a2paper, %
% a3paper, a4paper, a5paper, a6paper   %
%                                      %
% Language:                            %
% english (default), norsk             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{iteraposter}

\DeclareOption{english}{\def\iteraposter@lang{english}}
\DeclareOption{portrait}
{
  \PassOptionsToPackage{orientation = portrait}{beamerposter}
  \def\iteraposter@orientation{}
}
\DeclareOption{landscape}
{
  \PassOptionsToPackage{orientation = landscape}{beamerposter}
  \def\iteraposter@orientation{landscape}
}

\DeclareOption{a0paper}{\def\iteraposter@size{a0paper}}
\DeclareOption{a4paper}{\def\iteraposter@size{a4paper}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}

\ExecuteOptions{a4paper}
\ExecuteOptions{english}
\ExecuteOptions{portrait}
\ProcessOptions
\relax

\LoadClass[t]{beamer}

\RequirePackage[size = a0, scale = 1.5]{beamerposter}
\RequirePackage{etoolbox}
\RequirePackage{pgfpages}
\RequirePackage[utf8]{inputenx}
\RequirePackage[T1]{fontenc}
\RequirePackage{calc}
\RequirePackage[final]{microtype}
\RequirePackage{lmodern}
\RequirePackage[scaled]{beramono}

\hypersetup{colorlinks,
            urlcolor  = iteralink,
            linkcolor =,
            citecolor =,
            filecolor =}

\renewcommand{\sfdefault}{phv}
% \DeclareFontShape{OMX}{cmex}{m}{n}
% {
%     <-7.5>    cmex7
%     <7.5-8.5> cmex8
%     <8.5-9.5> cmex9
%     <9.5->    cmex10
% }{}
% \SetSymbolFont{largesymbols}{normal}{OMX}{cmex}{m}{n}
% \SetSymbolFont{largesymbols}{bold}  {OMX}{cmex}{m}{n}
% \setlength{\marginparwidth}{2cm}
% \setlength{\emergencystretch}{1em}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usefonttheme{serif}
\useinnertheme{rectangles}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{caption}[numbered]
\setbeamertemplate{caption label separator}{: }
\setbeamertemplate{qed symbol}{\(\blacksquare\)}
\setbeamertemplate{itemize items}{\color{itemize item.fg}\(\blacksquare\)}

\setlength{\labelsep}{3ex}
\setlength{\leftmargini}{18ex}
\setbeamersize{text margin left = 2cm, text margin right = 2cm}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% \definecolor{iterared}{cmyk}{0, 1, 1, 0}
% \definecolor{iterawhite}{cmyk}{0, 0, 0, 0}
% \definecolor{iterablack}{cmyk}{0, 0, 0, 1}
% \definecolor{iteraheader}{cmyk}{0, 0, 0, 0.6}
% \definecolor{iterabackground}{cmyk}{0, 0, 0, 0.2}
% \definecolor{iteralink}{HTML}{0B5A9D}

% Paleta 1: Fuente 1
\definecolor{1_iterablue1}{HTML}{21C6FF}
\definecolor{1_iterablue2}{HTML}{00A3FF}
\definecolor{1_iterablue3}{HTML}{0059A9}
\definecolor{1_iterablue4}{HTML}{00305D}

\definecolor{1_iteragreen1}{HTML}{00E9DA}
\definecolor{1_iteragreen2}{HTML}{62F3B3}
\definecolor{1_iteragreen3}{HTML}{00B472}

\definecolor{1_iterared1}{HTML}{FF6A7A}
\definecolor{1_iterared2}{HTML}{FF653C}

\definecolor{1_iterayellow1}{HTML}{F9F871}
\definecolor{1_iterayellow2}{HTML}{E7E761}

\definecolor{1_iteragrey1}{HTML}{D9E2E8}
\definecolor{1_iteragrey2}{HTML}{A8B0B6}
\definecolor{1_iteragrey3}{HTML}{798187}
\definecolor{1_iteragrey4}{HTML}{4E555A}

\definecolor{1_iterabluegrey1}{HTML}{C5DAE8}
\definecolor{1_iterabluegrey2}{HTML}{99AEBB}
\definecolor{1_iterabluegrey3}{HTML}{364954}

\definecolor{1_iterawhite1}{HTML}{FFFFFF}
\definecolor{1_iterawhite2}{HTML}{F7F7F7}

\definecolor{1_iteraback}{RGB}{29, 2, 2}
\definecolor{1_iterawhite}{HTML}{F2F2F0}
\definecolor{1_iteradark}{HTML}{364954}
\definecolor{1_iteradark1}{HTML}{99AEBB}
\definecolor{1_iterablue}{HTML}{00A3FF}
\definecolor{1_iterablue2}{HTML}{0059A9}
\definecolor{1_iteragreen}{HTML}{62F3B3}
\definecolor{1_iterayellow}{RGB}{254, 238, 33}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% -- Encabezado
\setbeamercolor{headline}{fg = 1_iterawhite2, bg = 1_iterablue2}
\setbeamercolor{title in headline}{fg = 1_iterawhite2}
\setbeamercolor{author in headline}{fg = 1_iterawhite2}

\setbeamercolor{background canvas}{fg = 1_iterawhite1, bg = 1_iterawhite1}
\setbeamercolor{footline}{fg = 1_iterawhite, bg = 1_iterablue3}

\setbeamercolor{structure}{fg = 1_iterablue}
\setbeamercolor{alerted text}{fg = 1_iterawhite}

\setbeamercolor{block title}{fg = 1_iterawhite, bg = 1_iteragrey3}
\setbeamercolor{block body} {fg = 1_iteragrey4, bg = 1_iterawhite1}

\setbeamercolor{block title highlighted}{fg = 1_iterawhite, bg = 1_iterawhite}
\setbeamercolor{block body highlighted} {fg = 1_iteragrey4, bg = 1_iterawhite}

\setbeamercolor{block title alerted}{fg = 1_iterawhite, bg = 1_iterawhite}
\setbeamercolor{block body alerted} {fg = 1_iteragrey4, bg = 1_iterawhite}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamerfont{title in headline}{family = \sffamily,
                                  series = \bfseries,
                                  size   = \LARGE}
                                  
\setbeamerfont{author in headline}{family = \sffamily,
                                   series = \bfseries,
                                   size   = \large}
                                   
\setbeamerfont{institute}{family = \sffamily,
                          series = \mdseries,
                          size   = \small}

\setbeamerfont{block title}{family = \sffamily,
                            series = \bfseries,
                            size   = \large}
                            
\setbeamerfont{block title alerted}{family = \sffamily,
                                    series = \bfseries,
                                    size   = \large}
                                    
\setbeamerfont{block title highlighted}{family = \sffamily,
                                    series = \bfseries,
                                    size   = \large}

\setbeamerfont{block body}{family = \rmfamily,
                           series = \normalfont,
                           size   = \normalsize}
                           
\setbeamerfont{block body highlighted}{family = \rmfamily,
                                   series = \normalfont,
                                   size   = \normalsize}
                                   
\setbeamerfont{block body alerted}{family = \rmfamily,
                                   series = \normalfont,
                                   size   = \normalsize}

\setbeamerfont{item projected}{family = \sffamily,
                               series = \bfseries,
                               size   = \small}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{headline}
{
    \begin{beamercolorbox}[wd = \paperwidth, leftskip  = 3cm,
                           rightskip = 3cm plus 20cm]{headline}
        \vskip.5cm
        \usebeamerfont{title in headline}
        \usebeamercolor{title in headline}
        \color{fg}
        \vskip1.5ex
        \inserttitle
        \vskip1.75ex
        \usebeamerfont{author in headline}
        \usebeamercolor{author in headline}
        \color{fg}
        \insertauthor
        \ifdefempty{\insertinstitute}{}
        { \vskip1ex
          \usebeamerfont{institute}
          \def\beamer@andinst{\quad}
          \insertinstitute
        }
        \vskip3cm
    \end{beamercolorbox}
    \vskip1cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{footline}
{
    \leavevmode
    \begin{beamercolorbox}[wd = \paperwidth]{footline}
        \vskip1cm
        \hskip1.5cm
        \includegraphics[scale = 1.5]{imagenes/logo_iteso_2}
        \vskip1cm
    \end{beamercolorbox}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block begin}
{
  \setbeamercolor{itemize item}  {fg = block title.bg}
  \setbeamercolor{item projected}{fg = block title.fg, bg = block title.bg}
  \setbeamercolor{description item}{fg = structure}

  \begin{beamercolorbox}[ht = 3.2 ex, dp = 1.3 ex,
                         leftskip = 2 ex, rightskip = 2 ex]{block title}

        \usebeamerfont*{block title}
        \insertblocktitle
        
    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 1 ex,
                           rightskip = 1 ex,
                           vmode]
                          {block body}

        \usebeamerfont{block body}
        \vskip2ex
        \begin{minipage}{\textwidth-2ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
             
}


\setbeamertemplate{block end}
{
  \end{minipage}
  \vskip0.2ex
  \end{beamercolorbox}
  \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block highlighted begin}
{
    \setbeamercolor{itemize item}  {fg = block title highlighted.bg}
    \setbeamercolor{item projected}{fg = block title highlighted.fg,
                                    bg = block title highlighted.bg}
    \setbeamercolor{description item}{fg = structure}

    \begin{beamercolorbox}[ht        = 3.2 ex,
                           dp        = 1.3 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex]
                          {block title highlighted}

        \usebeamerfont*{block title highlighted}
        \insertblocktitle

    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex,
                           vmode]
                          {block body highlighted}

        \usebeamerfont{block highlighted body}
        \vskip2ex
        \begin{minipage}{\textwidth-4ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
}


\setbeamertemplate{block highlighted end}
{
        \end{minipage}
    \vskip0.2ex
    \end{beamercolorbox}
    \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block alerted begin}
{
    \setbeamercolor{itemize item}  {fg = block title alerted.bg}
    \setbeamercolor{item projected}{fg = block title alerted.fg,
                                    bg = block title alerted.bg}
    \setbeamercolor{description item}{fg = structure}

    \begin{beamercolorbox}[ht        = 3.2 ex,
                           dp        = 1.3 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex]
                          {block title alerted}

        \usebeamerfont*{block title alerted}
        \insertblocktitle

    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex,
                           vmode]
                          {block body alerted}

        \usebeamerfont{block body alerted}
        \vskip2ex
        \begin{minipage}{\textwidth-4ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
}


\setbeamertemplate{block alerted end}
{
        \end{minipage}
    \vskip0.2ex
    \end{beamercolorbox}
    \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\enumitem}[1]
{
    \leavevmode\unskip
    \hbox
    {%
        \usebeamerfont*{item projected}%
        \usebeamercolor[bg]{item projected}%
        \vrule width2.25ex height1.85ex depth.4ex%
        \hskip-2.25ex%
        \hbox to2.25ex
        {%
            \hfil%
            \color{fg}#1%
            \hfil
        }%
    }%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\pgfpagesdeclarelayout{resize and center}
{
    \def\pgfpageoptionborder{0pt}
}
{
    \pgfpagesphysicalpageoptions
    {
        logical pages   = 1,
        physical height = \pgfpageoptionheight,
        physical width  = \pgfpageoptionwidth
    }
    \pgfpageslogicalpageoptions{1}
    {
        resized width  = \pgfphysicalwidth,
        resized height = \pgfphysicalheight,
        border shrink  = \pgfpageoptionborder,
        center         = \pgfpoint{.5\pgfphysicalwidth}{.5\pgfphysicalheight}
    }
}


\ifdefstring{\iteraposter@size}{a4paper}{}
{
    \pgfpagesuselayout{resize and center}[\iteraposter@size,
                                          \iteraposter@orientation]
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\endinput