import pandas as pd

# read csv data
df = pd.read_csv('input.csv',sep=r'\s*,\s*', engine='python')

# final_values to given to dataframe 
final_values = []

# iterate rows one by one
for i, current_row in df.iterrows():
    # change the type of date column to date
    current_row['date'] = pd.to_datetime(current_row['date'],format='%d-%m-%Y')
    # values to store if value_overlayed before
    f_val_list = []
    # check if any value_overlayed before
    for j,inner_row in df.iterrows():
        # current value of element  
        t_val = current_row['value']
        # check for the same element
        if inner_row['element'] == current_row['element']:
            # change the type to date
            inner_row['date'] = pd.to_datetime(inner_row['date'],format='%d-%m-%Y')
            
            # days between current value and value overlayed before
            n = abs(current_row['date'] - inner_row['date']).days

            # check the date for past 12 months
            if inner_row['date'] < current_row['date'] :        
                # if value overlayed in past 12 months than append the value to list to calculate reversal value overlaying
                if inner_row['value_overlayed'] == 'Y':
                    if n < 365:    
                        f_val_list.append({'f_val':inner_row['value'],'n':n}) 

    '''
    If value_overlayed than consider base value - 150
    else calculate the formula
    '''
    if current_row['value_overlayed'] == 'Y':
        final_values.append(150)
    else:
        if f_val_list != []:
            f_val = f_val_list[0]
            final_value = t_val - ((f_val['f_val']-150)/365) * (365-f_val['n'])
            final_values.append(final_value)
        else:
            final_value = current_row['value']
            final_values.append(final_value)

df['final_value'] = final_values

pd.options.display.float_format = '{:,.2f}'.format

df.to_csv('result.csv', sep='\t', encoding='utf-8')

           