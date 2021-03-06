import pandas as pd
import re

def cocitation_dataframe():
    '''
    Input: Cocitation Xenopus .txt file from Xenbase in which genes and their cocitations are seperated by "\t".
    The cocitated genes are seperated by ",".
    The information on the cocited gene contains: XenBase ID, gene symbol and cocitation frequency (seperated by ":").    
    
    Process: Retrieves the Xenopus cocitation .txt file from Xenbase and produces a pandas dataframe. 
    
    Output:
    -------------
    Pandas Dataframe with the following format:
    
    Gene    Co-gene    Association    Frequency
    A       X                1          int
    B       Y                1          int
    C       Z                1          int
    
    
    '''
    # Load the file containing genes with their cocitations as pandas dataframe
    filename = 'ftp://ftp.xenbase.org/pub/GenePageReports/GenePageInteractants.txt'
    df = pd.read_csv(filename, sep='\t,', index_col=False, na_filter=False, header=None, engine='python')
    
    df = df[0].str.split("\t", expand=True)  # Split strings on tab and make seperate columns
    df = df[df[2].notnull()]  # Only keep genes that have been cocited with at least one gene
    df[2] = df[2].str.split(r',\s*(?![^()]*\))')  # Split the cocited genes at the comma
    df.index = range(0, len(df))  # Re-index the dataframe, from 0 to length of dataframe

    co_dict = {}  # Make an empty dictionary to store a dictionary per row, containing the cocited genes
    for row in range(0, len(df)):  # For every row in the cocotation dataframe...
        row_dict = {}  # produce a dictionary (for every row in the cocitation dataframe)
        for gene_no in range(0, ((len(df[2][row]))-1)):  # For every position of cocited genes
            row_dict[gene_no] = df[2][row][gene_no]  # Make the position a key and the gene the value
        for key in row_dict:  # For every key in the cocitated genes dictionary
            # split the value at the ":", making the XB-ID, gene name and frequency seperate items
            row_dict[key] = re.split(r':\s*(?![^()]*\))', row_dict[key])
        # Each row of the cocitation df forms a dictionary key 
        # Within this key, a dictionary is stored in which every cocited gene of this row's gene is accessible
        # through its position - the position of the cocited gene forms the key
        co_dict[row] = row_dict 

    # Make three empty lists that will form the columns of a reference dataframe 
    # in which cocited genes are stored with their frequency
    gene_list = []  # Make a list to store the first gene of the gene pairs
    pair_list = []  # Make a list to store the second gene of the gene pairs
    frequency_list = []  # Make a list to store the cocitation frequency of the gene pairs
    for pos in range(len(df)):  # For each position in the cocitation_df, thus for each gene that has a cocitation
        for pair in co_dict[pos]:  # For each cocited gene stored in the dictionary
            gene_list.append(df[1][pos])  # Store the gene as often in the gene list as it has cocitated genes
            info_list = list(co_dict[pos][pair])  # The info list contains the value list of each cocited gene
            if info_list[1] == 'mg': # mg is seperated from the rest of the name by a ":", giving string seperation problems
                info_list[1] = info_list[1] + ':' + info_list[2]
                info_list.pop(2)
            pair_list.append(info_list[1])  # Store the gene name of the cocited gene
            frequency_list.append(int(info_list[2]))  # Store the frequency of the cocitation
    
    # Put all the retrieved information in a dataframe
    cocit_df = pd.DataFrame()
    cocit_df['Gene'] = gene_list
    cocit_df['Co-gene'] = pair_list
    cocit_df['Association'] = [1] * (len(cocit_df))
    cocit_df['Frequency'] = frequency_list
    
    return cocit_df

validation_network = cocitation_dataframe()
