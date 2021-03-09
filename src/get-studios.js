var data = require('../data.json');

(function main() {

    let studios = []

    data.forEach(movie => {

        let temp = movie.production_companies

        temp.forEach(studio => {
            if (studios.indexOf(studio.name) === -1)
                studios.push(studio.name)
        })

    })

    let out = {
        studios: [],
        ratings: []
    }

    let out2 = []

    studios.forEach(studio => {

        let ratings = []

        data.forEach(movie => {

            for (let std of movie.production_companies) {
                if (std.name === studio) {
                    ratings.push(parseFloat(movie.imdbRating) || 0)
                }
            }
        })

        if (ratings.length < 1)
            return

        let mean = ratings.reduce((acc, val) => acc + val) / ratings.length
        mean = Math.round(mean * 100) / 100

        out.studios.push(studio)
        out.ratings.push(mean)
    })

    out.studios.forEach((studio, i) => {

        out2.push({
            studio,
            rating: out.ratings[i]
        })
    })

    out2.sort((a, b) => a.rating - b.rating).reverse()

    console.log(JSON.stringify(out2))

})()

