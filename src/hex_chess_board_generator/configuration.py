from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from omegaconf import OmegaConf


@dataclass(frozen=True)
class HexagonDimensions:
    r_mm: float = 15.0
    height_mm: float = 8.0


@dataclass(frozen=True)
class MountingDimensions:
    length_mm: float = 5.0
    height_mm: float = 7.0
    base_diff_mm: float = 2.0
    height_margin_mm: float = 1.0
    width_margin_mm: float = 0.06


@dataclass(frozen=True)
class ConfigSchema:
    hex_dims: HexagonDimensions = field(default_factory=HexagonDimensions)
    mount_dims: MountingDimensions = field(default_factory=MountingDimensions)
    outpur_dir: Path = Path("./build")


def load_config(path: Path) -> ConfigSchema:
    yaml_config = OmegaConf.load(path)

    schema = OmegaConf.structured(ConfigSchema)
    merged = OmegaConf.merge(schema, yaml_config)
    return cast(ConfigSchema, OmegaConf.to_object(merged))
