"""Functions to write html"""
import os.path
import json


def adjustHeaders(head, available_badges):
    # Define the opening and closing tags for table head
    opening_tag = '<table id="highscoretable">'
    closing_tag = "</thead>"

    # Find the start and end indexes of the table head section
    start_index = head.find(opening_tag) + len(opening_tag)
    end_index = head.find(closing_tag, start_index)

    # Extract the table head section
    table_head = head[start_index:end_index]

    # Split the table head into individual table headers
    table_headers = table_head.split("<th")

    # Prepare the updated table head with the initial header format
    updated_table_head = '<th style="width:0.1">\n<p>Library</p>\n</th>'

    # Adjust the width and add the remaining valid table headers
    for header in table_headers[1:]:  # Skip the initial header
        header_start_index = header.find("<p>") + len("<p>")
        header_end_index = header.find("</p>", header_start_index)
        keyword = header[header_start_index:header_end_index]

        if keyword in available_badges:
            # Adjust the width by dividing it by the number of available badges
            width_index = header.find('style="width:') + len('style="width:')
            width_end_index = header.find('">', width_index)
            width = float(header[width_index:width_end_index])
            width /= len(available_badges)

            # Build the updated header string with adjusted width
            updated_header = f'<th style="width:{width}">\n<p>{keyword}</p>\n</th>'
            updated_table_head += updated_header

    # Combine the updated table head with the initial header and additional tags
    updated_head = (
        f"{opening_tag}\n  <thead>\n    <tr>\n{updated_table_head}</tr>\n  </thead>\n"
    )

    # Replace the original table head with the updated version
    updated_head += head[end_index:]

    return updated_head


def load_cache_file(filename):
    """Loads lines of code data from filename, stripping
    var_name from the front
    """
    ret_dict = {}
    try:
        with open(filename, "r") as filein:
            file_content = filein.read()
            # If there is a file but there are no hash entries inside i.e. the first time this functionality is run
            if len(file_content) == 0 or len(file_content.split("=")) == 1:
                return ret_dict
            try:
                jsontext = file_content.split("=")[1]
                ret_dict = json.loads(jsontext)
            except json.JSONDecodeError:
                raise json.JSONDecodeError
            except IndexError:
                raise IndexError
    except FileNotFoundError:
        pass

    return ret_dict


def make_html_file(package, jsfile, template_file="templates/loc_plot.html"):
    """Write Lines of Code information to html files of each library stored under /libraries/"""
    # create dir if not existing
    try:
        os.mkdir("loc/")
    except FileExistsError:
        pass

    with open(template_file, "r") as filein:
        template = filein.read()

    with_title = template.replace("PAGE_TITLE", str(package + " Lines of Code"))
    with_heading = with_title.replace(
        "CHART_HEADING", str(package + " Lines of Code vs Date")
    )
    with_data = with_heading.replace("PATH_TO_DATA", str("../" + jsfile))

    with open(str("loc/" + package + ".html"), "w") as fileout:
        fileout.write(with_data)


def write_to_js_file(data, fileout):
    """Write git hashes and date information to js files of each library stored under /libraries/"""
    outstring = str("var loc_data = " + json.dumps(data))
    with open(fileout, "w") as fileout:
        fileout.write(outstring)


def WriteCellWithLinkedImage(fileout, image=None, link=None, alt_text=None):
    """
    Write a cell to fileout with image and link
    if image is none it writes an empty cell
    """
    fileout.write("    <td>\n")
    if image is not None:
        fileout.write(str('      <a href="' + str(link) + '">\n'))
        fileout.write(
            str('        <img src="' + str(image) + '" alt="' + alt_text + '">\n')
        )
        fileout.write(str("      </a>\n"))
    fileout.write("    </td>\n")
