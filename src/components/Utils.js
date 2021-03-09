import Data from '../../data.json'
import Studios from '../../studios.json'
import Actors from '../../actors.json'
import Trios from '../../trios.json'
import Quartets from '../../quartets.json'

const rnd = num => Math.round(num / 1000) / 1000

export const delta = (sorted, out) => {

    var min = 1000000000, max = 0

    for (let i = 0; i < sorted.length; i++)
        if (sorted[i].budget < min) min = sorted[i].budget

    for (let i = 0; i < sorted.length; i++)
        if (sorted[i].budget > max) max = sorted[i].budget

    let delta = max - min

    for (let i = 0; i < sorted.length; i++)
        out.datasets[0].pointBackgroundColor.push(
            'hsl(' + Math.round(sorted[i].budget * 256 / delta) + ', 100%, 70%)'
        )
}

export const movies = (from, to)=> {

    if (from > to) {
        let temp = from
        from = to
        to = temp
    }

    console.log(`filter from ${from} to ${to}`)

    var sorted = []

    var out = {
        labels: [],
        datasets: [{
            label: 'IMDb Rating',
            data: [],
            pointRadius: 10,
            pointBackgroundColor: [],
            labels: [],
        }, {
            label: 'Korrelationsanalyse',
            data: [],
            pointRadius: 5,
            borderColor: '#000',
            borderWidth: 1,
            backgroundColor: 'transparent',
        }],
    }

    sorted = Data.filter(movie => movie.Year <= to && movie.Year >= from)
    sorted = sorted.filter(movie => movie.budget)
    sorted = sorted.filter(movie => parseFloat(movie.imdbRating))
    delta(sorted, out)

    var korr = {
        $x: 0,
        $y: 0,
        num: 0,
        denA: 0,
        denB: 0,
    }

    sorted.forEach(movie => {

        out.labels.push(rnd(movie.budget))
        out.datasets[0].data.push(movie.imdbRating)
        out.datasets[0].labels.push(movie.Title)

        korr.$x += movie.budget
        korr.$y += parseFloat(movie.imdbRating)
    })

    korr.$x /= sorted.length
    korr.$y /= sorted.length

    sorted.forEach(movie => {
        korr.num += (movie.budget - korr.$x) * (parseFloat(movie.imdbRating) - korr.$y)
        korr.denA += Math.pow(movie.budget - korr.$x, 2)
        korr.denB += Math.pow(parseFloat(movie.imdbRating) - korr.$y, 2)
    })

    korr.denA = Math.pow(korr.denA, .5)
    korr.denB = Math.pow(korr.denB, .5)

    var r = korr.num / (korr.denA * korr.denB)

    out.datasets[1].data = [
        {
            x: rnd(sorted[0].budget),
            y: r * ((sorted[0].budget - korr.$x) / korr.$x) + korr.$y,
        },
        {
            x: rnd(sorted[sorted.length - 1].budget),
            y: r * ((sorted[sorted.length - 1].budget - korr.$x) / korr.$x) + korr.$y,
        }
    ]

    return out
}

export const studios = (page)=> {

    var out = {
        labels: [],
        datasets: [{
            label: 'Mean IMDb Rating',
            data: [],
            pointRadius: 10,
            pointBackgroundColor: [],
            labels: [],
        }]
    }

    let drop = [Studios.length * (page - 1) / 20, Studios.length * page / 20]

    Studios.forEach((studio, i) => {
        if (i < drop[0] || i > drop[1]) return
        out.labels.push(studio.studio)
        out.datasets[0].data.push(studio.rating)
    })

    return out
}

export const actors = (page)=> {

    var out = {
        labels: [],
        datasets: [{
            label: 'Mean IMDb Rating',
            data: [],
            pointRadius: 10,
            pointBackgroundColor: [],
            labels: [],
        }]
    }

    let drop = [Actors.length * (page - 1) / 20, Actors.length * page / 20]

    Actors.forEach((actor, i) => {
        if (i < drop[0] || i > drop[1]) return
        out.labels.push(actor.actor)
        out.datasets[0].data.push(actor.rating)
    })

    return out
}

export const trios = () => {

    var out = {
        labels: [],
        datasets: [{
            label: 'Mean IMDb Rating',
            data: [],
            pointRadius: 10,
            pointBackgroundColor: [],
            labels: [],
        }]
    }

    Trios.forEach(trio => {
        out.labels.push('')
        out.datasets[0].labels.push(trio.actors.reduce((acc, val) => acc += val.actor + '\n', ''))
        out.datasets[0].data.push(trio.r)
    })

    return out
}

export const quartets = () => {

    var out = {
        labels: [],
        datasets: [{
            label: 'Mean IMDb Rating',
            data: [],
            pointRadius: 10,
            pointBackgroundColor: [],
            labels: [],
        }]
    }

    Quartets.forEach(quartet => {
        out.labels.push('')
        out.datasets[0].labels.push(quartet.actors.reduce((acc, val) => acc += val.actor + '\n', ''))
        out.datasets[0].data.push(quartet.r)
    })

    return out
}
