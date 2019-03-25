from setuptools import setup, find_packages

def get_requirements():
    ret = []
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            ret.append(line.strip())

    return ret


requires = get_requirements()

setup(
    name = 'dream-av',
    version = '0.2.1',
    # packages = ['dream-av'],
    packages=find_packages(),
    setup_requires=requires,
    entry_points = {
        'console_scripts': [
            'dream-av = dream-av.__main__:main'
        ]
    })
