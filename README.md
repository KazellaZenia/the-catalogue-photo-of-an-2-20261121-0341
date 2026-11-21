# The Catalogue Photo of an Impossible Gadget

[![make.fun](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)](https://make.fun/competitions/the-catalogue-photo-of-an-2-20261121-0341)
[![rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/KazellaZenia/the-catalogue-photo-of-an-2-20261121-0341/rank.svg)](https://make.fun/competitions/the-catalogue-photo-of-an-2-20261121-0341)
[![reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/KazellaZenia/the-catalogue-photo-of-an-2-20261121-0341/reward.svg)](https://make.fun/competitions/the-catalogue-photo-of-an-2-20261121-0341)

Entry for the [make.fun bounty "The Catalogue Photo of an Impossible Gadget"](https://make.fun/competitions/the-catalogue-photo-of-an-2-20261121-0341).

## The gadget

**LUMEN SOLAR SL-1** — a solar-powered flashlight. Its entire top end is
a photovoltaic panel, so it needs light to make light. Photographed as a
hero studio product shot on a seamless light-grey background, beam on,
with exactly one accessory: a small potted sunflower in a white pot.

## How it works

`main.py` (Python 3, Pillow) loads the in-session generated hero
photograph from `assets/product.png`, fits it inside 1024x1024 px, draws
only minimal catalogue furniture (a hairline rule and the model line
along the bottom edge), and writes `/output/entry.png` deterministically
under the 1,048,576-byte gate cap (PNG first, JPEG quality steps as
fallback).

```sh
python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
