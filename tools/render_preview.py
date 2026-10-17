"""Render all nine existing atlas rows as one transparent GIF preview."""
import argparse
import json
from pathlib import Path

from PIL import Image
from validate_pet import validate

DURATIONS = (
    (280, 110, 110, 140, 140, 320),
    (120, 120, 120, 120, 120, 120, 120, 220),
    (120, 120, 120, 120, 120, 120, 120, 220),
    (140, 140, 140, 280),
    (140, 140, 140, 140, 280),
    (140, 140, 140, 140, 140, 140, 140, 240),
    (150, 150, 150, 150, 150, 260),
    (120, 120, 120, 120, 120, 220),
    (150, 150, 150, 150, 150, 280),
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pet-dir', type=Path, default=root / 'berber')
    parser.add_argument('--output', type=Path, default=root / 'assets' / 'preview.gif')
    args = parser.parse_args()
    validate(args.pet_dir)
    metadata = json.loads((args.pet_dir / 'pet.json').read_text(encoding='utf-8-sig'))
    with Image.open(args.pet_dir / metadata['spritesheetPath']) as source:
        atlas = source.convert('RGBA')
    frames, durations = [], []
    for row, timing in enumerate(DURATIONS):
        for column, duration in enumerate(timing):
            frame = atlas.crop((column*192, row*208, (column+1)*192, (row+1)*208))
            frames.append(frame.resize((384, 416), Image.Resampling.LANCZOS))
            durations.append(duration)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(args.output, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=2, optimize=False)
    print(f'Rendered {len(frames)} frames to {args.output.name}')


if __name__ == '__main__':
    main()
