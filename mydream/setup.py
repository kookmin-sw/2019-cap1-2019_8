from setuptools import setup, find_packages

def get_requirements():
    ret = []
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            ret.append(line.strip())

    return ret


requires = get_requirements()

setup(
    name = 'mydream',
    version = '0.2.1',
    # packages = ['mydream'],
    packages=find_packages(),
    setup_requires=requires,
    entry_points = {
        'console_scripts': [
            'mydream = mydream.__main__:main'
        ]
    })
