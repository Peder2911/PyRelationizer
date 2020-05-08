
import pandas as pd

def getRelations(dataset,uoas)->[(pd.DataFrame,bool)]:
    relations = []

    for identifier,variables in uoas.items():
        rel = relationize(dataset,identifier,variables)
        if len(set(rel[identifier].values)) < rel.shape[0]:
            rel = getDuplicates(rel,identifier)
            relations.append((rel,False))
        else:
            relations.append((rel,True))

    return relations

def getDuplicates(relation, identifier):
    duplicatedIds = relation[identifier][relation[identifier].duplicated()].values
    return relation[relation[identifier].apply(lambda x: x in duplicatedIds)]

def relationize(dataset,identifier,variables):
    sub = dataset[[identifier, *variables]]
    sub = sub.drop_duplicates()
    return sub
