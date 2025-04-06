from pylix.algebra import Vector

class AnimationHandler:
    def __init__(self, start_position, end_position, transition_function: Vector, duration, delay,
                 start_rotation = 0, end_rotation=0, supress_del=False):
        self._start_position = start_position
        self._end_position = end_position
        self._transition_function = transition_function # transition_function ist ein 4D Vector
        self._duration = duration
        self._delay = delay
        self._t = -self._delay
        self._supress = supress_del
        #                   HasStarted, isDone
        self._animation_state = [False, False]

        self._start_rotation = start_rotation
        self._end_rotation = end_rotation

        self._finished = list()

    def cubic_bezier(self):
        t = self._t / self._duration
        return ((((1 -t) ** 3) * Vector(dimension=2))
                + (3 * ((1 - t) ** 2) * t) * Vector([self._transition_function[0],self._transition_function[1]])
                + (3 * (1 - t) * (t ** 2)) * Vector([self._transition_function[2],self._transition_function[3]])
                + (t ** 3) * Vector(dimension=2, default_value=1))

    def on_finished(self, func, *args):
        self._finished.append([func,len(args) > 0, args])

    def get_current_animation_step(self):
        if self._t < 0:
            return self._start_position

        progress = self.cubic_bezier()
        pos = self._start_position + (progress[1] * (self._end_position - self._start_position))

        return pos

    def get_current_animation_rotation(self):
        if self._t < 0:
            return self._start_rotation

        progress = self.cubic_bezier()
        progress = self._start_rotation + (progress[1] * (self._end_rotation - self._start_rotation))
        return progress

    def update(self, dt):
        if self._animation_state[0] and not self._animation_state[1]:
            self._t += dt

        if self._t > self._duration:
            self._animation_state[True] = True

            while len(self._finished) > 0:
                a = self._finished.pop()
                if a[1]:
                    a[0](*a[2])
                else:
                    a[0]()

            return -1

    def start(self):
        self._animation_state[False] = True

    def supress_del(self):
        self._supress = True

    def __del__(self):
        if not self._supress:
            while len(self._finished) > 0:
                a = self._finished.pop()
                if a[1]:
                    a[0](*a[2])
                else:
                    a[0]()
