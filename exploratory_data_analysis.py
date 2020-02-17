import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns


def initialize_percent_success(portfolio,
                               clean_data):
    """ Initializes a DataFrame that describes the success percentage for
    each offer
    
    INPUT:
        portfolio: DataFrame containing offer ids and meta data about 
                   each offer (duration, type, etc.)

        clean_data: DataFrame that characterizes the effectiveness of
                    customer offers
    
    OUTPUT:
        percent_success: DataFrame that describes the success percentage for
                         each offer"""
    successful_count =\
        clean_data[['offerid',
                    'offersuccessful']].groupby('offerid').sum().reset_index()

    offer_count = clean_data['offerid'].value_counts()

    offer_count = pd.DataFrame(list(zip(offer_count.index.values,
                                        offer_count.values)),
                               columns=['offerid', 'count'])

    successful_count = successful_count.sort_values('offerid')

    offer_count = offer_count.sort_values('offerid')

    percent_success = pd.merge(offer_count, successful_count, on="offerid")

    percent_success['percentsuccess'] =\
        100 * percent_success['offersuccessful'] / percent_success['count']

    percent_success = pd.merge(percent_success,
                               portfolio,
                               on="offerid")

    percent_success = percent_success.drop(columns=['offersuccessful'])

    percent_success = percent_success.sort_values('percentsuccess',
                                                  ascending=False)

    return percent_success.reset_index(drop=True)
