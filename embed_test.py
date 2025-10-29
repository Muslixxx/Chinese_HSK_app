from sentence_transformers import SentenceTransformer
import numpy as np


def main() -> None:
    model = SentenceTransformer("models/e5-small", device="cpu")
    refs = ["manger"]
    user = "voiture"

    # Normalize embeddings to simplify cosine computation
    e_refs = model.encode(refs, normalize_embeddings=True)
    e_user = model.encode([user], normalize_embeddings=True)[0]

    cos = float(np.dot(e_user, e_refs[0]) / (np.linalg.norm(e_user) * np.linalg.norm(e_refs[0])))
    print("cosine:", round(cos, 3))


if __name__ == "__main__":
    main()
