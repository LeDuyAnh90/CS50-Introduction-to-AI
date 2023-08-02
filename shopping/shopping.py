import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    data_type = {
        ('Administrative', 'Informational', 'ProductRelated', 'Month', 'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'VisitorType', 'Weekend') : int,
        ('Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay') : float
        }

    month = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

    with open(filename) as f:
        content = list(csv.reader(f, delimiter=','))
        evidence = []
        labels = []
        for i in range(1,len(content)):
            # convert 'month' 
            content[i][10] = month[content[i][10]]
            # convert 'VisitorType'
            content[i][15] = 1 if content[i][15] == 'Returning_Visitor' else 0
            # convert 'Weekend'
            content[i][16] = 1 if content[i][16] == 'TRUE' else 0
            # convert 'revenue'
            content[i][17] = 1 if content[i][17] == 'TRUE' else 0
            # convert data type
            col_index = {c:i for c,i in zip(content[0],range(len(content[0])))}
            for col in col_index:
                for cols in data_type:
                    if col in cols:
                        content[i][col_index[col]] = int(content[i][col_index[col]]) if data_type[cols] == int else float(content[i][col_index[col]])
            # creat results
            evidence.append(content[i][:16])
            labels.append(content[i][17])
        results = tuple((evidence,labels))
    return results
    # raise NotImplementedError

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # raise NotImplementedError
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence,labels)
    return neigh

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    true_negative = 0
    for i in range(len(labels)):
        if labels[i] == 1 and predictions[i] == 1:
            true_positive += 1
        elif labels[i] == 0 and predictions[i] == 0:
            true_negative += 1
    sensivity = true_positive/sum(labels)
    specitivy = true_negative/len([i for i in labels if i ==0])
    return sensivity,specitivy
    # raise NotImplementedError


if __name__ == "__main__":
    main()
