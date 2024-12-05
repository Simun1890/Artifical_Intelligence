import csv
import sys
import math

#Učitavanje podataka iz csv dat
def load(train_file, test_file):
    X_train=[]
    y_train=[]
    X_test=[]
    y_test=[]
    #čitanje csv file-a
    def load_csv(file):
        with open(file, mode='r') as f:
            reader=csv.reader(f)
            #čitanje redak po redak
            data=[row for row in reader]
        #prvi redak su značajke
        header=data[0]
        #ostatak
        rows=data[1:]
        return header, rows

    #čitanje podataka za trening
    train_header, train_data=load_csv(train_file)
    #čitanje podataka za testiranje
    test_header, test_data=load_csv(test_file)
    for row in train_data:
        #značajke
        X_train.append(row[:-1])
        #labela
        y_train.append(row[-1])

    for row in test_data:
        #značajke testiranja
        X_test.append(row[:-1])
        #labele testiranja
        y_test.append(row[-1])


    return train_header, X_train, y_train, X_test, y_test

#Izračun entropije
def entropy(y):
    frequency={}
    for label in y:
        if label not in frequency:
            #Ako smo došli na novo pojavljivanje stvaranje nove
            frequency[label]=0
        #Ako postoji povećamo za jedan
        frequency[label]=frequency[label] + 1
    #Ukupni broj
    total_samples=len(y)
    entropy_value=0
    for label in frequency:
        probability=frequency[label] / total_samples
        #Sama entropija po formuli sa predavanja
        entropy_value=entropy_value - (probability * math.log2(probability))
    
    return entropy_value

#Izračun informacijske dobiti
def information_gain(X, y, feature_index):
    feature_values=[]
    unique_values=[]
    #Entorpija početak
    total_entropy=entropy(y)
    for x in X:
        #Stvaranje liste bez ponavljanja
        if(x[feature_index] not in feature_values):
            unique_values.append(x[feature_index])
        feature_values.append(x[feature_index])#Index značajke za koju računamo
    feature_entropy=0

    for value in unique_values:
        subset_y=[]
        for i in range(len(y)):
            if feature_values[i] == value:
                #samo trenutnte vrijednosti
                subset_y.append(y[i])
        #Entropija trenutne značajke
        feature_entropy=feature_entropy + ((len(subset_y) / len(y)) * entropy(subset_y))

        #Informacijska dobit
        i_gain=total_entropy - feature_entropy
    
    return i_gain

