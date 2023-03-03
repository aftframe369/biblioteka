from difflib import SequenceMatcher


def compare(comparison, term):
    return SequenceMatcher(None, comparison, term).ratio()

def similar(comparison, term):
    highest=compare(comparison, term)
    for i in comparison.split(' '):
        a = compare(i, term)
        if a>0.69 and a>highest:
            highest=a
    return highest


def create_index(term, books):
    ranking = []
    for i in books:
        ranking.append({
        'book': i,
        'title':similar(i.title, term),
        'author': similar(i.author, term), 
        'category': similar(i.category, term)
        })
    return ranking

#TODO: dodać próg poniżej którego wyniki są odrzucane 
def search(term, books):
    rank = create_index(term, books)
    rank_authors = sorted(rank, key=lambda d: d['author'], reverse=True)
    rank_titles = sorted(rank, key=lambda d: d['title'], reverse=True)
    rank_categories = sorted(rank, key=lambda d: d['category'], reverse=True)

    books_ranked_in_different_ways =[]
    for ranking in rank_titles, rank_authors, rank_categories:
        books_ranked_in_different_ways.append(ranking)
    return books_ranked_in_different_ways