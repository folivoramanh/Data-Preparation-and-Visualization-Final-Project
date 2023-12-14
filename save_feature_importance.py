import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


def plot_feature_importance(feature_importance, features_per_subplot=30, show=False):
    """
    This function is used to plot the feature importance of a model.

    Parameters
    ----------
    feature_importance : pandas.DataFrame
        A dataframe containing the feature importance of a model.
    features_per_subplot : int, default=30
        The number of features to plot per subplot. 
        If the number of features exceeds this number, multiple subplots will be created.
    show : bool, default=False
        Whether to show the plot or not.

    Returns
    -------
    None
    """
    # Sort features based on their importance
    sorted_idx = feature_importance['Importance'].abs().argsort()[::-1]

    # Calculate the number of subplots needed
    num_subplots = int(np.ceil(len(sorted_idx) / features_per_subplot))

    # Create subplots
    _, axes = plt.subplots(num_subplots, 1, figsize=(
        10, 6 * num_subplots), sharex=True)

    # Plot each subplot
    for i in range(num_subplots):
        start_idx = i * features_per_subplot
        end_idx = (i + 1) * features_per_subplot
        current_features = feature_importance['Feature'][sorted_idx][start_idx:end_idx]
        current_importance = feature_importance['Importance'][sorted_idx][start_idx:end_idx]

        s = sns.barplot(x=current_importance, y=current_features,
                        ax=axes[i], palette=sns.color_palette("Blues_d", features_per_subplot)[::-1], hue=current_features)

        axes[i].invert_yaxis()
        if i == 0:
            xlabel = s.get_xticklabels()
        axes[i].set_yticks(range(len(current_features)))
        axes[i].set_xticklabels(xlabel)
        axes[i].set_yticklabels(current_features)
        axes[i].set_xlabel("Feature Importance")
        axes[i].invert_yaxis()
        axes[i].set_ylabel("Feature")
        axes[i].set_title(
            f"Top {(i)*features_per_subplot + 1} - {(i + 1)*features_per_subplot} Feature Importance")

    plt.tight_layout()
    plt.savefig('save.png')
    if show:
        plt.show()
