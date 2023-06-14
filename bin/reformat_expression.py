# coding: utf-8

# In[1]:

import pandas as pd
import sys
import getopt


###############################################################################
#                               MAIN
###############################################################################
if __name__ == "__main__":
    usage = '''
    %s -e <expression file> -s <specimen> -E <expr out>
    ''' % (sys.argv[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:E:s:h")
    except getopt.GetoptError:
        sys.exit(str(getopt.GetoptError) + usage)

    expression_file = None
    expr_output = None
    specimen_file = None
    for o, a in opts:
        if o == '-e':
            expression_file = a
        elif o == '-E':
            expr_output = a
        elif o == '-s':
            specimen_file = a
        else:
            sys.exit(usage)
    if not(expression_file and expr_output and specimen_file):
        sys.exit(usage)

    specimens = pd.read_csv(specimen_file, sep='\t', header=0,
                            usecols=['icgc_specimen_id', 'specimen_type'])
    tumor_specimens = [row[1]['icgc_specimen_id']
                       for row in specimens.iterrows() if
                       not row[1]['specimen_type'].startswith('Normal')]

    import os
    expression_dict = {}
    if os.stat(expression_file).st_size:
        expression = pd.read_csv(expression_file, sep=' ',
                                 names=['gene_id', 'donor', 'project',
                                        'specimen', 'sample', 'icgc_sample',
                                        'submitted_sample', 'gene_model',
                                        'norm_read_count', 'raw_read_count',
                                        'FC', 'assembly', 'platform',
                                        'total_read_count', 'protocol',
                                        'alignment', 'normalization',
                                        'other_analysis', 'strategy',
                                        'repository', 'accession',
                                        'ref_sample_type'])

        for row in expression.iterrows():
            if row[1]['specimen'] in tumor_specimens:
                cat = row[1]['donor']
                if not cat in expression_dict:
                    expression_dict[cat] = {}
                expression_dict[cat][row[1]['gene_id']] = row[1]['norm_read_count']
    df = pd.DataFrame.from_dict(expression_dict)
    df.to_csv(expr_output, sep='\t', index=True)
