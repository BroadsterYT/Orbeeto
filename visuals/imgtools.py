import typing

import cv2
import numpy
import pygame
from pygame.math import Vector2 as vec


def stack_images(base_image: pygame.Surface, top_image: pygame.Surface, stack_x: int, stack_y: int) -> pygame.Surface:
    """Places an image overtop another image, then returns the new image

    :param base_image: The image being covered over
    :param top_image: The image being placed on top of the base image
    :param stack_x: The x-position to put the top image over the base image (0 -> align left sides)
    :param stack_y: The y-position to put the top image over the base image (0 -> align top edges)
    :return: The stacked image
    """
    output_image = pygame.Surface(vec(base_image.get_width(), base_image.get_height()))
    output_image.blit(base_image, vec(0, 0))
    output_image.blit(top_image, vec(stack_x, stack_y))
    return output_image


def warp(surf: pygame.Surface, warp_pts, smooth=True,
         out: pygame.Surface = None) -> typing.Tuple[pygame.Surface, pygame.Rect]:
    """Stretches a pygame surface to fill a quad using cv2's perspective warp.

        Args:
            surf: The surface to transform.
            warp_pts: A list of four xy coordinates representing the polygon to fill.
                Points should be specified in clockwise order starting from the top left.
            smooth: Whether to use linear interpolation for the image transformation.
                If false, nearest neighbor will be used.
            out: An optional surface to use for the final output. If None or not
                the correct size, a new surface will be made instead.

        Returns:
            [0]: A Surface containing the warped image.
            [1]: A Rect describing where to blit the output surface to make its coordinates
                match the input coordinates.
    """
    if len(warp_pts) != 4:
        raise ValueError("warp_pts must contain four points")

    w, h = surf.get_size()
    is_alpha = surf.get_flags() & pygame.SRCALPHA
    # XXX throughout this method we need to swap x and y coordinates
    # when we pass stuff between pygame and cv2. I'm not sure why .-.
    src_corners = numpy.float32([(0, 0), (0, w), (h, w), (h, 0)])
    quad = [tuple(reversed(p)) for p in warp_pts]

    # find the bounding box of warp points
    # (this gives the size and position of the final output surface).
    min_x, max_x = float('inf'), -float('inf')
    min_y, max_y = float('inf'), -float('inf')
    for p in quad:
        min_x, max_x = min(min_x, p[0]), max(max_x, p[0])
        min_y, max_y = min(min_y, p[1]), max(max_y, p[1])
    warp_bounding_box = pygame.Rect(int(min_x), int(min_y),
                                    int(max_x - min_x),
                                    int(max_y - min_y))

    shifted_quad = [(p[0] - min_x, p[1] - min_y) for p in quad]
    dst_corners = numpy.float32(shifted_quad)

    mat = cv2.getPerspectiveTransform(src_corners, dst_corners)

    orig_rgb = pygame.surfarray.pixels3d(surf)

    flags = cv2.INTER_LINEAR if smooth else cv2.INTER_NEAREST
    out_rgb = cv2.warpPerspective(orig_rgb, mat, warp_bounding_box.size, flags=flags)

    if out is None or out.get_size() != out_rgb.shape[0:2]:
        out = pygame.Surface(out_rgb.shape[0:2], pygame.SRCALPHA if is_alpha else 0)

    pygame.surfarray.blit_array(out, out_rgb)

    if is_alpha:
        orig_alpha = pygame.surfarray.pixels_alpha(surf)
        out_alpha = cv2.warpPerspective(orig_alpha, mat, warp_bounding_box.size, flags=flags)
        alpha_px = pygame.surfarray.pixels_alpha(out)
        alpha_px[:] = out_alpha
    else:
        out.set_colorkey(surf.get_colorkey())

    # XXX swap x and y once again...
    return out, pygame.Rect(warp_bounding_box.y, warp_bounding_box.x,
                            warp_bounding_box.h, warp_bounding_box.w)


if __name__ == '__main__':
    import os
    import timeit

    print(os.getcwd())
    os.chdir('C:\\Users\BroDe\Documents\GitHub\Orbeeto')
    print(os.getcwd())

    sheet = pygame.image.load('sprites/tiles/wall.png')
    img = pygame.Surface((16, 16))
    img.blit(sheet, (0, 0))

    print(timeit.timeit('warp(img, [(0, 0), (0, 32), (16, 128), (16, 0)])', number=1000, globals=globals()))
