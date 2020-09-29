const masterColor = [51, 153, 0]

function convert(str) {
    let total = 0
    for (let i = 0; i < str.length; i++) {
        total += str[i].charCodeAt(0) * i
    }
    return total
}
function selectColor(number) {
    const hue = number * 137.508; // use golden angle approximation
    return `hsl(${hue},50%,75%)`;
}

const grids = {}
navigator.geolocation.getCurrentPosition(async position => {
    const [lat, lng] = [position.coords.latitude, position.coords.longitude]

    const response = await fetch(`http://localhost:5000/${lat},${lng}`)
    const result = await response.json()
    
    for (const activity in result.bounds) {
        const [lower, upper] = [ result.bounds[activity][0], result.bounds[activity][1] ]
        grids[activity] = (function() {
            const arr = []
            for (let i = 0; i <= upper - lower; i++) {
                arr.push((function() {
                    const a = []
                    for (let i = 0; i < 7; i++) {
                        a.push([])
                    }
                    return a
                })())
            }
            return arr
        })()
    }

    for (const chunk of result.chunks) {
        const grid = grids[chunk.activity]
        const row = chunk.dateFromTodayInt
        
        const cols = [...Array(chunk.endTimeInt - chunk.startTimeInt + 1).keys()]

        for (let col = chunk.startTimeInt; col < chunk.endTimeInt; col++) {
            grid[col - result.bounds[chunk.activity][0]][row].push(...chunk.locations)
        }
    }

    const app = new Vue({
        el: '#app',
        data: {
            grid: grids.Walking,
            locations: result.locations.reduce((acc, cur) => {
                acc[cur] = selectColor(convert(cur))
                return acc
            }, {}),
            days: result.days
        },
        methods: {
            getShade: function(n) {
                const ratio = n / result.locations.length

                if (ratio == 0) {
                    return 'FFFFFF'
                }
                const color = masterColor.map(x => x * ratio)
                return `rgb(${color[0]},${color[1]},${color[2]})`
            }
        }
    })
})