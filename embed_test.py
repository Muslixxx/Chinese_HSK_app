from sentence_transformers import SentenceTransformer
import numpy as np


def cos(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> None:
    # Utilise le modèle paraphrase local (aucun préfixe query/passage)
    model = SentenceTransformer("models/paraphrase-multi", device="cpu")

    pairs = [
        ("manger", "partir"),
        ("manger", "bouffer"),
        ("je vais à l'école", "je me rends au collège"),
        ("le chat est sur le tapis", "le chien est dans le jardin"),
        ("il fait beau aujourd'hui", "le soleil brille ce jour-ci"),
        ("la voiture rouge", "le véhicule écarlate"),
        ("j'aime la musique classique", "j'apprécie les symphonies"),
        ("le ciel est bleu", "l'océan est vaste"),
        ("le film était captivant", "le livre était ennuyeux"),
        ("la technologie avance rapidement", "les innovations technologiques progressent vite"),
    ]

    for ref, usr in pairs:
        e_ref = model.encode([ref], normalize_embeddings=True)[0]
        e_usr = model.encode([usr], normalize_embeddings=True)[0]
        print(f"ref={ref!r} usr={usr!r} -> cosine: {cos(e_usr, e_ref):.3f}")


if __name__ == "__main__":
    main()
