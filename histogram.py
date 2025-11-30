import histogram


class Histogram:

    def __init__(self, image):
        assert image.image.mode == "L"
        self._hist = 256 * [0]
        self._image = image
        self._levels = 0
        self._max = 0
        self.recompute_histogram()

    @property
    def levels(self):
        return self._levels

    @property
    def histogram(self):
        return self._hist

    @property
    def max(self):
        return self._max

    def recompute_histogram(self):

        new_hist = 256 * [0]
        self._levels = 0
        self._max = 1

        def compute_function(pix):
            new_hist[pix] += 1
            if new_hist[pix] == 1:
                self._levels += 1

            self._max = max(self._max, new_hist[pix]) # udrzujeme maximum
            return pix

        with self._image.image_map(compute_function, self._image) as img:
            pass

        self._hist = new_hist
        return self

    def comulative_normalized_histogram(self, x):
        return (sum(self.histogram[0:x+1]) /
                (self._image.width * self._image.height))



