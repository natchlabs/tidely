_sun = { 113, 116 }
_overcast = { 119, 122, 143, 248, 260 }

_lightRain = { 176, 263, 266, 293, 296, 311, 353 }
_lightSnow = { 179, 182, 185, 317, 323, 326, 362, 368 }

_lightning = { 200, 386, 389, 392, 395 }
_snow = { 227, 320, 329, 332, 392 }
_rain = { 281, 299, 302 }

_heavySnow = { 230, 335, 338, 365, 371, 395 }
_heavyRain = { 284, 305, 308, 314, 356, 359, 389 }

_icePellets = { 374, 377, 350 }

_all = _sun | _overcast | _lightRain | _lightSnow | _lightning | _snow | _rain | _heavyRain | _heavySnow | _icePellets

sunny = _sun
calm = _sun | _overcast
uncalm = _all - calm
raining = _lightRain | _rain | _heavySnow
snowing = _lightSnow | _snow | _heavySnow