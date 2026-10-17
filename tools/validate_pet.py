"""Validate berber's packaged 8x9 animation atlas without modifying it."""
import argparse
import json
from pathlib import Path

from PIL import Image

FRAME_COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6)


def validate(pet_dir: Path) -> dict:
    metadata = json.loads((pet_dir / 'pet.json').read_text(encoding='utf-8-sig'))
    for field in ('id', 'displayName', 'description', 'spritesheetPath'):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f'pet.json needs a non-empty {field}')
    if metadata.get('spriteVersionNumber', 1) != 1:
        raise ValueError('This checker expects the 8x9 v1 atlas, not a v2 atlas')
    sprite_path = (pet_dir / metadata['spritesheetPath']).resolve()
    if not sprite_path.is_relative_to(pet_dir.resolve()):
        raise ValueError('spritesheetPath must stay inside the pet folder')
    with Image.open(sprite_path) as source:
        if source.size != (1536, 1872):
            raise ValueError(f'Expected 1536x1872, got {source.size}')
        if 'A' not in source.getbands():
            raise ValueError('Spritesheet needs an alpha channel')
        atlas = source.convert('RGBA')
    for row, frame_count in enumerate(FRAME_COUNTS):
        for column in range(8):
            cell = atlas.crop((column*192, row*208, (column+1)*192, (row+1)*208))
            visible = cell.getchannel('A').getbbox() is not None
            if visible != (column < frame_count):
                raise ValueError(f'Unexpected empty/occupied cell at row {row}, column {column}')
    pixels = atlas.tobytes()
    residue = sum(pixels[i+3] == 0 and any(pixels[i:i+3])
                  for i in range(0, len(pixels), 4))
    if residue:
        raise ValueError(f'{residue} fully transparent pixels retain RGB data')
    return {'ok': True, 'pet': metadata['id'], 'states': 9, 'frames': 57,
            'unused_cells': 15, 'transparent_rgb_residue_pixels': 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pet_dir', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'berber')
    args = parser.parse_args()
    try:
        result = validate(args.pet_dir)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=True))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
