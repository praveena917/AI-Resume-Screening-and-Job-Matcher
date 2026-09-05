from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between
    resume and job description.
    """

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    return similarity * 100