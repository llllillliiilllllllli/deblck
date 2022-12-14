from typing import Any, List, Tuple 
import inspect 
import re 
import Features

def collect_features(*args, **kwargs) -> List[Tuple[Any, Any]]: 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    features = []
    for _, pack in inspect.getmembers(Features, inspect.ismodule):
        for _, mdl in inspect.getmembers(pack, inspect.ismodule):
            if re.search(r"Feature", mdl.__name__):
                for _, cls in inspect.getmembers(mdl, inspect.isclass):
                    for _, funct in inspect.getmembers(cls, inspect.isfunction):
                        features.append((cls, funct))
    
    return features
