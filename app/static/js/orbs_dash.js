Set.prototype.difference = function(otherSet) {
    // creating new set to store difference 
    var differenceSet = new Set(); 

    // iterate over the values 
    for(var elem of this) { 
        // if the value[i] is not present  
        // in otherSet add to the differenceSet 
        if(!otherSet.has(elem)) 
            differenceSet.add(elem); 
    } 

    // returns values of differenceSet 
    return differenceSet; 
}
function isSuperset(set, subset) {
    for (let elem of subset) {
        if (!set.has(elem)) {
            return false
        }
    }
    return true
}

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
                        a.push(new Set())
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
            const set = grid[col - result.bounds[chunk.activity][0]][row]
            chunk.locations.forEach(l => set.add(l))
        }
    }

    function findLocationGroups(arr, categories) {
        const result = branch(arr, 0, categories)

        const flattened = []
        function unwrap(arr) {
            arr.forEach(elem =>{
                if (elem instanceof Array) {
                    return unwrap(elem)
                }
                flattened.push(elem)
            })
        }
        unwrap(result)
        return flattened
    }

    function branch(arr, i, equivalent) {
        if (i == arr.length || equivalent.size == 1) {
            return equivalent
        }

        const examine = arr[i].locations.filter(l => equivalent.has(l))
        if (examine.length == equivalent.size || examine.length == 0) {
            return branch(arr, ++i, equivalent)
        }

        const present = new Set()
        examine.forEach(l => present.add(l))
        const absent = equivalent.difference(present)

        return [ branch(arr, ++i, present), branch(arr, ++i, absent) ]
    }

    const set = new Set()
    result.locations.forEach(l => set.add(l))
    const groups = findLocationGroups(result.chunks, set)

    const app = new Vue({
        el: '#app',
        data: {
            grid: grids.Walking,
            locations: result.locations.reduce((acc, cur) => {
                acc[cur] = selectColor(convert(cur))
                return acc
            }, {}),
            days: result.days,
            locationGroups: groups
        },
        methods: {
            groupToColor: function(set) {
               return selectColor(convert(Array.from(set).join(', ')))
            }
        },
        computed: {
            groupsOnGrid: function() {
                return this.grid.map(row => row.map(locations => {
                    const groups = []
                    this.locationGroups.forEach(group => {
                        if (isSuperset(locations, group)) {
                            groups.push(group)
                        }
                    })
                    return groups
                }))
            }
        }
    })
})