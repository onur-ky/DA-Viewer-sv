import pandas as pd

def get_features(data, evalue_threshold=0, include_na_eval=False, cutoff=0.5):
    features = {}
    for protein in data.values():
        for feature, tools in protein.items():
            if tools and feature != 'length':
                for feature_type in tools:
                    feature_type = 'seg_LCR' if feature_type == 'seg_low_complexity_regions' else feature_type
                    if feature_type not in features:
                        features[feature_type] = 1
                    else:
                        features[feature_type] += 1
    features = {key: val/len(data) for key, val in features.items()}
    return features


def coverage_df_gen(data):
    prevalences = get_features(data)
    data_dict = {}
    proteins = []
    for p,anno in data.items():
        proteins.append(p)
        for tool, instances in anno.items():
            plength = anno['length']
            if tool != 'length':
                for domain, val in instances.items():
                    domain = 'seg_LCR' if domain == 'seg_low_complexity_regions' else domain
                    if domain not in data_dict:
                        data_dict[domain] = []
                    coverage = 0.0
                    prev_instance = None
                    for i in val['instance']:
                        if prev_instance:
                            if prev_instance[1] > i[0]:
                                coverage += (i[1] - prev_instance[1])/plength
                            else:
                                coverage += (i[1] - i[0])/plength
                        else:
                            coverage += (i[1] - i[0])/plength
                        prev_instance = i
                    data_dict[domain].append((p,coverage))
    
    for v in data_dict.values():
        add_to_v = []
        for p in proteins:
            if p not in [i[0] for i in v]:
                add_to_v.append((p,0.0))
        v += add_to_v
        v.sort(key=lambda x: x[0])
    
    
    df_dict = {k: [i[1] for i in v] for k,v in data_dict.items() if prevalences[k] >= 0.05}
    df = pd.DataFrame(df_dict)
    return df