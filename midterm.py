
from typing import List, Tuple, Any, Dict

# Part a to d

def malbrough(spec: List[Tuple[str, str]]) -> List[str]:
    return gen_lyrics(spec, description_malbrough)

def print_lyrics(lines: List[str]) -> None:
    for s in lines:
        print(s)

def lorraine(spec: List[Tuple[str, str]]) -> List[str]: # arguments tbd
    return gen_lyrics(spec, description_lorraine)
    

def pied_mariton(spec: List[Tuple[str, str]]) -> List[str]: # arguments dbd
    return gen_lyrics(spec, description_piedMariton)

def gen_lyrics(spec: List[Tuple[str]], description: Dict[str, Any]) -> List[str]: # arguments tbd
    spec = crosslink_verses_tupples(spec, description)
    # Encode the template
    li: List[str] = []
    for vers_tupple in spec:
        generator: 'Lyrics_Generator' = Lyrics_Generator(description["vers_template"])
        generator.encode_repetition()
        generator.fill_list_in(vers_tupple)
        generator.fill_phrases_in(vers_tupple)
        li += generator.get_as_list()
    return li

def crosslink_verses_tupples(spec: List[Tuple[str]], description: Dict[str, Any]) -> List[Tuple[str]]:
    crosslink_dict: Dict[str, int]
    for crosslink_dict in description["crosslinking verses"]:
        if crosslink_dict["from_vers_pos"] == 0: # add the whole tupple
            for verse_nr, verse_tupple in enumerate(spec):
                if verse_nr + crosslink_dict["from_vers"] >= 0: # the verse reffered to exists
                    spec[verse_nr] += spec[verse_nr + crosslink_dict["from_vers"]]
        else: 
            for verse_nr, verse_tupple in enumerate(spec):
                if len(verse_tupple) < crosslink_dict["insert_as"]: # if there'se no verse where we would insert the linked one (not overwriting)
                    crosslinked_str = spec[verse_nr + crosslink_dict["from_vers"]][crosslink_dict["from_vers_pos"]-1] # get the element refered to: -1 corrects the start at 1 in the dict
                    spec[verse_nr] += (crosslinked_str, )
    return spec

class Lyrics_Generator():
    def __init__(self, template: Any) -> None:
        self.template: str = template

    def encode_repetition(self) -> None:
        while True:
            start: int = self.template.find("{:")
            end: int = self.template.find(":}") + 2
            # return if no repetition was found
            if start == -1:
                return

            block: str = self.template[start:end]
            repetitions_content_separator: int = block.find(" ")+1
            number_of_repetitions: int = int(block[2:repetitions_content_separator])
            content: str = block[repetitions_content_separator:-3]
            self.template = self.template.replace(block, content * number_of_repetitions)

    def fill_phrases_in(self, phrases: Tuple[str]) -> None:
        # {x} tags
        for i in range(len(phrases)):
            template_section_to_replace: str = "{" + str(i+1) + "}"
            self.template = self.template.replace(template_section_to_replace, phrases[i])

    def fill_list_in(self, phrases: Tuple[str]) -> None:
        # deal with {[]} tags
        while True:
            start = self.template.find("{[")
            end = self.template.find("]}")
            if start == -1: # return if there are no {[]} tags
                return
            joining_string = self.template[start + 2: end]
            self.template = self.template.replace("{["+joining_string+"]}", joining_string.join(phrases))

    def get_as_list(self) -> List[str]:
        return self.template.split("\n")

# -------------------- Variabels -----------------------------------
# ------------------------------- Malbrough --------------------------------------------
template_malbrough = """
{1}
Miroton, mironton, mirontaine
{1}
{:3 {2} \n :}
"""

str_malbrough = [
    ("Malbroughs’enva-t-enguerre","Ne sait quand reviendra"), 
    ("Il reviendraz à Pâques","Ou à la Trinité"), 
    ("La Trinité se passe","Malbrough ne revient pas"),
    ("Madame à sa tour monte","Si haut qu’elle peut monter")
]

description_malbrough = {
    "vers_template": template_malbrough, # specifies the template to be used
    "crosslinking verses": [], 
    # specifies how strings between verses are connected. Nothing will be overwritten if there's already a string at insert_as.
}

# ------------------------------- Lorraine --------------------------------------------

template_lorraine = """
{2} avec mes sabots (bis)
{1}
Avec mes sabots, dondaine
Oh oh oh, avec mes sabots
"""

str_lorraine = [
("Rencontrai trois capitaines", "En passant par la Lorraine"),
("Ils m'ont appelée vilaine", ),
("Je ne suis pas si villaine", )

]

description_lorraine = {
    "vers_template": template_lorraine, # specifies the template to be used
    "crosslinking verses": [{"from_vers":-1, "from_vers_pos": 1, "insert_as":2}], # vers pos starts with 1
}

# ------------------------------- Pied Mariton --------------------------------------------

template_piedMariton = """
La Marie-Madeleine, elle a {1}
{[\n]}
Un pied mariton Madeleine, un pied mariton Madelon (bis)
"""

str_piedMariton = [
    ("un pied mariton", ), 
    ("une jambe de boué", ),
    ("un genoux cagneux", ),
    ("une cuisse de v'lours", ),

]

description_piedMariton = {
    "vers_template": template_piedMariton, # specifies the template to be used
    "crosslinking verses": [{"from_vers":-1, "from_vers_pos": 0, "insert_as":2}], # vers pos starts with 1, from vers pos = 0 => everything in the tupple
}

# ------------------------------ chevaliers de la table ronde ------------------------------

template_chevaliers = """
{1}
{2} {3}
{2}, oui oui oui
{2}, non non non
{2} {3}
"""

str_chevaliers = [
    ("Chevaliers de la table ronde", "Goûtons voir", "si le vin est bon"),
    ("S'il est bon, s'il est agréable", "J'en boirai", "jusque à mon plaisir"),
    ("J'en boirai cinq à six bouteilles", "Une femme", "sur mes genoux")]

description_chevaliers = {
    "vers_template": template_chevaliers, # specifies the template to be used
    "crosslinking verses": [], # vers pos starts with 1, from vers pos = 0 => everything in the tupple
}

# ------------------------- l'empereur sa femme et le petit prince ---------------------
template_prince = """
{1} matin,
L’empereur, sa femme et le p’tit prince
Sont venus chez moi, pour me serrer la pince.
Comme j’étais parti,
Le p’tit prince a dit :
« Puisque c’est ainsi, nous reviendrons {2}. » 
"""

str_prince = [
    ("Lundi", ), 
    ("Mardi", ), 
    ("Mercredi", ), 
    ("Jeudi", ), 
    ("Vendredi", ), 
    ("Samedi", ), 
    ("Dimanche", "plus"), 
]

description_prince = {
    "vers_template": template_prince, # specifies the template to be used
    "crosslinking verses": [{"from_vers":1, "from_vers_pos": 1, "insert_as":2}], # vers pos starts with 1, from vers pos = 0 => everything in the tupple
}


if __name__ == "__main__":
    #res = malbrough(str_malbrough)
    #res = lorraine(str_lorraine)
    #res = pied_mariton(str_piedMariton)
    #res = gen_lyrics(str_chevaliers, description_chevaliers)
    res  = gen_lyrics(str_prince, description_prince)
    print_lyrics(res)

    