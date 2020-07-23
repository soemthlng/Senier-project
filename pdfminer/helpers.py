import os


def absolute_sample_path(relative_sample_path):
    sample_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../testdata'))  # __file__ means the position of execution code. so this case, means ~~/~~/~~/tests
                                    # and os.path.join concatenating the dir path name correctly for ex) /home/david , /parser -> /home/david/parser
    
    sample_file = os.path.join(sample_dir, relative_sample_path) # so this means ~~/~~/samples/target.pdf
    return sample_file
