#!/usr/bin/env python

# this package needs a setup.sh 
# and also a requirements file
# to set up the calender.sty
# use my library stuff for the setup

import calendar
import argparse
import glob
import os
import sh
import mypymod.jinja2tex as j2x

# add arguments to the mypymod.argparsers

def my_args():
    des='''
    Enter year and month as integer
    to generate a A4 month calender page
    '''
    parser = argparse.ArgumentParser(description=des)
    parser.add_argument('-y', '--year', metavar='', type=int, help='is integer', required=True)
    parser.add_argument('-m', '--month', metavar='', type=int, help='is integer', required=True)
    return parser.parse_args()

# this multiline string should be in a seperate file
# if tempate arguments are passed over a dictionary
# the whole function can be generic
def monthly_calendar(year, month):
    first_monthday, monthdays = calendar.monthrange(year, month)
    monthname = calendar.month_name[month]
    tex = r"""
\documentclass[landscape,a4paper]{article}
\usepackage{calendar}
\usepackage[landscape,margin=0.5in]{geometry}
\begin{document}
\pagestyle{empty} 
\noindent
\StartingDayNumber=2
\begin{center}
\textsc{\LARGE \VAR{monthname}}\\
\textsc{\large \VAR{year}}
\end{center}
\begin{calendar}{\hsize}
\BLOCK{ for i in range(first_monthday)}
\BlankDay
\BLOCK{ endfor }
\setcounter{calendardate}{1}
\BLOCK{ for i in range(monthdays)}
\day{}{\vspace{2cm}}
\BLOCK{ endfor }
\finishCalendar
\end{calendar}
\end{document}
    """
    template = j2x.env.from_string(tex).render(year=year, month=month, monthname=monthname, monthdays=monthdays, first_monthday=first_monthday)
    with open("{}_{:02d}".format(year, month), 'w') as f:
        f.write(template)
        f.seek(0)
        sh.pdflatex(f.name)
        sh.rm(glob.glob("./{}".format(f.name)), glob.glob("./{}.[la]*".format(f.name)))

if __name__ == "__main__":
    args = my_args()
    monthly_calendar(args.year, args.month)
