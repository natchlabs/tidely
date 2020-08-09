# About

## Overview

todo: write overview.

## APIs used

Weather information is provided by the [worldweatheronline marine api](https://www.worldweatheronline.com/developer/api/marine-weather-api.aspx).

Geocoding is provided by the [HERE Developer geocoding api](https://developer.here.com/documentation/geocoder/dev_guide/topics/what-is.html)

# App breakdown

## General

- The [dashboard](#dashboard) is the main screen of the application; a returning user is brought here upon login.
- The dashboard contains a list of all of the times and places at which the user may engage in the [activities](#activities) which they have indicated that they are interested in.
- Associated with a user account will be a list of the activities that a user is interested in and the [weather conditions](#weather-preferences) which they desire for these activities.
- Also associated with a user account will be a list of the beaches / locations at which the user desires to engage in their activities of interest list.
- The default mode of the application is to use the fixed list of beaches for activity recommendations. The user may change the mode of the application to 'nearby', which will make recommendations at nearby beaches. For how this interacts with filtering, see [filtering](#filtering).
    - The last used mode of the application is remembered by the application on subsequent logins.
    - The radius used to find nearby beaches may be specified by the user.
- The user may add and remove which activities they are interested in on the [activities screen](#activities-screen). They may also change the weather conditions they desire for each activity at this screen.
    - This screen is the screen to which the user is brought upon registration.
- The application contains a warning to the user to use it at their own discretion, as it is not possible for information surrounding which beaches have no access points or are private to be incorporated into the application's recommendations.

## Dashboard

- The dashboard is mostly an information screen which does not allow for much user interaction in the way of changing data.
    - If the user wishes to change their various preferences / account settings, they must do this by accessing one of the other pages from the dashboard page.
- The dashboard contains cards, with each card representing one of the activities that the user is interested in.
- Each card has a title representing the activity and a horizontally scrolling list of elements which each represent one time at which the weather conditions at a location meet the requirements specified by the user for the respective activity.
    - Each element will display the timespan at which the weather requirements are met (e.g. 8.00-10.00am) and the location at which these requirements are met.
    - For further information (i.e. the exact weather information over this timespan) the element may be clicked and a drawer will appear from the right hand side of the screen containing the information.
- Cards may be dragged and dropped by the user to reorder them.
- There are [filtering](#filtering) buttons at the top of the dashboard which allow the user to filter certain elements out of the card displays.
    - Additionally, there are filtering buttons at the top right of every card. By default the global filter is applied, but if a card specific filter is applied then it will be combined with the global filter in the way described under [filtering](#filtering).

### Filtering

- The filtering buttons at the top allow the user to filter elements out based on location; e.g. so that only certain beaches are shown in the results.
- Additionally, the filtering buttons allow filtering by time; e.g. so that night-time results are not shown.
- The card-specific filters will be appended to the global filter if they are compatible (e.g. if the global filter is for the time and the card-specific one is for the location, they must be compatible) to create more specific filters.
- If the filters are not compatible, then the card-specific one will be applied rather than the global one.
- Filters are defined either as "belonging to this group" or "not belonging to this group."
- Filtering rules are unique between default mode and nearby mode; i.e. the filtering rules applied in one mode do not apply to the other mode and are saved when swapping to the other mode.

## Activities

- An activity consists of a name property and a set of weather preferences which the user wishes to perform the activity under.

### Weather preferences

- When deciding which timespans the user may want to perform an activity, the application will look at the weather preferences and find timespans which simultaneously meet all of the weather criteria.
- The basic criteria include wind speed, tide level, "feels like" temperature, cloud cover, and sun position (e.g. a possible configuration could be 'after sunrise and before sunset'), and rainfall level.
- More advanced options such as humidity, moon phase, wind direction, swell direction, swell height, and swell period are also available.
- The user is not required to set a preference for every weather option; those which the user has no preference towards will not be factored into filtering out results which don't match the user's desires.

## Activities screen

- The activities screen allows for the user to add and remove activities which they are interested in from the application.
- Activities should be selected from a presets list, which will have a list of common activities and the weather conditions which the user is most likely to desire for the specified activity.
    - If the user has slightly different weather requirements for the activity as compared to the preset, the user may edit these before using it.
    - Presets have their weather requirements described in a human readable format (e.g. cold weather excluded). Once the user has selected a preset, the fields are shown with their actual, numerical values. The user may alter these if they desire.
- Alternatively, users may create an activity with its weather requirements from scratch.
- The temperature option may either be set as the "feels like" temperature, or as the absolute temperature. The user is not permitted to have weather requirements on both restrictions simultaneously.
