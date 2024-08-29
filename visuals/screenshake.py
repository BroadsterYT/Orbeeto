import random as rand

from pygame.math import Vector2 as vec

import constants as cst
import screen


class ScreenShakeQueue:
    """An object that handles screen-shaking capabilities."""

    def __init__(self):
        self.queue = []

    def add(self, amplitude: float, duration: int, rate_of_decay: float = 1.2) -> None:
        """Adds a screen shake to the queue of screen shakes.

        :param amplitude: How intense the shake should be
        :param duration: How long the shake should last
        :param rate_of_decay: The intensity of the decay. Set to 1.2 by default. Should be greater than or equal to 0.
        :return: None
        """
        new_queue = []
        adj_duration = int(duration * (pow(screen.dt, -1) / cst.M_FPS))
        for tick in range(adj_duration):
            decay = (pow(adj_duration - tick, rate_of_decay)) / pow(adj_duration, rate_of_decay)
            queue_input = vec(rand.uniform(-amplitude, amplitude) * decay, rand.uniform(-amplitude, amplitude) * decay)
            new_queue.append(queue_input)

        self.queue = self._combine_queues(new_queue)

    def _combine_queues(self, waiting_queue):
        combined_list = []
        max_length = max(len(self.queue), len(waiting_queue))

        for i in range(max_length):
            value1 = self.queue[i] if i < len(self.queue) else vec(0, 0)
            value2 = waiting_queue[i] if i < len(waiting_queue) else vec(0, 0)
            combined_list.append(value1 + value2)

        return combined_list

    def run(self):
        if len(self.queue) != 0:
            output = self.queue[0]
            self.queue.pop(0)
            return output
        else:
            return vec(0, 0)


screen_shake_queue = ScreenShakeQueue()
