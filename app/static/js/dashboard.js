navigator.geolocation.getCurrentPosition(async position => {
    const [lat, lng] = [position.coords.latitude, position.coords.longitude]

    const response = await fetch(`http://localhost:5000/${lat},${lng}`)
    const result = await response.json()

    const activities = []
    const activityCardHolder = document.createElement('div');
    activityCardHolder.className = 'uk-flex uk-flex-column uk-margin-xlarge-left uk-margin-xlarge-right uk-margin-top'
    result.chunks.forEach(chunk => createCard(chunk, activities, activityCardHolder))
    document.querySelector('#activitiesContainer').appendChild(activityCardHolder)
})

function createCard(chunk, activities, activityCardHolder) {
    const activityName = chunk.activity
    if (!activities[activityName]) {
        activities[activityName] = createActivityCard(activityName)
        activityCardHolder.appendChild(activities[activityName])
    }
    activities[activityName].querySelector('.detailsCardHolder').appendChild(createDetailsCard(chunk))
}

function createActivityCard(activity) {
    const activityCard = document.createElement('div')
    activityCard.className = 'uk-card-large uk-card-default uk-margin-large-bottom'

    const header = document.createElement('div')
    header.classList = 'uk-card-header uk-padding-remove-top uk-padding-remove-bottom'

    const heading = document.createElement('h3')
    heading.className = 'uk-card-title'
    heading.innerText = activity

    header.appendChild(heading)
    activityCard.appendChild(header)

    const body = document.createElement('div')
    body.classList = 'uk-card-body uk-padding-remove'

    const detailsCardHolder = document.createElement('div')
    detailsCardHolder.classList = 'uk-flex detailsCardHolder'
    detailsCardHolder.style.overflowX = 'scroll'

    body.appendChild(detailsCardHolder)
    activityCard.appendChild(body)

    return activityCard
}

function createDetailsCard(chunk) {
    const detailsCard = document.createElement('div')
    detailsCard.classList = 'uk-card-small uk-card-secondary uk-card-hover uk-margin-left'
    detailsCard.style.marginTop = '5px'

    const header = document.createElement('div')
    header.classList = 'uk-card-header uk-padding-remove uk-text-center'
    header.style.width = '16em'

    const heading = document.createElement('h3')
    heading.classList = 'uk-card-title'
    heading.innerHTML = `${chunk.date}<br>${chunk.startTime12h} - ${chunk.endTime12h}`

    header.appendChild(heading)
    detailsCard.appendChild(header)

    const body = document.createElement('div')
    body.classList = 'uk-card-body uk-padding-remove'
    body.style.marginLeft = '8px'

    const localHeading = document.createElement('h4')
    localHeading.innerText = chunk.locations[0]
    if (chunk.locations.length > 1) {
        const moreLocations = document.createElement('span')
        moreLocations.innerText = ' +' + (chunk.locations.length - 1)
        chunk.locations.forEach(location => moreLocations.title += location + '\n')
        localHeading.appendChild(moreLocations)
    }

    const weatherIcon = document.createElement('img')
    weatherIcon.classList = 'uk-align-right uk-margin-remove'
    weatherIcon.src = chunk.weather.icon
    weatherIcon.style.width = '100px'
    localHeading.appendChild(weatherIcon)

    body.appendChild(localHeading)

    const weatherDescription = document.createElement('p')
    weatherDescription.innerText = chunk.weather.desc

    body.appendChild(weatherDescription)
    detailsCard.appendChild(body)

    return detailsCard
}