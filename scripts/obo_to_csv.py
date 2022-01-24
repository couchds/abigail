import argparse


def line_requires_direct_extraction(line):
    """ The value extracted from these tags are simply the value itself.
    
    Params:
    @line (str): The line of the file that is being processed
    """
    DIRECT_EXTRACTION_TAGS = (
        "id",
        "name",
        "def",
        "namespace"
    )
    for tag in DIRECT_EXTRACTION_TAGS:
        if line.startswith(f'{tag}:'):
            return True
    return False

def extract_value_from_line(file_line):
    """ From an OBO tag-value pair, return the value that will be stored in
    the Neo4j database. The rule for how to extract this value depends on
    the tag that we are on.

    In addition, returns a boolean indicating if the line required direct extraction
    or not.

    Params:
    @file_line (str): The line of the file that is being processed
    """
    if line_requires_direct_extraction(file_line):
        return file_line.split(': ')[1].replace('"', ''), True
    if file_line.startswith('synonym:'):
        return file_line.split('"')[1], False
    return None, None

def create_new_file(file_name, file_headers):
    """ Create a new file that has a single row with the column headers.

    Params:
    @file_name (str): The name of the file
    @file_headers (list): The column headers of the file
    """
    with open(file_name, 'w') as outfile:
        outfile.write('\t'.join(file_headers)+'\n')

def perform_write_row(file_name, wrow, synonyms):
    """ Write row representing a Neo4j node to the output file.

    Params:
    @file_name (str): The file that the row is being written to
    @wrow (list): The contents of the row, excluding the synonyms
    @synonyms (list): The synonyms for the node
    """
    with open(file_name, 'a') as outfile:
        outfile.write('\t'.join(wrow)+'\t'+','.join(synonyms)+'\n')

def convert_obo_to_csv(infile, outfile_name):
    """ Convert an OBO file to a CSV file.

    Params:
    @infile (file): The OBO file to convert
    @outfile_name (str): The name of the output CSV file that will be created
    """
    on_new_term = False # this is set to true whenever we are on a new term
    active_write_row = [] # the row actively being written, emptied each time we are on a new term
    active_row_synonyms = [] # tracks the synonyms for the row being written
    for line in infile:
        line = line.strip()
        on_new_term = (line == '[Term]')
        if on_new_term:
            perform_write_row(outfile_name, active_write_row, active_row_synonyms)
            active_write_row = []
            active_row_synonyms = []
            on_new_term = False
        else:
            value, is_direct = extract_value_from_line(line)
            if is_direct:
                active_write_row.append(value)
            elif is_direct is False:
                active_row_synonyms.append(value)
            else:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts an OBO file to a CSV file.')
    parser.add_argument('--infile', required=True)
    parser.add_argument('--outfile', required=True)
    parser.add_argument('--cols', required=True)
    args = parser.parse_args()
    input_file_name = args.infile
    output_file_name = args.outfile
    cols = args.cols.split(',')

    create_new_file(output_file_name, cols)
    with open(input_file_name, 'r') as infile:
        convert_obo_to_csv(infile, output_file_name)