import libraries.controllers.file_controller as fc
import random

CHALLENGE_FOLDER_PATH = fc.SYSTEM_PATHS["challenges"]

def _get_path(parent, child):
    return fc.os.path.join(parent, child)

class ChallengeLayer:
    def __init__(self, layer: int):
        self.layer = layer
        self.challenge_layer_jsons = {
            1: _get_path(CHALLENGE_FOLDER_PATH, "layer1.json"),
            2: _get_path(CHALLENGE_FOLDER_PATH, "layer2.json"),
            3: _get_path(CHALLENGE_FOLDER_PATH, "layer3.json"),
            4: _get_path(CHALLENGE_FOLDER_PATH, "later4.json")
        }

        self.current_layer_json = None

        self._load()

    def get(self) -> dict:
        return fc.pull_data(self.current_layer_json)

    def _load(self) -> None:
        self.current_layer_json = self.challenge_layer_jsons[self.layer]

class Challenges:
    def __init__(self, layer: int):
        self.layer = layer
        LAYER_INSTANCE = ChallengeLayer(self.layer)
        self.LAYER_DATA = LAYER_INSTANCE.get()

        self.STATIC = self.LAYER_DATA["static"]
        self.DYNAMIC = self.LAYER_DATA["dynamic"]

    def get_starters(self) -> dict:
        if self.layer != 1:
            return None
        return self.STATIC["starter"]
    
    def _get_random_static(self, concept: str, amount=1) -> list[dict]:
        challenge_list = list(self.STATIC[concept].values())
        k_value = min(amount, len(challenge_list))
        return random.sample(challenge_list, k=k_value)
    
    def get_statics(self, amount=1) -> dict:
        """
        Returns a list of random static challenges
        amount arg sets the amount of challenges for each static concept
        """
        statics = {}
        for concept in self.STATIC:
            if concept == "starter":
                continue
            statics[concept] = self._get_random_static(concept, amount)

        return statics
    

if __name__ == "__main__":
    fc.initialize_system_folders()
    c = Challenges(1)

    print(c.get_statics(1))