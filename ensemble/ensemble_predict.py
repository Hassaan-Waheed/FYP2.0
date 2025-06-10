from typing import Union

# Placeholder: Ensemble model outputs

def ensemble_predict(score_t: Union[float, int], score_x: Union[float, int], score_s: Union[float, int]) -> float:
    return 0.4*score_t + 0.3*score_x + 0.3*score_s

if __name__ == "__main__":
    print(ensemble_predict(0.8, 0.6, 0.7)) 