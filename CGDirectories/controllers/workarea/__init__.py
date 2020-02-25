import os
import CGDirectories.config as config


def create(path):
    workarea = config.get("workarea")

    def make_workarea():
        playground_dir = os.path.join(path, workarea[0])
        publish_dir = os.path.join(path, workarea[1])
        os.makedirs(playground_dir)
        os.makedirs(publish_dir)

    make_workarea()


if __name__ == '__main__':
    path = os.getcwd()
