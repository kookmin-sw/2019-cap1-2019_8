from setuptools import setup

setup(
    name="dream",
    version="0.1.0",
    packages=["dream"],
    setup_requires=["lightgbm", "numpy"],
    entry_points={
        'console_script': [
            'dream=dream.cli.cli:main'
        ]
    }
)