import csv


def escape_double_quotes(in_file, out_file):
    with open(in_file) as in_f:
        with open(out_file, 'w') as out_f:
            row = in_f.read()
            escaped_row = row.replace('"', r'\"')
            out_f.write(escaped_row)


def get_wrong_guess(in_file, out_file):
    # counter = 0
    wrong_guess = []
    with open(out_file, 'w') as out_f:
        with open(in_file) as in_f:
            f_tsv = csv.reader(in_f, delimiter='\t', escapechar='\\')
            for row in f_tsv:
                # counter += 1
                word, answer, guess = row
                if answer != guess:
                    out_f.write(row[0] + '\t' + row[1] + '\t' + row[2] + '\n')
                    wrong_guess.append(row)
    # print counter
    return wrong_guess


if __name__ == '__main__':
    # in_file, out_file = 'debug.txt', 'debug_esc.txt'
    # escape_double_quotes(in_file, out_file)

    in_file, out_file = 'debug_esc.txt', 'debug_wrong.txt'
    wrong_guess = get_wrong_guess(in_file, out_file)
    print len(wrong_guess)
