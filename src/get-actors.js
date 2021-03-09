var data = require('../data.json');

(function main() {

    let actors = []

    data.forEach(movie => {

        let temp = movie.Actors.split(', ')

        temp.forEach(actor => {
            if (actors.indexOf(actor) === -1)
                actors.push(actor)
        })

    })

    let out = {
        actors: [],
        ratings: []
    }

    let out2 = []

    actors.forEach(actor => {

        let ratings = []

        data.forEach(movie => {

            let temp = movie.Actors.split(', ')

            if (temp.indexOf(actor) !== -1)
                ratings.push(parseFloat(movie.imdbRating) || 0)
        })

        if (ratings.length < 1) return

        let mean = ratings.reduce((acc, val) => acc + val) / ratings.length
        mean = Math.round(mean * 100) / 100

        out.actors.push(actor)
        out.ratings.push(mean)
    })

    out.actors.forEach((actor, i) => {

        out2.push({
            actor,
            rating: out.ratings[i]
        })
    })

    out2.sort((a, b) => a.rating - b.rating).reverse()

    console.log(JSON.stringify(out2))

})()

