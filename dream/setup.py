from setuptools import setup

setup(
    name="dream",
    version="0.1.0",
    packages=["lightgbm","numpy","dream"],
    entry_points={
        'console_script': [
            'dream=dream.__main__:main'
        ]
    }
)