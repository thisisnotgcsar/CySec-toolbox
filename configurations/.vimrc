" Disable compatibility with vi which can cause unexpected issues.
set nocompatible

" Enable type file detection. Vim will be able to try to detect the type of file in use.
filetype on

" Turn syntax highlighting on.
syntax on

" Add numbers to each line on the left-hand side.
set relativenumber

" Set tab width to 4 columns.
set tabstop=4

" use tab characters instead of spaces
set noet

" > indentation is 1 tab
set shiftwidth=4

" the name says it all
set smartindent

" Do not wrap lines. Allow long lines to extend as far as the line goes.
set nowrap

" Enable auto completion menu after pressing TAB.
set wildmenu

" Make wildmenu behave like similar to Bash completion.
set wildmode=list:longest
