from argparse import ArgumentParser
from pathlib import Path

from hex_chess_board_generator.configuration import load_config
from hex_chess_board_generator.generator import generate_hexagon


def arguments_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "--config-path",
        "-c",
        type=str,
        required=False,
        default="src/configs/default.conf.yaml",
    )
    return parser


def main() -> None:
    args = arguments_parser().parse_args()
    conf = load_config(path=Path(args.config_path))

    model = generate_hexagon(conf)
    conf.outpur_dir.mkdir(parents=True, exist_ok=True)
    model.save_as_stl(conf.outpur_dir / "hexagon.stl")


if __name__ == "__main__":
    main()
