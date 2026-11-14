# Red Frontier: Junior Astronaut Mission Trainer

NASA Space Apps 2026 challenge: *Build a Junior Astronaut Mission Trainer.*

## Play and install
- **Play online:** https://benedict-nimo.github.io/red-frontier/ (free, no login).
- **Install as an app:** press **Install the app** on the title screen. On iPhone or iPad (Safari): Share → **Add to Home Screen**. On Android (Chrome): ⋮ menu → **Install app**. On a computer (Chrome or Edge): the install icon in the address bar. The app opens full-screen and works offline after the first visit.
- **Slow device?** Graphics are set automatically and drop to a lighter setting if the game runs slowly. You can also choose Auto, High, Medium or Low with the **Graphics** button (top right, or in Help).

## Adventure mode (`index.html`): the main game
**Story:** Astro was flying a monthly sample-check mission around Mars when a rogue asteroid hit the rocket. Astro crash-landed next to an empty NASA supply outpost with supplies for only 1 month (30 sols). Unless Astro calls for help, Earth won't send a rescue for another 5 months. Astro has to survive with what's there and reach the satellite uplink to request an immediate rescue. An animated 5-scene intro tells the story, with a read-aloud option.

| Level | Martian problem | What the player does | Tool earned |
|---|---|---|---|
| 1 Power up | Crash dust covers the solar panels, and the emergency tools are wooden | Brush the dust off 3 panels **and** mine basalt and collect hematite and sulfate to upgrade the pickaxe, brush and shovel from wood to stone at the workbench (both are required) | Ice drill |
| 2 Find water | Water is too heavy to fly in | Drill about 10 m to ice without overheating; put the water-cleaning steps in order | Oxygen kit (+6 sols) |
| 3 Make air | Mars air is 95% CO₂ | Split CO₂ molecules (MOXIE); follow the hiss and patch the leak | Seed kit (+6 sols) |
| 4 Grow food | Toxic perchlorate soil, limited power | Pick out the perchlorate crystals; share 10 power units | Radio parts (+8 sols) |
| 5 Solar storm | A real-data particle storm is coming | Build a regolith shield wall, send the 3 sample robots inside, beat the timer | Emergency beacon |
| 6 Call Earth | Earth won't send help for 5 months | Climb to the satellite, rewire its power, aim the dish at Earth, send the SOS | Junior Astronaut medal |

- **Stone tools work better:** the stone pickaxe mines in 1 hit instead of 3, and the stone brush cleans a wider strip.
- **Manual pages:** the crash scattered 12 pages of the spacecraft manual around the base. Walking over one collects it. Each page gives a hint for one of the 2 Mission Control quiz questions at the end of each level. The Manual button shows the pages found and the ones still missing.
- **Supplies and sol clock:** one sol passes every 60 seconds of play. Supplies drop by 1 per sol, and a bit faster on nights below −90 °C. They're topped up by the water, air and food levels. If they run out, Astro finds an emergency ration box (+12 sols) and the certificate counts how many were needed.
- **Real Mars weather:** every sol shows the measured high, low and air pressure from a real day of NASA's Phoenix lander weather station (data.nasa.gov listing "Phoenix Mars Meteorological Pressure/Temperature RDR V1.0", files from the NASA PDS Atmospheres Node). The data covers 137 sols in 2008: night lows of −78 to −98 °C, and pressure falling from 855 to 722 Pa as CO₂ froze onto the polar cap. The temperature on screen rises and falls with the time of day, and the sky turns to night with stars and a helmet lamp. There's a full chart and a sol picker in **NASA data room → Mars weather**. The daily summaries are saved in `nasa/phoenix-weather-daily.json`.
- **Circular controls:** a round joystick lets you walk in any direction, and pushing it further makes you go faster. Drag the ground (or press Q and R) to rotate the camera, pinch or scroll to zoom, and a compass shows north. W A S D and the arrow keys also work, relative to the camera.
- **Map** (top-right button, or M): north-up, showing your position, numbered remaining tasks, the minerals still to collect in Level 1, the leak search area, the robots in Level 5, and "Guide me" waypoints.

## Strategy mode (`manager.html`)
The earlier sol-by-sol outpost management game, for older learners: cargo mass and budget, crew tasks, power math, solar storms, and a 2D rover drive.

## Real NASA data inside the game
- **Solar storms (NASA DONKI):** 7 solar particle storms recorded near Earth, 2025-11-14 to 2026-11-08 (42 satellite readings from GOES, SOHO, STEREO-A and ACE). Players explore them on a clickable timeline. The rate sets the in-game risk: about 45% chance of at least one storm in a 30-sol mission, and about 10 expected in a real 500-sol stay. Every in-game solar storm warning quotes one of these real events.
- **CMEs (NASA DONKI):** 130 coronal mass ejections, 2026-10-01 to 2026-11-14 (median 375 km/s, fastest 1,048 km/s). In the "CME race", players launch a real CME and see its travel time to Earth (40 h) and Mars (60 h), which is their warning time.
- **Photos (images.nasa.gov):** 12 official NASA images, each linked to a game mechanic (Phoenix ice and frost, MOXIE, Curiosity's sunset and solar-storm specks, Opportunity's dust storm, Spirit's dust devil, RASSOR, Veggie).
- Saved copy of the data: `nasa/donki-snapshot-2026-11-14.json`. When the game runs from a laptop or website, it also tries to fetch live CME data from api.nasa.gov.

## From the expert talk to the game
- **Wind tunnel lab:** the talk's walnut-shell experiment. Players switch between Earth and Mars air, and between sand and walnut shell, to find the wind speed that lifts grains.
- **Ask the Scientist quiz:** 14 questions from the talk and the NASA data, asked between sols. Right answers earn science, and 3 in a row earns a spare part. The debrief reports the quiz score, which gives learning evidence from playtests.
- **Trade-off badges:** the talk's list (iron triangle, weighted requirements, weight vs strength, speed vs cost, quality vs price, latency vs throughput, consistency vs availability) plus safety vs progress. Each one is unlocked by a real in-game decision. The latency vs throughput and consistency vs availability badges come from two new events: a data downlink and two sensors that disagree.
- **Atmosphere:** sound effects, screen shake and a flash during solar storms, read-aloud buttons for events and quiz questions, and confetti on success.
- **About this project** (on the title screen) covers the problem, how the game fits the challenge, the evidence and the sources, for judges.


## Datasets used
| Dataset | Source | Used for |
|---|---|---|
| Phoenix Mars Meteorological Pressure/Temperature RDR V1.0 | data.nasa.gov → NASA PDS Atmospheres Node | 137 sols of real daily high/low temperature and air pressure that drive the in-game sol clock |
| DONKI Solar Energetic Particle events | NASA DONKI (api.nasa.gov) | 7 real solar storms (Nov 2025 – Nov 2026) for the Level 5 storm and the data room |
| DONKI Coronal Mass Ejections | NASA DONKI (api.nasa.gov) | 130 CMEs for the "CME race" |
| NASA Image and Video Library | images.nasa.gov | 12 official photos shown in the game |

## Tech
A single `index.html` built with three.js r128 (3D) and Canvas 2D (pixel rover game). It doesn't need a build step. Open the file in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

## Building the app files
`index.html`, `manifest.webmanifest` and `sw.js` are generated by `tools/build.py` from the source page. The 3D engine (three.js r128, MIT licence) is in `vendor/`, and the fonts (Chakra Petch, Atkinson Hyperlegible, JetBrains Mono; SIL Open Font Licence, see `fonts/`) are in `fonts/`, so the app works offline.