#Definicija klase ID3
class ID3:
    def __init__(self, max_depth=0):
        #Inicijalizacija stabla i max dubine
        self.tree=None
        self.max_depth=max_depth

    def fit(self, X, y, header):
        #Građenje stabla na temelju trening podataka
        self.tree=self._build_tree(X, y, header, depth=0)

    def _build_tree(self, X, y, header, depth):
        #Ako sve oznake pripadaju jednoj klasi, vrati tu klasu
        if(len(set(y)) == 1):
            return y[0]

        #Ako nema više značajki za razmatranje, vrati najčešću klasu
        if(len(X[0]) == 0):
            return max(set(y), key=y.count)
        
        #Ako smo dosegnuli maksimalnu dubinu, vrati najčešću klasu
        if (self.max_depth != 0 and depth >= self.max_depth):
            return max(set(y), key=y.count)
        
        #Izračunaj IG za sve značajke
        gains=[]
        for i in range(len(X[0])):
            gains.append(information_gain(X, y, i))
        
        #Odaberi najbolju značajku na temelju IG
        best_feature_index=gains.index(max(gains))
        best_feature=header[best_feature_index]
        tree={best_feature: {}}

        #Pronađi jedinstvene vrijednosti najbolje značajke
        unique_values=[]
        for x in X:
            if(x[best_feature_index] not in unique_values):
                unique_values.append(x[best_feature_index])
                    
        #Stvori podstabla za svaku vrijednost najbolje značajke
        for value in unique_values:
            subset_X=[]
            subset_y=[]
            for x in X:
                if(x[best_feature_index] == value):
                    a=x[:best_feature_index] + x[best_feature_index+1:]
                    subset_X.append(a)
            for i in range(len(y)):
                if(X[i][best_feature_index] == value):
                    subset_y.append(y[i])
            pom=header[:best_feature_index] + header[best_feature_index+1:]
            depth=depth+1
            subtree=self._build_tree(subset_X, subset_y, pom, depth)
            tree[best_feature][value]=subtree

        return tree

    def print_branches(self, tree=None, level=1, branch=""):
        #Ispiši grane stabla
        if(tree is None):
            tree=self.tree
            print("[BRANCHES]:")
        
        if(isinstance(tree, dict)):
            feature=list(tree.keys())[0]
            sorted_values=sorted(tree[feature].items(), key=lambda x: x[0])  # Sortiranje po abecedi
            for value, subtree in sorted_values:
                branch_details=f"{level}:{feature}={value}"
                pom_print=branch + " " + branch_details
                self.print_branches(subtree, level+1, pom_print)
        else:
            print(f"{branch} {tree}")

    def predict(self, X):
        #Predviđanje oznaka za skup podataka
        predictions=[]
        for instance in X:
            predictions.append(self.predict_instance(instance, self.tree))
        return predictions

    def predict_instance(self, instance, tree):
        if(isinstance(tree, dict)):
            feature = list(tree.keys())[0]
            value = instance[header.index(feature)]  # Pronalaženje indeksa značajke u zaglavlju
            if(value in tree[feature]):
                return self.predict_instance(instance, tree[feature][value])
            else:
                #Ako nema odgovarajuće vrijednosti za značajku, predviđamo najčešću klasu u tom čvoru
                counts = []
                for v in tree[feature].values():
                    if(isinstance(v, dict)):
                        counts.extend(self.collect_labels(v))
                    else:
                        counts.append(v)
                return max(set(counts), key=counts.count)
        else:
            return tree

#Funckija točnosti
def accuracy(y_true, y_pred):
    correct=0
    for true, pred in zip(y_true, y_pred):
        if(true == pred):
            correct=correct+1
    total=len(y_true)
    acc=correct/total
    return acc

#Funkcija stvaranja matrice zabune
def confusion_matrix(y_true, y_pred):
    #Stvaranje rječnika za praćenje broja pojavljivanja kombinacija
    matrix={}
    for true, pred in zip(y_true, y_pred):
        if(true not in matrix):
            matrix[true]={}
        if(pred not in matrix[true]):
            matrix[true][pred]=0
        matrix[true][pred]=matrix[true][pred]+1
    
    # Sortiranje vrijednosti ciljne varijable abecedno
    labels=sorted(set(y_true + y_pred))

    return labels, matrix

#Funckija ispisa matrice zabune
def print_confusion_matrix(labels,matrix):
    
    print("[CONFUSION_MATRIX]:")
    for true_label in labels:
        row=[]
        for pred_label in labels:
            count=matrix.get(true_label, {}).get(pred_label, 0)
            row.append(str(count))
        print(" ".join(row))


if __name__ == "__main__":
    #file za trening
    train_file_path=sys.argv[1]
    #file za testiranje
    test_file_path=sys.argv[2]
    #ako postoji parametar za dubinu
    if (len(sys.argv) > 3):
        #spremi ga
        max_depth=int(sys.argv[3])
    else:
        #ako ne postavi na None
        max_depth=0

    #učitavanje podataka sa funkcijom
    header, X_train, y_train, X_test, y_test=load(train_file_path, test_file_path)

    #inicijalizacija modela
    model=ID3(max_depth=max_depth)
    model.fit(X_train, y_train, header[:-1])
    
    model.print_branches()

    predictions=model.predict(X_test)
    print("\n[PREDICTIONS]:", " ".join(predictions))

    # Izračunaj točnost modela
    acc=accuracy(y_test, predictions)

    # Ispiši točnost
    print(f"[ACCURACY]: {acc:.5f}")

    # Izračunaj matricu zabune
    labels,matrix=confusion_matrix(y_test, predictions)

    #Ispis matrice zabune
    print_confusion_matrix(labels,matrix)
