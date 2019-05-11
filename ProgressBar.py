import math

class ProgressBar():
    """Create a progess bar"""
    def __init__(self, percent_complete):
        self.percent_complete = percent_complete

    def gen_progress_string(self, bar_length=15):
        """create a progress bar of n length"""
        p = math.floor(scale(self.percent_complete, 0, 100, 0, bar_length))

        bar = map(lambda x:'█', range(p))
        bar = ''.join(bar)

        bar_empty = ''.join( map( lambda x:'░', range(bar_length - p) ) )
        bar = ''.join( [bar, bar_empty] )
        progress_string = str(math.floor(self.percent_complete))
        bar = ''.join([ bar, " ", progress_string, "%" ])
        return bar
