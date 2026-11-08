from functools import lru_cache

from solid2.extensions.bosl2 import hexagon, trapezoid

from hex_chess_board_generator.configuration import ConfigSchema


@lru_cache
def _generate_male_mount(conf: ConfigSchema):
    mnt_size = conf.mount_dims.length_mm
    width_margin = conf.mount_dims.width_margin_mm
    mounting_male_len = mnt_size - width_margin
    return (
        trapezoid(
            h=mounting_male_len,
            w1=mnt_size - width_margin,
            w2=mnt_size + conf.mount_dims.base_diff_mm - width_margin,
            center=True,
        )
        .linear_extrude(conf.mount_dims.height_mm - conf.mount_dims.height_margin_mm)
        .forward(conf.hex_dims.r_mm + mounting_male_len // 2)
    )


@lru_cache
def _generate_female_mount(conf: ConfigSchema):
    mnt_size = conf.mount_dims.length_mm
    return (
        trapezoid(
            h=mnt_size,
            w1=mnt_size,
            w2=mnt_size + conf.mount_dims.base_diff_mm,
            center=True,
        )
        .linear_extrude(conf.mount_dims.height_mm)
        .back(conf.hex_dims.r_mm - mnt_size // 2)
    )


def _add_mounting_holes(base_shape, conf: ConfigSchema):
    return base_shape + _generate_male_mount(conf) - _generate_female_mount(conf)


def generate_hexagon(conf: ConfigSchema):
    base = hexagon(ir=conf.hex_dims.r_mm).linear_extrude(conf.hex_dims.height_mm)

    base = _add_mounting_holes(base, conf)
    base = _add_mounting_holes(base.rotateZ(60), conf)
    base = _add_mounting_holes(base.rotateZ(60), conf)
    return base
