var Data = require('../data.json')
var data1 = require('./stage1.json')
var data2 = require('./stage2.json')
var data3 = require('./stage3.json')
var data4 = require('./stage4.json')

const stage1 = () => {

    let dataset = Data
        .filter(movie => parseFloat(movie.imdbRating))
        .sort((a, b) => parseFloat(a.imdbRating) - parseFloat(b.imdbRating))
        .reverse()

    let actors = []

    dataset.forEach(movie => {
        movie.Actors.split(', ').forEach(actor => {
            if (actors.indexOf(actor) === -1) actors.push(actor)
        })
    })

    let stage1 = []

    actors.forEach(actor => {

        let temp = {
            actor,
            f: 0
        }

        Data.forEach(movie => {
            movie.Actors.split(', ').forEach(a => {
                if (actor === a) temp.f++
            })
        })

        stage1.push(temp)
    })

    stage1 = stage1.filter(actor => actor.f > 2)

    return stage1
}

const stage2 = () => {

    var stage2 = []

    data1.forEach(actor1 => {

        data1.forEach(actor2 => {

            if (actor1.actor === actor2.actor) return
            for (var i = 0; i < stage2.length; i++) {
                if (stage2[i].actors[0] == actor1 &&
                    stage2[i].actors[1] == actor2)
                    return
                if (stage2[i].actors[1] == actor1 &&
                    stage2[i].actors[0] == actor2)
                    return
            }

            var temp = {
                actors: [actor1, actor2],
                f: 0
            }

            Data.forEach(movie => {

                var done = 2

                movie.Actors.split(', ').forEach(a => {
                    if (a === actor1.actor || a === actor2.actor) done--
                })

                if (done == 0) temp.f++
            })

            if (temp.f > 0) stage2.push(temp)
        })

    })

    stage2 = stage2.filter(actors => actors.f > 1)

    return stage2
}

const stage3 = () => {

    var stage3 = []

    data1.forEach(actor => {

        data2.forEach(actors => {

            if (actors.actors[0].actor === actor.actor) return
            if (actors.actors[1].actor === actor.actor) return

            for (var i = 0; i < stage3.length; i++) {

                if (stage3[i].actors[0].actor === actors.actors[0].actor &&
                    stage3[i].actors[1].actor === actors.actors[1].actor &&
                    stage3[i].actors[2].actor === actor.actor)
                    return

                if (stage3[i].actors[1].actor === actors.actors[0].actor &&
                    stage3[i].actors[0].actor === actors.actors[1].actor &&
                    stage3[i].actors[2].actor === actor.actor)
                    return

                if (stage3[i].actors[2].actor === actors.actors[0].actor &&
                    stage3[i].actors[1].actor === actors.actors[1].actor &&
                    stage3[i].actors[0].actor === actor.actor)
                    return

                if (stage3[i].actors[0].actor === actors.actors[0].actor &&
                    stage3[i].actors[2].actor === actors.actors[1].actor &&
                    stage3[i].actors[1].actor === actor.actor)
                    return
            }

            var temp = {
                actors: [actor, ...actors.actors],
                f: 0,
                r: 0
            }

            Data.forEach(movie => {

                var done = 3

                movie.Actors.split(', ').forEach(a => {
                    temp.actors.forEach(actor => {
                        if (actor.actor === a) done--
                    })
                })

                if (done == 0) {
                    temp.f++
                    temp.r += parseFloat(movie.imdbRating)
                }
            })

            temp.r /= temp.f
            if (temp.f > 0) stage3.push(temp)
        })

    })

    stage3 = stage3.filter(actors => actors.f > 1)

    return stage3
}

const stage4 = () => {

    var stage = []

    data1.forEach(actor => {

        data3.forEach(actors => {

            if (actors.actors[0].actor === actor.actor) return
            if (actors.actors[1].actor === actor.actor) return
            if (actors.actors[2].actor === actor.actor) return

            var arr = [actor, ...actors.actors]
            var freq = 0
            var rating = 0

            for (var i = 0; i < Data.length; i++) {

                var _actors = Data[i].Actors.split(', ')

                var done = 4

                for (var b of arr)
                    for (var c of _actors)
                        if (b.actor === c)
                            done--

                if (done == 0) {
                    freq++
                    rating += parseFloat(Data[i].imdbRating)
                }
            }

            rating /= freq
            if (freq > 0) stage.push({
                actors: arr,
                f: freq,
                r: rating,
            })

        })

    })

    return stage
}

const stage5 = () => {

    var stage = []

    for (var i = 0; i < data4.length; i++) {
        data4[i].actors.sort((a, b) => {

            var nameA = a.actor.toUpperCase(); // ignore upper and lowercase
            var nameB = b.actor.toUpperCase(); // ignore upper and lowercase

            if (nameA < nameB) {
              return -1;
            }
            if (nameA > nameB) {
              return 1;
            }

            return 0;
        })
        stage.push(data4[i])
    }

    var a = stage
    var b = stage

    for (var i = 0; i < a.length; i++) {

        for (var j = 0; j < b.length; j++) {

            if (JSON.stringify(a[i]) == JSON.stringify(b[j]) && i != j)
                b.splice(j, 1)
        }

    }

    stage = b

    return stage
}
