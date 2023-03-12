from difflib import SequenceMatcher


def compare(comparison, query):
    return SequenceMatcher(None, comparison, query).ratio()

def similar(comparison, query):
    highest=compare(comparison, query)
    for i in comparison.split(' '):
        a = compare(i, query)
        if a>0.69 and a>highest:
            highest=a
    return highest


def create_index(query, books):
    ranking = []
    for i in books:
        ranking.append({
        'book': i,
        'title':similar(i.title, query),
        'author': similar(i.author, query), 
        'category': similar(i.category, query)
        })
    return ranking

#TODO: dodać próg poniżej którego wyniki są odrzucane 
def search(query, books):
    rank = create_index(query, books)
    rank_titles = sorted(rank, key=lambda d: d['title'], reverse=True)
    rank_authors = sorted(rank, key=lambda d: d['author'], reverse=True)
    rank_categories = sorted(rank, key=lambda d: d['category'], reverse=True)

    print([i for i in rank_authors if i['author']>0.5])
    return rank_titles, rank_authors, rank_categories