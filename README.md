## JICK_DIR_BUSTER


## General information

This is a command-line script written in Python that brute-forces website directory and file paths.
This is to find website directories or file paths that are accessible, which shouldn't be.

Use [Jick](https://www.github.com/TheBlueNightmare/Jick) to crawl the targeted website.
The output file from the Jick crawler is used as the input for this directory buster to generate a comprehensive
list of URLs and then it brute-forces them, finding all URLs that can be browsed to.

This script also comes with several files in it, which contain common directory names or filenames that may
be sensitive. These file lists, in combination with the crawled URLs that were output by Jick, are used to
generate the list of visited URLs in the directory-busting process.

You can add, subtract, or edit these file lists as you want.

Jick also generates variations of the filenames and directory names that it uses. E.g it tries all filenames
in all capitalized letters, all lowercase letters, the first letter capitalized and the rest lowercase. It tries
every file in the filelist with all the different file extensions listed in the file extensions list, e.t.c.

## Usage

``
python dir_buster.py
``


By default, this will read from a targets.txt file in the same directory. To use a different input file, use:


``
python dir_buster.py --target-file target_list.txt
``

Remember that the target list file is the list of crawled URLs (presumably output by Jick), and it will look something like this:

``
GET https://www.example.com/

GET https://www.example.com/nowhere/

POST https://www.example.com/nowhere/again/
``

So if you want to use another tool like Jick, just make sure it follows that same format. Although the "GET" and "POST" at the beginning of
the lines in the file don't need to be there. Just make sure that the rest of the lines of the file are URLs.

By default, this directory buster will read from local filenames that are hardcoded into it. However, you can override these filenames to make
it read from different files, if you want. E.g


``
python dir_buster.py --dynamic-directories new_dynamic_directories_file.txt
``


or


``
python dir_buster.py --dynamic-files new_dynamic_files_file.txt
``


or


``
python dir_buster.py --dynamic-file-extensions new_dynamic_file_extensions.txt
``

or


``
python dir_buster.py --static-files new_static_files.txt
``


Just look at what each local file does, and it is pretty easy to figure out what the different files are used for.

Use the:

``
--deny-cookies
``

argument to make the program not store/transmit cookies as it does its thing.

Use:

``
--output output.txt
``

to change the output file.

When filtering results, this tool can use 3 criteria: the HTTP response status code, an xpath query performed on the returned HTML, or a regular expression search performed on the returned HTML.
By default, none of these filters are applied. And so you must apply at least 1 of them, or you will always get absolutely no results, even if some visited URLs were discovered. The tool needs to
know how to decide on which visited URLs were actually successfully visited, and so you must specify at least 1 of these 3 options.

You can use:

``
python dir_buster.py --status-code 200
``

or
``
python dir_buster.py --xpath //body/pre/a
``

or
``
python dir_buster.py --regex what.ver
``

As some examples. Then, any visited URL that matches the assigned status code, xpath query, or regular expression will be put into the output file.


## Credit
--------

This project was made by VyperLabs at [https://www.securityandpentesting.org/](https://www.securityandpentesting.org/)
