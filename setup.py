from setuptools import setup

setup(
    name='yamm',
    version='0.0.1',
    license='GPL',
    description='yet another markov module',
    author='Tim Pauli <tim.pauli@folkwang-uni.de>, Levin Zimmermann <levin-eric.zimmermann@folkwang-uni.de>',
    url='https://github.com/inkeye/yamm',
    packages=['yamm'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=3.5'
)
