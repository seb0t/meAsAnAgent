from .registry import registry

@registry.register(category="conversion")
def kilometers_to_miles(
    kilometers: float
    ) -> dict:
    """
    Descrizione: Funzione utile per convertire chilometri in miglia.
    Args:
        kilometers: La distanza in chilometri.
    Returns:
        Un dizionario contenente la distanza convertita in miglia.
    """
    miles = kilometers * 0.621371
    return {"result": miles}

@registry.register(category="conversion")
def miles_to_kilometers(
    miles: float
    ) -> dict:
    """
    Descrizione: Funzione utile per convertire miglia in chilometri.
    Args:
        miles: La distanza in miglia.
    Returns:
        Un dizionario contenente la distanza convertita in chilometri.
    """
    kilometers = miles / 0.621371
    return {"result": kilometers}

@registry.register(category="conversion")
def kilograms_to_pounds(
    kilograms: float
    ) -> dict:
    """
    Descrizione: Funzione utile per convertire chilogrammi in libbre.
    Args:
        kilograms: Il peso in chilogrammi.
    Returns:
        Un dizionario contenente il peso convertito in libbre.
    """
    pounds = kilograms * 2.20462
    return {"result": pounds}

@registry.register(category="conversion")
def pounds_to_kilograms(
    pounds: float
    ) -> dict:
    """
    Descrizione: Funzione utile per convertire libbre in chilogrammi.
    Args:
        pounds: Il peso in libbre.
    Returns:
        Un dizionario contenente il peso convertito in chilogrammi.
    """
    kilograms = pounds / 2.20462
    return {"result": kilograms}
