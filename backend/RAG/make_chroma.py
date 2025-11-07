from Chroma_class import Chroma_Init

CHROMA_PATH = "./chroma_db"
DATA_PATH = "Vulnerabilities.pdf"

if __name__ == "__main__":
    chroma_db = Chroma_Init(DATA_PATH, CHROMA_PATH)
    db = chroma_db.add_to_chroma()


### Vulnerabilities.pdf HAS BEEN ALREADY ADDED, ADD NEW FILES ONLY

