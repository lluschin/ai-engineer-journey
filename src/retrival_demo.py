from services.retrival_service import RetrivalService

documents = [
    "Der Hund spielt im Garten.",
    "Die Katze schläft auf dem Sofa.",
    "Python ist eine Programmiersprache.",
    "FastAPI ist ein Web Framework.",
]

retrival_service = RetrivalService()
retrival_service.add_documents(documents)

results = retrival_service.search("Welche Texte handeln von Tieren=", 2)

for result in results:
    print(f"{result['score']:.4} | {result['document']}")