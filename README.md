[![Logo](https://github.com/dcs-retribution/dcs-retribution/raw/main/resources/ui/splash_screen.png)](https://shdwp.github.io/ukraine/)

(Github Readme Banner and Splash screen Artwork by Andriy Dankovych, CC BY-SA 4.0)

[![Patreon](https://img.shields.io/badge/patreon-become%20a%20patron-orange?logo=patreon)](https://patreon.com/dcsliberation)

[![Download](https://img.shields.io/github/downloads/dcs-retribution/dcs-retribution/total?label=Download)](https://github.com/dcs-retribution/dcs-retribution/releases)

[![Discord](https://img.shields.io/discord/1015931619187621999?label=Discord&logo=discord)](https://discord.gg/b4x34Bg4We)

[![GitHub pull requests](https://img.shields.io/github/issues-pr/dcs-retribution/dcs-retribution)](https://github.com/dcs-retribution/dcs-retribution/pulls)
[![GitHub issues](https://img.shields.io/github/issues/dcs-retribution/dcs-retribution)](https://github.com/dcs-retribution/dcs-retribution/issues)
![GitHub stars](https://img.shields.io/github/stars/dcs-retribution/dcs-retribution?style=social)

## About DCS Retribution 
(Last update: 2023-05-20)

DCS Retribution was forked from [DCS Liberation](https://github.com/dcs-liberation/dcs_liberation),
which is a [DCS World](https://www.digitalcombatsimulator.com/en/products/world/) turn based single-player or co-op dynamic campaign. 
It is an external program that generates full and complex DCS missions and manage a persistent combat environment.

![Screenshot](https://user-images.githubusercontent.com/315852/120939254-0b4a9f80-c6cc-11eb-82f5-ce3f8d714bfe.png)

DCS Retribution is still relying on Liberation for certain updates,
and will possibly stay that way in a more distant future. Therefore,
the patreon link will keep pointing to [Khopa's](https://github.com/Khopa) account until further notice.
However, we are no longer backwards compatible with Liberation, and will no longer attempt to do so.

Instead, we are focussing on keeping our campaigns forward compatible so that you as a user
can continue on whatever campaign you had going on.
Please keep in mind that once you save a campaign that was started
in a previous (save-compatibility breaking) build, your save file
will have been migrated and thus no longer compatible with the previous build.
Therefore, we recommend backing up your saves and perhaps organizing them by version/build number.

For a more complete overview of our features, check the
[changelog](https://github.com/dcs-retribution/dcs-retribution/blob/main/changelog.md).

## Downloads

Latest release is available here : https://github.com/dcs-retribution/dcs-retribution/releases

To download preview builds of the next version of DCS Retribution, see https://github.com/dcs-retribution/dcs-retribution/wiki/Betas.

## DCS bugs

~~These DCS bugs prevent us from improving AI behavior. Please upvote them! (But please
_don't_ spam them with comments):~~

* ~~[A2A and SEAD escorts don't escort](https://forums.eagle.ru/topic/251798-options-for-alternate-ai-escort-behavior/?tab=comments#comment-4668033)~~
* ~~[DEAD can't use mixed loadouts effectively](https://forums.eagle.ru/topic/271941-ai-rtbs-after-firing-decoys-despite-full-load-of-bombs/)~~

While DCS bugs are still a thing, we don't quite agree with the ones stated above.
We believe to have addressed these, although some quirks still exist.
For example, SEAD Escorts tend to be a little picky with what they engage,
especially with older SAM systems.

## Bugs and feature requests

If you need to report a bug or want to suggest a new feature, you can do this on our 
[bug tracker](https://github.com/dcs-retribution/dcs-retribution/issues).
In either case, please use the search bar at the top of the page to see if it has already been reported.
Note that you may need to remove the filter for open bugs if it's something we've recently fixed.

## Roadmap

Our plans for future releases can be found on our
[Projects page](https://github.com/dcs-retribution/dcs-retribution/projects).
Each planned release has a Project, and the page for that project has columns for to do,
in progress, and done. Items in the Done column are in the
[preview build](https://github.com/dcs-retribution/dcs-retribution/wiki/Betas)
for that release. Items in the To do column are planned to be added to that release.

## Resources

Tutorials, contributors and developer's guides are available in the project's
[Wiki](https://github.com/dcs-retribution/dcs-retribution/wiki/)

(Some historical information is also availabe on
[Liberation's Wiki](https://github.com/dcs-liberation/dcs_liberation/wiki/))

## Special Thanks

First, a big thanks to shdwp, for starting the original DCS Liberation project. 

Then, DCS Liberation/Retribution uses [pydcs](https://github.com/pydcs/dcs) for mission generation, and nothing would be possible without this.
It also uses the popular [Mist](https://github.com/mrSkortch/MissionScriptingTools) lua framework for mission scripting.

Excellent lua scripts DCS Liberation/Retribution uses as plugins:

* For the JTAC feature, DCS Retribution embeds Ciribob's JTAC Autolase [script](https://github.com/ciribob/DCS-JTACAutoLaze).
* Walder's [Skynet-IADS](https://github.com/walder/Skynet-IADS) is used for Integrated Air Defense System.
* Carstens Arty Spotter https://www.digitalcombatsimulator.com/en/files/3339128/ is an amazing force multiplyer to drop the hammer on enemies.

Please also show some support to these projects ! 
