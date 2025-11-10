# agent_core/tools/math.py
from .registry import registry

@registry.register(category="math")
def subtract(
    a: int , 
    b: int   
    ) -> dict:
    """
    Descrizione: Funzione utile per sottrarre due numeri interi.
    Args:
        a: Il primo numero.
        b: Il secondo numero.   
    Returns:
        Un dizionario contenente il risultato della sottrazione.
    """
    return {"result": a - b}

@registry.register(category="math")
def add(
    a: int, 
    b: int
    ) -> dict:
    """
    Descrizione: Funzione utile per sommare due numeri interi.
    Args:
        a: Il primo numero.
        b: Il secondo numero.
    Returns:
        Un dizionario contenente il risultato della somma.
    """
    return {"result": a + b}

@registry.register(category="math")
def multiply(
    a: int, 
    b: int
    ) -> dict:
    """
    Descrizione: Funzione utile per moltiplicare due numeri interi.
    Args:
        a: Il primo numero.
        b: Il secondo numero.
    Returns:
        Un dizionario contenente il risultato della moltiplicazione.
    """
    return {"result": a * b}

@registry.register(category="math")
def divide(
    a: int, 
    b: int
    ) -> dict:
    """
    Descrizione: Funzione utile per dividere due numeri interi.
    Args:
        a: Il primo numero.
        b: Il secondo numero (non deve essere zero).
    Returns:
        Un dizionario contenente il risultato della divisione.
    Raises:
        ValueError: Se il divisore è zero.
    """
    if b == 0:
        raise ValueError("Il divisore non può essere zero.")
    return {"result": a / b}
