db = db.getSiblingDB('movies')
printjson(
    db.merged.find({}, {'Title': 1, 'budget': 1, 'imdbRating': 1, 'Year': 1, 'Actors': 1, 'production_companies.name': 1, '_id': 0}).limit(1000).toArray().sort((a, b) => a.budget - b.budget)
)
