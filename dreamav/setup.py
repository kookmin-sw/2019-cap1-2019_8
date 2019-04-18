from setuptools import setup, find_packages

def get_requirements():
    ret = []
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            ret.append(line.strip())

    return ret


requires = get_requirements()

setup(
    name = 'dreamav',
    version = '0.2.2',
    # packages = ['dreamav'],
    packages=find_packages(),
    setup_requires=requires,
    entry_points = {
        'console_scripts': [
            'dreamav = dreamav.__main__:main'
        ]
    })
