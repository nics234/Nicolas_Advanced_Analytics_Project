import hdbscan
import numpy as np
import pandas as pd

def approximator(processed_data:pd.DataFrame, testdata:list) -> int:
    """Function which uses the hdbscan-algorithm to detect clusters in the data.
    Afterwards the cluster for one seller can be predicted.

    Parameters
    __________
    processed_data:pd.DataFrame
        Dataframe that contains metadata about the orders

    testdata:list
        List that contains metadata for one specific seller, for whom the cluster should be predicted.

    Returns
    ----------
    test_labels:int
        Integer that represents the cluster to which the seller belongs."""
    processed_data_npy = np.array(processed_data)

    clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.2, approx_min_span_tree=True,
                                gen_min_span_tree=False, leaf_size=35, cluster_selection_method='eom',
                                metric='euclidean', min_cluster_size=15, min_samples=10, p=None,
                                prediction_data=True).fit(processed_data_npy)

    test_labels, strengths = hdbscan.approximate_predict(clusterer, testdata)
    test_labels = test_labels[0]
    return test_labels

def seller_classifier(selected_datapoint:int) -> None:
    """For the cluster that was detected, specific information about key characteristics will be given.

    Parameters
    ___________
    datapoint:int
        Integer that represents the cluster, the seller belongs to.

    Returns
    __________
    [print Output]
        Statements that show the key characteristics of each the seller cluster."""
    if selected_datapoint == -1:
        print("\nThis seller probably belongs to cluster 1.\nThey are selling more complex products that require a detailed product description and many pictures.\nBecause of maybe custom made solutions the products usually have a very high delivery_duration.\nNonetheless the sellers in this cluster average the moste revenue per order from all our sellers.")
    elif selected_datapoint == 0:
        print("\nThis seller probably belongs to cluster 2.\nThis cluster is said to contain our newcomers since they have not handled many orders just yet.\nBut they are keen on delivering a pleasent customer service through short delivery times and qucik review responses.")
    else:
        print("\nThis seller probably belongs to cluster 3.\nThe sellers are focused on very easy, self-explanatory products. Therefore they usually keep the product description length as well as the amount of pictures relatively low.\nBecause of the basic product-design, also the average price is very low.\nThis group of sellers evens this out by handling more orders than other sellers.")