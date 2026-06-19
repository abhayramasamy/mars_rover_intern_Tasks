import os
import yaml
import click
import cv2
from cv2 import aruco
import numpy as np


DICT_NAME = aruco.DICT_4X4_50

# 4x3 cube net layout:
#   row 0:        left
#   row 1: bottom  front  top
#   row 2:        back
#   row 3:       right
#
# This matches the original logic:
# ids are assigned in this order:
# left, bottom, front, top, back, right
FACE_POSITIONS = {
    "left":   (0, 1),
    "bottom": (1, 0),
    "front":  (1, 1),
    "top":    (1, 2),
    "back":   (2, 1),
    "right":  (3, 1),
}


class MarkerFactory:
    def __init__(self, aruco_dict_name=DICT_NAME):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco_dict_name)

    def create_marker_tile(
        self,
        tile_size: int,
        marker_id: int,
        marker_fraction: float = 0.62,
    ) -> np.ndarray:
        """
        Create one full tile:
        - white background
        - large ArUco marker centered inside
        - wide quiet zone around it

        marker_fraction controls how much of the tile is occupied by the marker.
        Smaller fraction = bigger white border = better quiet zone.
        """
        if not (0.2 < marker_fraction < 0.9):
            raise ValueError("marker_fraction should be between 0.2 and 0.9")

        tile = np.full((tile_size, tile_size), 255, dtype=np.uint8)

        marker_size = int(tile_size * marker_fraction)
        marker_size = max(8, marker_size)

        # Make marker size even so centering is cleaner
        if marker_size % 2 == 1:
            marker_size += 1

        quiet_zone = (tile_size - marker_size) // 2
        quiet_zone = max(1, quiet_zone)

        marker = aruco.generateImageMarker(self.aruco_dict, marker_id, marker_size)

        y0 = quiet_zone
        y1 = quiet_zone + marker_size
        x0 = quiet_zone
        x1 = quiet_zone + marker_size

        tile[y0:y1, x0:x1] = marker
        return tile


class TileMap:
    def __init__(self, rows: int, cols: int, tile_size: int):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self._map = np.full((rows, cols, tile_size, tile_size), 255, dtype=np.uint8)

    def set_tile(self, pos: tuple[int, int], img: np.ndarray):
        r, c = pos
        if img.shape != (self.tile_size, self.tile_size):
            raise ValueError(
                f"Tile shape mismatch: expected {(self.tile_size, self.tile_size)}, got {img.shape}"
            )
        self._map[r, c] = img

    def get_map_image(self) -> np.ndarray:
        rows_img = []
        for r in range(self.rows):
            row = np.concatenate([self._map[r, c] for c in range(self.cols)], axis=1)
            rows_img.append(row)
        return np.concatenate(rows_img, axis=0)


@click.command()
@click.argument("path", type=click.Path(file_okay=False, dir_okay=True))
@click.option("--tile_size", type=int, default=1024, show_default=True)
@click.option("--marker_fraction", type=float, default=0.62, show_default=True)
def main(path, tile_size, marker_fraction):
    """
    Generates:
      marker_tile.png         -> 4x3 net image
      marker_tiles_square.png  -> centered square board image
      marker_info.yml         -> marker id mapping
    """
    os.makedirs(path, exist_ok=True)

    marker_factory = MarkerFactory()
    tile_map = TileMap(rows=4, cols=3, tile_size=tile_size)

    face_order = ["left", "bottom", "front", "top", "back", "right"]
    ids = []

    marker_id = 0
    for face in face_order:
        pos = FACE_POSITIONS[face]
        marker_img = marker_factory.create_marker_tile(
            tile_size=tile_size,
            marker_id=marker_id,
            marker_fraction=marker_fraction,
        )
        tile_map.set_tile(pos, marker_img)
        ids.append(marker_id)
        marker_id += 1

    # 4x3 net image
    tile_img = tile_map.get_map_image()

    # Center the 4x3 net inside a 4x4 square canvas
    square_size = tile_size * 4
    tile_img_square = np.full((square_size, square_size), 255, dtype=np.uint8)

    x_offset = tile_size // 2
    y_offset = 0
    tile_img_square[
        y_offset : y_offset + tile_img.shape[0],
        x_offset : x_offset + tile_img.shape[1],
    ] = tile_img

    # Save outputs
    cv2.imwrite(os.path.join(path, "marker_tile.png"), tile_img)
    cv2.imwrite(os.path.join(path, "marker_tiles_square.png"), tile_img_square)

    marker_config = dict(zip(face_order, ids))

    config = {
        "aruco_dict": "4X4_50",
        "tile_size": tile_size,
        "marker_fraction": marker_fraction,
        "markers": marker_config,
    }

    with open(os.path.join(path, "marker_info.yml"), "w") as yml_file:
        yaml.safe_dump(config, yml_file, sort_keys=False)

    print(f"Saved to: {path}")
    print(" - marker_tile.png")
    print(" - marker_tiles_square.png")
    print(" - marker_info.yml")


if __name__ == "__main__":
    main()
